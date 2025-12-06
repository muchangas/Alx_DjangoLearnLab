from django.shortcuts import render
# from .models import Post # Uncomment once you start querying the DB

def post_list(request):
    """Placeholder view to render the home page template."""
    # posts = Post.objects.all() # Example of fetching data
    context = {}
    return render(request, 'blog/post_list.html', context)