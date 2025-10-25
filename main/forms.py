from django import forms
from django.forms import ModelForm
<<<<<<< HEAD
from main.models import Venue, Article, Events
from main.models import Comment
=======
from main.models import Venue

form_control_attrs = {'class': 'form-control'}
form_control_textarea_attrs = {'class': 'form-control', 'rows': 4}
form_control_url_attrs = {'class': 'form-control', 'placeholder': 'https://...'}
>>>>>>> origin/main

# --- Define common widget attributes ---
# Use these for consistency across forms
form_control_attrs = {'class': 'form-control'}
form_control_textarea_attrs = {'class': 'form-control', 'rows': 4}
form_control_url_attrs = {'class': 'form-control', 'placeholder': 'https://...'}

# --- Venue Form ---
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # Ensure these fields exist in your Venue model in models.py
        fields = [
            "name", "city", "address", "contact", "website",
<<<<<<< HEAD
            # Add these fields to your Venue model if they don't exist:
            # "price_range", "facilities",
            "image_url",
            # Add these fields to your Venue model if needed:
            # "image_url_2", "image_url_3", "image_url_4", "image_url_5"
=======
            "price_range", "facilities",
            "image_url",
            "image_url_2", "image_url_3", "image_url_4", "image_url_5"
>>>>>>> origin/main
        ]

        widgets = {
            'name': forms.TextInput(attrs=form_control_attrs),
            'city': forms.TextInput(attrs=form_control_attrs),
            'address': forms.TextInput(attrs=form_control_attrs),
<<<<<<< HEAD
            'contact': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., 0812...'}), # Added placeholder example
            'website': forms.URLInput(attrs=form_control_url_attrs),
            # Uncomment these if fields exist in model
            # 'price_range': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., $$ - $$$'}),
            # 'facilities': forms.Textarea(attrs=form_control_textarea_attrs),
            'image_url': forms.URLInput(attrs=form_control_url_attrs),
            # Uncomment these if fields exist in model
            # 'image_url_2': forms.URLInput(attrs=form_control_url_attrs),
            # 'image_url_3': forms.URLInput(attrs=form_control_url_attrs),
            # 'image_url_4': forms.URLInput(attrs=form_control_url_attrs),
            # 'image_url_5': forms.URLInput(attrs=form_control_url_attrs),
        }
        # Add labels if desired

# --- Article (Blog) Form ---
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "category", "image_url"]

        widgets = {
            'title': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'Blog Post Title'}),
            # Use common textarea attributes, override rows if needed
            'content': forms.Textarea(attrs={**form_control_textarea_attrs, 'rows': 10, 'placeholder': 'Write your blog content here...'}),
            'category': forms.Select(attrs={'class': 'form-control'}), # Apply class to select dropdown
            'image_url': forms.URLInput(attrs={**form_control_url_attrs, 'placeholder': 'https://... (Optional Banner Image)'}),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'category': 'Category',
            'image_url': 'Image URL (Optional)',
        }

# --- Event Form ---
class EventForm(ModelForm):
    class Meta:
        model = Events
        # Ensure these fields match your Events model
        fields = ["name", "type", "date", "venue", "price", "description", "image_url"]

        widgets = {
            'name': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., Morning Fun Match'}),
            'type': forms.Select(attrs={'class': 'form-control'}), # Category should be Select based on model choices
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), # Calendar widget
            'venue': forms.Select(attrs={'class': 'form-control'}), # Venue selection dropdown
            'price': forms.NumberInput(attrs={**form_control_attrs, 'placeholder': 'e.g., 150000'}),
            'description': forms.Textarea(attrs={**form_control_textarea_attrs, 'placeholder': 'Event description...'}),
            'image_url': forms.URLInput(attrs={**form_control_url_attrs, 'placeholder': 'https://... (Optional)'}),
        }

        labels = {
            'name': 'Event Name',
            'type': 'Match Category',
            'date': 'Date & Time',
            'venue': 'Venue',
            'price': 'Price (Rp)',
            'description': 'Description',
            'image_url': 'Image URL (Optional)',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
=======
            'contact': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., 0812...'}),
            'website': forms.URLInput(attrs=form_control_url_attrs),
            'price_range': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., $$ - $$$'}),
            'facilities': forms.Textarea(attrs=form_control_textarea_attrs),
            'image_url': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_2': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_3': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_4': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_5': forms.URLInput(attrs=form_control_url_attrs),
>>>>>>> origin/main
        }