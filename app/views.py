from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from .forms import ProfileForm, RegisterForm, PostForm

# Landing Page
def landing(request):
    return render(request, 'app/landing.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'app/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)

        # ✅ Create profile at registration
        Profile.objects.get_or_create(user=user)

        login(request, user)
        return redirect('home')

    return render(request, 'app/register.html')


from .models import Profile

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Ensure profile exists (IMPORTANT FIX)
            profile, created = Profile.objects.get_or_create(user=user)

            login(request, user)
            return redirect('home')
        else:
            return render(request, 'app/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'app/login.html')


def user_logout(request):
    logout(request)
    return redirect('landing')


@login_required
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'app/home.html', {
        'posts': posts
    })


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('profile', request.user.username)
    return render(request, 'app/create_post.html', {'form': form})


@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('home')


@login_required
def comment_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        Comment.objects.create(
            post=post,
            user=request.user,
            text=request.POST['text']
        )

    return redirect('home')


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    posts = user.posts.all()

    if request.method == "POST":
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)

    return render(request, 'app/profile.html', {
        'profile': profile,
        'posts': posts
    })
@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if form.is_valid():
        form.save()
        return redirect('profile', request.user.username)

    return render(request, 'app/edit_profile.html', {'form': form})
@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.user:
        return redirect('home')

    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('profile', request.user.username)

    return render(request, 'app/create_post.html', {'form': form})