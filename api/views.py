from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from api.models import Post
from api.forms import RegistrationForm


def home(request):
  # Get all published posts (ordered by published date descending)
  posts = Post.objects.all().order_by('-published')
  context = {'posts': posts}  # Add posts to the context dictionary
  return render(request, 'home.html', context)

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)
  context = {'post': post, 'author_first_name': post.author.first_name, 'author_last_name': post.author.last_name}
  return render(request, 'post_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin:login')  # Redirect to Django admin login
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})