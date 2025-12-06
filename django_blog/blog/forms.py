from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Comment
# Get the active User model TagWidget()", "tags (usually django.contrib.auth.models.User)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for user registration that includes the email field.
    The email field is set to be required.
    """
    email = forms.EmailField(required=True, help_text='Required. Must be a valid email address.')

    class Meta(UserCreationForm.Meta):
        # Use the base User model and add the 'email' field
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

# Simple form for profile editing (allows changing first_name, last_name, and email)
class UserProfileEditForm(UserChangeForm):
    """
    A form for users to update their profile information.
    Inherits from UserChangeForm but excludes the password field for security
    and simplifies the fields presented to the user.
    """
    password = None  # Remove password field inherited from UserChangeForm

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }