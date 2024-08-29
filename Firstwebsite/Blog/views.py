from django.shortcuts import render, get_object_or_404
from .models import Posts
from Users.models import Profile
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(ListView):
    model = Posts
    template_name = 'Blog/homepage.html'
    context_object_name = 'posts'
    ordering = '-date_published'
    paginate_by = 5
    
    
class UserPostListView(ListView):
    model = Posts
    template_name = 'Blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username') )
        return Posts.objects.filter(author = user).order_by("-date_published")
        
    
class PostDetailView(DetailView):
    model = Posts
    
    
class PostCreateView(CreateView):
    model = Posts
    
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user : return True
        return False
    
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = "/"
        
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user : return True
        return False
        


def about(request):
    return render(request, 'Blog/about.html', {'title': 'About Page'})
