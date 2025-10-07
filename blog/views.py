from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Project, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PostForm, CommentForm, TestimonialForm, Testimonial, CustomUserCreationForm, ProjectForm
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')[:2]
    latest_projects = Project.objects.order_by('-created_at')[:3]
    return render(request, 'blog/home.html', {'posts': posts, 'latest_projects': latest_projects})

@staff_member_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            return redirect('post_detail', slug=p.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_list(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    return render(request, "blog/post_list.html", {"posts": posts})

def projects_list(request):
    projects = Project.objects.order_by('-created_at')
    return render(request, 'blog/projects_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, id=pk)
    return render(request, 'blog/project_detail.html', {'project': project})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by('-created_at')

    if request.user.is_authenticated:  # ✅ Only allow logged in users to post
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                c = form.save(commit=False)
                c.post = post
                c.author_name = request.user.username  # use logged-in username
                c.save()
                return redirect('post_detail', slug=post.slug)
        else:
            form = CommentForm()
    else:
        form = None  # not logged in → no form

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@staff_member_required
@user_passes_test(lambda u: u.is_staff)  # Only staff (admins) can access
def project_create(request):
    """
    Add a new project (title, description, url, screenshot).
    Visible only to logged-in users.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects_list')
    else:
        form = ProjectForm()
    return render(request, 'blog/project_form.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})

def testimonials(request):
    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')  # only approved
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.approved = False  # submitted but not visible
            testimonial.save()
            return redirect('testimonials')
    else:
        form = TestimonialForm()
    return render(request, "blog/testimonials.html", {"form": form, "testimonials": testimonials})
