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