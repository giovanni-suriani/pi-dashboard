import os
import re
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

# Logging setup
logger = logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(funcName)s:%(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = settings.BASE_DIR


def delete_old_charts():
    """
    Delete charts whose month component does not match the current month
    from the 'pisGrafico' and 'wordcloud_images' directories.
    """
    now_month = datetime.datetime.now().month

    chart_pis_storage = os.path.join(
        BASE_DIR, "dashboard", "static", "chart_storage", "pisGrafico"
    )
    pis_charts = os.listdir(chart_pis_storage)

    for chart in pis_charts:
        match = re.search(r"\d{4}-(\d{2})", chart)
        if match:
            chart_month = int(match.group(1))
            if chart_month != now_month:  # If it's not the current month
                chart_path = os.path.join(chart_pis_storage, chart)
                if os.path.isfile(chart_path):
                    os.remove(chart_path)
                    logger.info(f"Deleted old chart file: {chart_path}")

    chart_wordcloud_storage = os.path.join(
        BASE_DIR, "dashboard", "static", "chart_storage", "wordcloud_images"
    )
    wordcloud_charts = os.listdir(chart_wordcloud_storage)

    for chart in wordcloud_charts:
        match = re.search(r"\d{4}-(\d{2})", chart)
        if match:
            chart_month = int(match.group(1))
            if chart_month != now_month:
                chart_path = os.path.join(chart_wordcloud_storage, chart)
                if os.path.isfile(chart_path):
                    os.remove(chart_path)
                    logger.info(f"Deleted old chart file: {chart_path}")


def delete_all_charts():
    """
    Delete all charts from the 'pisGrafico' and 'wordcloud_images' directories.
    """
    chart_pis_storage = os.path.join(
        BASE_DIR, "dashboard", "static", "chart_storage", "pisGrafico"
    )
    pis_charts = os.listdir(chart_pis_storage)

    for chart in pis_charts:
        chart_path = os.path.join(chart_pis_storage, chart)
        if os.path.isfile(chart_path):
            os.remove(chart_path)
            logger.info(f"Deleted chart file: {chart_path}")

    chart_wordcloud_storage = os.path.join(
        BASE_DIR, "dashboard", "static", "chart_storage", "wordcloud_images"
    )
    wordcloud_charts = os.listdir(chart_wordcloud_storage)

    for chart in wordcloud_charts:
        chart_path = os.path.join(chart_wordcloud_storage, chart)
        if os.path.isfile(chart_path):
            os.remove(chart_path)
            logger.info(f"Deleted chart file: {chart_path}")


class Command(BaseCommand):
    help = "Delete old charts from previous months or delete all charts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete_old",
            action="store_true",
            help="Delete old charts from previous months",
        )
        parser.add_argument(
            "--delete_all", action="store_true", help="Delete all charts"
        )

    def handle(self, *args, **options):
        logger.info(f"Executando rotina em {datetime.datetime.now()}")
        
        if options["delete_old"]:
            logging.info("Deleting old charts (previous months)...")
            delete_old_charts()
            logging.info("Old charts deleted.")

        if options["delete_all"]:
            logging.info("Deleting ALL charts...")
            delete_all_charts()
            logging.info("All charts deleted.")


# python3 manage.py clean_old_charts --delete_old
