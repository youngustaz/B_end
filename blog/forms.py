from django import forms
from .models import Post, Comment, Testimonial, Project
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'published']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,   # reduce height
                'cols': 30,  # reduce width
                'placeholder': 'Write your comment here...',
            }),
        }

class ProjectForm(forms.ModelForm):   # <-- add this
    class Meta:
        model = Project
        fields = ['title', 'description', 'url', 'screenshot']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'message']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address")

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Password must be at least 7 characters (letters or numbers)."  # 👈 custom text
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text=None  # 👈 removes default duplicate text
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": None,
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 7:
            raise forms.ValidationError("Password must be at least 7 characters long.")
        return password1