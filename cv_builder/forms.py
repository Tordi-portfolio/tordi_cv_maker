# cv_builder/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CV

# Form for creating/editing CV entries
class CVForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to all fields automatically
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-md'})

    class Meta:
        model = CV
        exclude = ['user']  # User is assigned automatically in the view

# Form for user registration with Email support
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to the default fields as well
        for field in self.fields.values():
            if field.widget.input_type != 'checkbox': # Avoid styling checkboxes
                field.widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-md'})