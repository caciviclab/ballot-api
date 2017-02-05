import csv
import io
import logging
import re
import tempfile
import urllib.request

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from gsheets.models import Candidate
from gsheets.serializers import CandidateSerializer


CANDIDATES_SHEET = 'https://docs.google.com/spreadsheets/d/1272oaLyQhKwQa6RicA5tBso6wFruum-mgrNm3O3VogI/pub?gid=0&single=true&output=csv' # noqa
REFERENDUMS_SHEET = 'https://docs.google.com/spreadsheets/d/1272oaLyQhKwQa6RicA5tBso6wFruum-mgrNm3O3VogI/pub?gid=1693935349&single=true&output=csv' # noqa
REFERENDUM_NAME_TO_NUMBER_SHEET = 'https://docs.google.com/spreadsheets/d/1272oaLyQhKwQa6RicA5tBso6wFruum-mgrNm3O3VogI/pub?gid=896561174&single=true&output=csv' # noqa
COMMITTEES_SHEET = 'https://docs.google.com/spreadsheets/d/1272oaLyQhKwQa6RicA5tBso6wFruum-mgrNm3O3VogI/pub?gid=1995437960&single=true&output=csv' # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import data from Google Sheets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            default=False,
            help="Import the entity even if it already exists.")

    def handle(self, *args, **options):
        force = options['force']

        with urllib.request.urlopen(CANDIDATES_SHEET) as request:
            with tempfile.TemporaryFile() as csvfile:
                csvfile.write(request.read())
                csvfile.seek(0)
                reader = csv.DictReader(io.TextIOWrapper(csvfile, encoding='utf-8'))

                total = 0
                imported = 0
                import_errors = 0
                for row in reader:
                    total += 1
                    name = row.get('Candidate', None)
                    if not name:
                        continue

                    exists = True
                    try:
                        Candidate.objects.get(candidate=name)
                    except ObjectDoesNotExist:
                        exists = False

                    if exists and not force:
                        continue
                    field_names = [field.name for field in Candidate._meta.get_fields()]
                    model = ((k.lower(), v) for k, v in row.items())
                    model = ((re.sub(r'\s+', '_', k), v) for k, v in model)
                    model = ((re.sub(r'[^a-z_]', '', k), v) for k, v in model)
                    model = dict((k, v) for k, v in model if k in field_names)

                    # Convert fppc
                    fppc = model.get('fppc', None)
                    if not fppc:
                        model['fppc'] = None

                    # Parse booleans
                    accepted_expenditure_ceiling = model.get('accepted_expenditure_ceiling', False)
                    model['accepted_expenditure_ceiling'] = bool(accepted_expenditure_ceiling)

                    # Convert twitter @handle to URL
                    twitter = model.get('twitter', None)
                    if twitter:
                        # Drop the first char (@)
                        model['twitter'] = 'https://twitter.com/%s' % twitter[1:]

                    logger.debug(model)
                    serializer = CandidateSerializer(data=model)
                    if not serializer.is_valid():
                        import_errors += 1
                        logger.error('Candidate could not be parsed: name="%s" parse_errors=%s row=%s',
                                     name, serializer.errors, model)
                        continue

                    Candidate.objects.update_or_create(candidate=name, defaults=serializer.validated_data)
                    imported += 1
                    logger.info('Imported candidate "%s"' % name)

                logger.info('Import candidates complete: total=%s imported=%s errors=%s',
                            total, imported, import_errors)
