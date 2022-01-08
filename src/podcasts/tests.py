from django.test import TestCase
from django.utils import timezone
from .models import Episode

class PodCastsTests(TestCase):
    def setUp(self):
        self.episode = Episode.objects.create(
            podcast_title="Podcast 1",
            description="lorem ipsum hakuna matata cheese burger",
            pub_date=timezone.now(),
            url="https://podcasts.com",
            image="https://podcasts.image.com",
            podcast_name="Podcast Name",
            guid="del12o9123-124-asd123512"
        )

    def test_episode_content(self):
        self.assertEqual(self.episode.description, "lorem ipsum hakuna matata cheese burger")
        self.assertEqual(self.episode.url, "https://podcasts.com")
        self.assertEqual(self.episode.guid, "del12o9123-124-asd123512")

    def test_episode_str_representation(self):
        self.assertEqual(str(self.episode), "Podcast Name: Podcast 1")
