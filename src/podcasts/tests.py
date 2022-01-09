from django.test import TestCase
from django.utils import timezone
from .models import Episode
from django.urls.base import reverse


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

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_lists_content(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "Podcast 1")
        