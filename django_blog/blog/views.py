from django.shortcuts import render, redirect 
# from .models import Post # Uncomment once you start querying the DB
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileEditForm
from .models import Post # Keep this import if it exists

def post_list(request):
    """Placeholder view to render the home page template."""
    # posts = Post.objects.all() # Example of fetching data
    context = {}
    return render(request, 'blog/post_list.html', context)

# New Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Log the user in immediately after registration
            # login(request, user) 
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

# New Profile Management View (Requires Login)
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # Pass the current user instance to pre-populate the form
        form = UserProfileEditForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'blog/profile.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

from .forms import CustomUserCreationForm, UserProfileEditForm
from .models import Post

# --- Function-Based Views (Keep existing) ---

def post_list_old(request): # Renamed the old function view to avoid conflict with ListView
    # posts = Post.objects.all()
    context = {}
    return render(request, 'blog/post_list.html', context)

# ... (Keep register and profile views) ...


# --- Class-Based Views (New CRUD Implementation) ---

class PostListView(ListView):
    """Displays a list of all published blog posts."""
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-published_date'] # Orders posts from newest to oldest
    paginate_by = 5

class PostDetailView(DetailView):
    """Displays the full content of a single blog post."""
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create a new post."""
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        # Automatically set the author to the currently logged-in user
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the post author to edit their existing post."""
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # Ensures the author remains the current logged-in user (though it shouldn't change)
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)

    def test_func(self):
        """Mixin check: Ensures the logged-in user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the post author to delete their post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    # Use reverse_lazy because the URL may not be loaded when this file is executed
    success_url = reverse_lazy('post_list') 

    def test_func(self):
        """Mixin check: Ensures the logged-in user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author