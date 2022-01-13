from django.core.management.base import BaseCommand
import feedparser
from dateutil import parser
from podcasts.models import Episode


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
    def handle(self, *args, **options):
        fetch_cyrusSays()
        fetch_realPython()