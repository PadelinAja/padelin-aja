from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from main.forms import VenueForm, ArticleForm, EventForm
from main.models import Venue, Article, Events, Rating


class RatingTests(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(
            name="Test Venue", city="Jakarta", address="Street 123"
        )

    def test_anonymous_can_submit_comment_and_rating(self):
        response = self.client.post(reverse('main:rate_item'), {
            'type': 'venue',
            'id': str(self.venue.id),
            'score': '4',
            'comment': 'Great court and friendly staff!',
            'name': 'Anonymous Tester'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Rating saved!')
        rating = Rating.objects.first()
        self.assertIsNotNone(rating)
        self.assertEqual(rating.score, 4)
        self.assertEqual(rating.comment, 'Great court and friendly staff!')
        self.assertEqual(rating.anonymous_name, 'Anonymous Tester')


TEST_TEMPLATES = {
    "main.html": "MAIN OK",
    "venues.html": "VENUES OK",
    "article_page.html": "ARTICLES OK",
    "event_page.html": "EVENTS OK",
    "article_detail.html": "ARTICLE: {{ article.title }}",
    "event_detail.html": "EVENT: {{ event.name }}",
    "venue_detail.html": "VENUE: {{ venue.name }}",
}


def locmem_templates_settings():
    return [{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "loaders": [
                ("django.template.loaders.locmem.Loader", TEST_TEMPLATES),
            ],
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }]


@override_settings(TEMPLATES=locmem_templates_settings())
class FormFieldTests(TestCase):
    def test_venue_form_fields(self):
        form = VenueForm()
        expected_fields = [
            "name", "city", "address", "contact", "website",
            "price_range", "facilities",
            "image_url", "image_url_2", "image_url_3", "image_url_4", "image_url_5"
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_article_form_fields(self):
        form = ArticleForm()
        expected_fields = ["title", "content", "category", "image_url"]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_event_form_fields(self):
        form = EventForm()
        expected_fields = ["name", "type", "date", "venue", "price", "description", "image_url"]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_venue_form_minimal_valid(self):
        data = {
            "name": "Padel Court A",
            "city": "Jakarta",
            "address": "Jl. Padel No.1",
        }
        form = VenueForm(data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_event_form_invalid_without_requireds(self):
        form = EventForm(data={})
        self.assertFalse(form.is_valid())


@override_settings(TEMPLATES=locmem_templates_settings())
class RatingModelTests(TestCase):
    def test_create_anonymous_rating_for_venue(self):
        v = Venue.objects.create(name="Court A", address="Address", city="Jakarta")
        ct = ContentType.objects.get_for_model(Venue)
        r = Rating.objects.create(
            user=None,
            anonymous_name="Alice",
            score=5,
            comment="Great courts!",
            content_type=ct,
            object_id=v.id,
        )
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(r.content_object, v)
        self.assertEqual(str(v), "Court A")


@override_settings(TEMPLATES=locmem_templates_settings())
class PublicViewsSmokeTests(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(name="Court A", address="Address", city="Jakarta")
        self.article = Article.objects.create(
            title="Intro to Padel",
            content="Content...",
            category=Article.CategoryChoices.BEGINNER,
        )
        self.event = Events.objects.create(
            name="Morning Match",
            type=Events.MatchType.FUN_MATCH,
            description="Friendly game.",
            date=timezone.now(),
            price=0,
            venue=self.venue,
        )

    def test_list_pages_load(self):
        for name in ("main:show_main", "main:show_venues", "main:article_list", "main:event_page"):
            resp = self.client.get(reverse(name))
            self.assertEqual(resp.status_code, 200, msg=f"{name} did not return 200")

    def test_detail_pages_load(self):
        checks = [
            ("main:show_venue", (self.venue.id,)),
            ("main:show_article", (self.article.id,)),
            ("main:show_event", (self.event.id,)),
        ]
        for name, args in checks:
            resp = self.client.get(reverse(name, args=args))
            self.assertEqual(resp.status_code, 200, msg=f"{name} with {args} did not return 200")
