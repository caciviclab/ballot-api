import csv
import io
import logging
import re
import tempfile
import urllib.request

from django.core.management.base import BaseCommand

from gsheets import parsers


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

    def format_csv_fields(self, row):
        """Lowercases the keys of row and removes any special characters"""

        # Lowercase the keys
        model = ((k.lower(), v) for k, v in row.items())

        # Replace spaces with underscore
        model = ((re.sub(r'\s+', '_', k), v) for k, v in model)

        # Strip other characters
        model = ((re.sub(r'[^a-z_]', '', k), v) for k, v in model)

        return dict(model)

    def handle(self, *args, **options):
        self.fetch_and_parse_from_url(CANDIDATES_SHEET, parsers.CandidateParser(), **options)
        self.fetch_and_parse_from_url(COMMITTEES_SHEET, parsers.CommitteeParser(), **options)
        self.fetch_and_parse_from_url(REFERENDUMS_SHEET, parsers.ReferendumParser(), **options)
        self.fetch_and_parse_from_url(REFERENDUM_NAME_TO_NUMBER_SHEET, parsers.ReferendumMappingParser(), **options)

    def fetch_and_parse_from_url(self, url, parser, force=False, **options):
        with urllib.request.urlopen(url) as request:
            with tempfile.TemporaryFile() as csvfile:
                csvfile.write(request.read())
                csvfile.seek(0)
                reader = csv.DictReader(io.TextIOWrapper(csvfile, encoding='utf-8'))

                total = 0
                imported = 0
                import_errors = 0
                for row in reader:
                    total += 1

                    row = self.format_csv_fields(row)
                    logger.debug(row)

                    exists = parser.exists_in_db(row)
                    if exists and not force:
                        # Skip this row
                        continue

                    id = row.get(parser.key)

                    try:
                        data = parser.parse(row)
                        logger.debug(data)
                        model, created = parser.commit(data)
                    except Exception as err:
                        import_errors += 1
                        logger.error('%s "%s" could not be parsed: parse_errors=%s row=%s',
                                     parser.name, id, err, row)
                        logger.exception(err)
                        continue

                    imported += 1
                    if created:
                        logger.info('Created %s "%s"', parser.name, id)
                    else:
                        logger.info('Updated %s "%s"', parser.name, id)

                logger.info('Import %s data complete: total=%s imported=%s errors=%s',
                            parser.name, total, imported, import_errors)
