from django.shortcuts import render, get_object_or_404
from api.models import Post

def home(request):
  # Get all published posts (ordered by published date descending)
  posts = Post.objects.all().order_by('-published')
  context = {'posts': posts}  # Add posts to the context dictionary
  return render(request, 'home.html', context)

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)
  context = {'post': post}
  return render(request, 'post_detail.html', context)