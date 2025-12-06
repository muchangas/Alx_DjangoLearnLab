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