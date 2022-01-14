import logging
from django.conf import settings
from django.core.management.base import BaseCommand
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from podcasts.models import Episode

logger = logging.getLogger(__name__)

def delete_old_job_executions(max_age=604_800):
    "delete logs older than age || 604_800 = 1 week"
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def save_new_episode(feed):
    """
    Saves new episodes
    """
    # feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid):
            episode = Episode(
                podcast_title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()

def fetch_cyrusSays():
    """ Fetches new shows from JRE """
    _feed = feedparser.parse("http://cyrussays.ivm.libsynpro.com/rss")
    save_new_episode(_feed)


def fetch_realPython():
    _feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
    save_new_episode(_feed)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_realPython,
            trigger="interval",
            hours=4,
            id="The Real Python Podcast",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Real Python Podcast.")

        scheduler.add_job(
            fetch_cyrusSays,
            trigger="interval",
            hours=4,
            id="Cyrus Says",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Cyrus Says.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
