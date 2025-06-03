from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Pet, Post, Comment, Message,VetNote
from .models import Appointment



User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'gender']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image_url', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows':4, 'cols':40, 'placeholder': 'Write your post...'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Optional image URL'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'cols':40, 'placeholder': 'Write a comment...'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'cols':40, 'placeholder': 'Write your message...'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'city', 'user_type', 'profile_image']
        widgets = {
            'user_type': forms.Select()
        }


class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    USER_TYPES = [
        ('PetOwner', 'Pet Owner'),
        ('Veterinarian', 'Veterinarian'),
        ('Admin', 'Admin'),
    ]
    user_type = forms.ChoiceField(label='User Type', choices=USER_TYPES, required=True)



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type']
        widgets = {
            'user_type': forms.Select()
        }



class VetNoteForm(forms.ModelForm):
    class Meta:
        model = VetNote
        fields = ['pet', 'note']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }        



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'date', 'reason']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }        