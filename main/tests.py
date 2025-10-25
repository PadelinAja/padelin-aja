from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from main.forms import CommentForm

class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        """Test the form is valid when provided with text."""
        form = CommentForm(data={'text': 'This is a test comment.'})
        # ASSERT: The form should be valid
        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        """Test the form is invalid when the text field is empty."""
        form = CommentForm(data={'text': ''})
        # ASSERT: The form should be invalid
        self.assertFalse(form.is_valid())
        # ASSERT: Check for the specific error in the 'text' field
        self.assertIn('text', form.errors.keys())
        self.assertIn('This field is required.', form.errors['text'])

# main/tests.py (Start of the file)
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from main.models import Article, Venue, Events, Rating, Comment # Ensure these are imported
from main.forms import ArticleForm, CommentForm
from django.contrib.contenttypes.models import ContentType
import uuid # For UUID primary keys

# 💡 Helper to create a user for authentication
class AppTestSetup(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        
        # Create a Venue for testing
        self.venue = Venue.objects.create(
            name="Test Venue", city="Jakarta", address="123 Street", 
            contact="12345", website="http://test.com", user=self.user1
        )
        # Create an Article for testing
        self.article = Article.objects.create(
            title="Test Article", content="Test content.", category="Sport", 
            published_date=timezone.now(), user=self.user1
        )
        # Create an Event for testing
        self.event = Events.objects.create(
            name="Test Event", type="Match", date=datetime(2025, 12, 31, 19, 0, tzinfo=timezone.utc), 
            venue=self.venue, price=100000, description="Fun event", user=self.user1
        )
        
        # Pre-calculate content types
        self.article_type = ContentType.objects.get_for_model(Article)
        self.venue_type = ContentType.objects.get_for_model(Venue)
        self.event_type = ContentType.objects.get_for_model(Events)

        # URLs
        self.create_venue_url = reverse('main:create_venue')
        self.create_article_url = reverse('main:create_article')
        self.rate_url = reverse('main:rate_item')
        self.article_detail_url = reverse('main:show_article', args=[self.article.id]) 
        # Note: You have to ensure 'id' is used in show_article redirect or change URL to use 'article_id'

class CreationViewTest(AppTestSetup):
    def test_create_article_success(self):
        """Test authenticated user can create an article successfully."""
        self.client.login(username='testuser1', password='testpassword')
        
        initial_count = Article.objects.count()
        new_article_data = {
            'title': 'New Test Blog',
            'content': 'Amazing new content.',
            'category': 'Food', 
            # image_url is optional
        }
        
        response = self.client.post(self.create_article_url, data=new_article_data, follow=True)
        
        # ASSERT: Redirects on success (HTTP 302 then 200)
        self.assertEqual(response.status_code, 200) 
        # ASSERT: Article count increases
        self.assertEqual(Article.objects.count(), initial_count + 1)
        # ASSERT: Check ownership
        new_article = Article.objects.latest('published_date')
        self.assertEqual(new_article.user, self.user1)

    def test_create_article_unauthenticated(self):
        """Test unauthenticated user is redirected to login."""
        response = self.client.post(self.create_article_url, data={})
        # ASSERT: Redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('main:login'), response.url)

class DeleteEditViewTest(AppTestSetup):
    def test_ajax_delete_article_success(self):
        """Test authenticated owner can delete an article via AJAX."""
        self.client.login(username='testuser1', password='testpassword')
        article_id = self.article.id
        
        delete_url = reverse('main:ajax_delete', args=['article', article_id])
        
        # ASSERT: Item exists before deletion
        self.assertTrue(Article.objects.filter(id=article_id).exists())
        
        response = self.client.post(delete_url)
        
        # ASSERT: Returns JSON success
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        # ASSERT: Item is gone
        self.assertFalse(Article.objects.filter(id=article_id).exists())

    def test_ajax_delete_permission_denied(self):
        """Test deletion attempt by non-owner is denied (403)."""
        self.client.login(username='testuser2', password='testpassword') # Log in as different user
        article_id = self.article.id
        
        delete_url = reverse('main:ajax_delete', args=['article', article_id])
        
        response = self.client.post(delete_url)
        
        # ASSERT: Permission denied
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'success': False, 'errors': 'Permission denied.'})
        # ASSERT: Item still exists
        self.assertTrue(Article.objects.filter(id=article_id).exists())

class RatingCommentTest(AppTestSetup):
    def test_rate_item_creation(self):
        """Test a user can successfully create a new rating via AJAX."""
        self.client.login(username='testuser1', password='testpassword')
        
        rate_data = {
            'type': 'article',
            'id': self.article.id,
            'score': 5
        }
        
        initial_rating_count = Rating.objects.count()
        response = self.client.post(self.rate_url, data=rate_data)
        
        # ASSERT: Successful response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.count(), initial_rating_count + 1)
        # ASSERT: JSON content is correct
        self.assertJSONEqual(response.content, {'message': 'Rating saved!', 'average': 5.0, 'your_rating': 5})
        
    def test_rate_item_update(self):
        """Test a user can successfully update an existing rating via AJAX."""
        self.client.login(username='testuser1', password='testpassword')
        
        # Create initial rating
        Rating.objects.create(
            user=self.user1, content_type=self.article_type, object_id=self.article.id, score=1
        )
        initial_rating_count = Rating.objects.count()
        
        rate_data = {
            'type': 'article',
            'id': self.article.id,
            'score': 4 # New score
        }
        
        response = self.client.post(self.rate_url, data=rate_data)
        
        # ASSERT: No new rating object created (count is same)
        self.assertEqual(Rating.objects.count(), initial_rating_count)
        # ASSERT: Rating was updated
        updated_rating = Rating.objects.get(user=self.user1, object_id=self.article.id)
        self.assertEqual(updated_rating.score, 4)

    def test_rate_item_invalid_score(self):
        """Test rating with an invalid score (outside 1-5 range) returns 400."""
        self.client.login(username='testuser1', password='testpassword')
        
        rate_data = {
            'type': 'article',
            'id': self.article.id,
            'score': 99 # Invalid score
        }
        
        response = self.client.post(self.rate_url, data=rate_data)
        
        # ASSERT: Returns HTTP 400
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid score value.'})

    def test_comment_on_article_success(self):
        """Test comment submission on the article detail page."""
        self.client.login(username='testuser1', password='testpassword')
        
        comment_data = {
            'text': 'Great article, thanks!',
        }
        
        initial_comment_count = Comment.objects.count()
        
        # NOTE: show_article handles the comment POST and redirects
        response = self.client.post(self.article_detail_url, data=comment_data)
        
        # ASSERT: Successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), initial_comment_count + 1)
        # ASSERT: Check comment content and link
        new_comment = Comment.objects.latest('created_at')
        self.assertEqual(new_comment.text, 'Great article, thanks!')
        self.assertEqual(new_comment.content_object, self.article)

