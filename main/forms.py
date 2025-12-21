from django import forms
from django.forms import ModelForm
from main.models import Venue

form_control_attrs = {'class': 'form-control'}
form_control_textarea_attrs = {'class': 'form-control', 'rows': 4}
form_control_url_attrs = {'class': 'form-control', 'placeholder': 'https://...'}

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
            "price_range", "facilities",
            "image_url",
            "image_url_2", "image_url_3", "image_url_4", "image_url_5"
        ]

        widgets = {
            'name': forms.TextInput(attrs=form_control_attrs),
            'city': forms.TextInput(attrs=form_control_attrs),
            'address': forms.TextInput(attrs=form_control_attrs),
            'contact': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., 0812...'}),
            'website': forms.URLInput(attrs=form_control_url_attrs),
            'price_range': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., $$ - $$$'}),
            'facilities': forms.Textarea(attrs=form_control_textarea_attrs),
            'image_url': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_2': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_3': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_4': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_5': forms.URLInput(attrs=form_control_url_attrs),
        }
from django import forms
from django.forms import ModelForm
from main.models import Venue, Article, Events, UserProfile

form_control_attrs = {'class': 'form-control'}
form_control_textarea_attrs = {'class': 'form-control', 'rows': 4}
form_control_url_attrs = {'class': 'form-control', 'placeholder': 'https://...'}

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = [
            "name", "city", "address", "contact", "website",
            "price_range", "facilities",
            "image_url",
            "image_url_2", "image_url_3", "image_url_4", "image_url_5"
        ]

        widgets = {
            'name': forms.TextInput(attrs=form_control_attrs),
            'city': forms.TextInput(attrs=form_control_attrs),
            'address': forms.TextInput(attrs=form_control_attrs),
            'contact': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., 0812...'}),
            'website': forms.URLInput(attrs=form_control_url_attrs),
            'price_range': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., $$ - $$$'}),
            'facilities': forms.Textarea(attrs=form_control_textarea_attrs),
            'image_url': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_2': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_3': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_4': forms.URLInput(attrs=form_control_url_attrs),
            'image_url_5': forms.URLInput(attrs=form_control_url_attrs),
        }

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "category", "image_url"]

        widgets = {
            'title': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'Blog Post Title'}),
            'content': forms.Textarea(attrs={**form_control_textarea_attrs, 'rows': 10, 'placeholder': 'Write your blog content here...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={**form_control_url_attrs, 'placeholder': 'https://... (Optional Banner Image)'}),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'category': 'Category',
            'image_url': 'Image URL (Optional)',
        }

class EventForm(ModelForm):
    class Meta:
        model = Events
        fields = ["name", "type", "date", "venue", "price", "description", "image_url"]

        widgets = {
            'name': forms.TextInput(attrs={**form_control_attrs, 'placeholder': 'e.g., Morning Fun Match'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'venue': forms.Select(attrs={'class': 'form-control'}),
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

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
            "hobbies",
            "competence",
            "profile_picture",
        ]
        widgets = {
            "hobbies": forms.TextInput(
                attrs={"placeholder": "Padel, Futsal, Photography"}
            ),
            "competence": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe your experience..."}
            ),
        }
