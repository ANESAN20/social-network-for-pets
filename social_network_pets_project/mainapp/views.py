from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.shortcuts import render,redirect
from .forms import RegisterForm, PetForm, PostForm, CommentForm
from .models import Pet, Post, Like, Friendship, Message
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import MessageForm
from .forms import ProfileForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CustomLoginForm
from .models import VetNote
from .forms import UserUpdateForm
from .models import Post, Comment
from django.db.models import Count
from .models import Appointment, VetNote, Pet
from .forms import  AppointmentForm
from .forms import  VetNoteForm
from django.db.models import Count, F, Avg




@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    pets = request.user.pets.all()
    friendships = Friendship.objects.filter(pet1__in=pets)
    return render(request, 'home.html', {'pets': pets, 'friendships': friendships})
    

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def pet_list(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_list.html', {'pets': pets})

@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'pet_form.html', {'form': form})

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'add_pet.html', {'form': form})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.like_count = post.likes.count()  
        if request.user.is_authenticated:
            post.user_has_liked = post.likes.filter(user=request.user).exists()
        else:
            post.user_has_liked = False
    return render(request, 'post_list.html', {'posts': posts})



@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = post.likes.filter(user=request.user).exists()

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post.id)
        elif 'like_submit' in request.POST:
            if not user_has_liked:
                Like.objects.create(user=request.user, post=post)
            else:
                post.likes.filter(user=request.user).delete()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'user_has_liked': user_has_liked,
        'like_count': post.likes.count(),
    })



def friendship_list(request):
    pets = request.user.pets.all()
    friendships = Friendship.objects.filter(pet1__in=pets)
    return render(request, 'friendship_list.html', {'friendships': friendships})

@login_required
def add_friendship(request):
    if request.method == 'POST':
        pet1_id = request.POST.get('pet1')
        pet2_id = request.POST.get('pet2')
        pet1 = get_object_or_404(Pet, id=pet1_id, owner=request.user)
        pet2 = get_object_or_404(Pet, id=pet2_id)

        if pet1 != pet2:
            Friendship.objects.get_or_create(pet1=pet1, pet2=pet2)
            

        return redirect('friendship_list')
    else:
        pets = request.user.pets.all()
        all_pets = Pet.objects.exclude(owner=request.user)
        return render(request, 'add_friendship.html', {'pets': pets, 'all_pets': all_pets})
    


@login_required
def message_list(request):
    
    messages_sent = Message.objects.filter(sender=request.user)
    messages_received = Message.objects.filter(receiver=request.user)
    all_messages = messages_sent.union(messages_received).order_by('sent_at')

    return render(request, 'message_list.html', {'messages': all_messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})    



@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    pets = user.pets.all()
    posts = user.posts.all()

    context = {
        'form': form,
        'pets': pets,
        'posts': posts,
    }
    return render(request, 'profile.html', context)


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == user_type:
            login(request, user)
            if user.user_type == 'Admin':
                return redirect('home')
            elif user.user_type == 'Veterinarian':
                return redirect('home')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password or user type')
            form = CustomLoginForm(request.POST)  
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

from django.contrib.auth import get_user_model
from .models import Pet, Post, Comment

User = get_user_model()

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'Admin':
        return HttpResponseForbidden("You don't have permission to access this page.")

    users = User.objects.all()
    pets = Pet.objects.all()
    posts = Post.objects.all()
    comments = Comment.objects.all()

    context = {
        'users': users,
        'pets': pets,
        'posts': posts,
        'comments': comments,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
def veterinarian_dashboard(request):
    if request.user.user_type != 'Veterinarian':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    
    pets = Pet.objects.all() 
    vet_notes = VetNote.objects.filter(veterinarian=request.user).order_by('-created_at')
    
    context = {
        'pets': pets,
        'vet_notes': vet_notes,
    }
    return render(request, 'veterinarian_dashboard.html', context)



@login_required
def login_redirect(request):
    user = request.user
    if user.user_type == 'Admin':
        return redirect('admin_dashboard')
    elif user.user_type == 'Veterinarian':
        return redirect('veterinarian_dashboard')
    else:
        return redirect('home')
    



@login_required
def user_update(request, user_id):
    if request.user.user_type != 'Admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserUpdateForm(instance=user_obj)
    
    return render(request, 'user_update.html', {'form': form, 'user_obj': user_obj})





@login_required
def admin_post_list(request):
    if request.user.user_type != 'Admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'admin_post_list.html', {'posts': posts})

@login_required
def admin_comment_list(request):
    if request.user.user_type != 'Admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'admin_comment_list.html', {'comments': comments})

@login_required
def admin_post_delete(request, post_id):
    if request.user.user_type != 'Admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('admin_post_list')

@login_required
def admin_comment_delete(request, comment_id):
    if request.user.user_type != 'Admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('admin_comment_list')


@login_required
def admin_statistics(request):
    if request.user.user_type != 'Admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    total_messages = Message.objects.count()

    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_messages': total_messages,
    }
    return render(request, 'admin_statistics.html', context)







def veterinarian_dashboard(request):
    if request.user.user_type != 'Veterinarian':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    pets = Pet.objects.filter(owner=request.user)
    appointments = Appointment.objects.filter(veterinarian=request.user).order_by('date')
    vet_notes = VetNote.objects.filter(veterinarian=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        if 'add_note' in request.POST:
            note_form = VetNoteForm(request.POST)
            if note_form.is_valid():
                new_note = note_form.save(commit=False)
                new_note.veterinarian = request.user
                new_note.save()
                messages.success(request, 'Note added successfully.')
                return redirect('veterinarian_dashboard')
        elif 'add_appointment' in request.POST:
            appointment_form = AppointmentForm(request.POST)
            if appointment_form.is_valid():
                new_appointment = appointment_form.save(commit=False)
                new_appointment.veterinarian = request.user
                new_appointment.save()
                messages.success(request, 'Appointment created successfully.')
                return redirect('veterinarian_dashboard')
    else:
        note_form = VetNoteForm()
        appointment_form = AppointmentForm()

    context = {
        'pets': pets,
        'appointments': appointments,
        'vet_notes': vet_notes,
        'note_form': note_form,
        'appointment_form': appointment_form,
    }
    return render(request, 'veterinarian_dashboard.html', context)





@login_required
def advanced_reports(request):
    
    user_id = 1
    total_posts = Post.objects.filter(user_id=user_id).count()

    
    top_vet_posts = (
        Post.objects.filter(user__user_type='Veterinarian')
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            engagement=F('likes_count') + F('comments_count')
        )
        .order_by('-engagement')[:5]
    )

    
    avg_age_labrador = Pet.objects.filter(breed='Labrador Retriever').aggregate(avg_age=Avg('age'))['avg_age']

    
    top_friends = (
        Friendship.objects.values('pet1')
        .annotate(friend_count=Count('pet2'))
        .order_by('-friend_count')[:5]
    )
    pet_ids = [entry['pet1'] for entry in top_friends]
    pets_with_friends = Pet.objects.filter(id__in=pet_ids)
    pet_friend_count = {entry['pet1']: entry['friend_count'] for entry in top_friends}

    
    city = request.GET.get('city', 'Istanbul')

    popular_pets = (
        Pet.objects.filter(owner__city=city)
        .annotate(friend_count=Count('friendships_initiated'))
        .order_by('-friend_count')[:5]
    )

    
    cities = User.objects.values_list('city', flat=True).distinct()

    context = {
        'total_posts': total_posts,
        'user_id': user_id,
        'top_vet_posts': top_vet_posts,
        'avg_age_labrador': avg_age_labrador,
        'pets_with_friends': pets_with_friends,
        'pet_friend_count': pet_friend_count,
        'popular_pets': popular_pets,
        'city': city,
        'cities': cities,
    }

    return render(request, 'advanced_reports.html', context)




