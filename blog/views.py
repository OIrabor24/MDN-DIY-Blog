from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView
from .models import Blog, BlogComment, BlogAuthor
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
# Create your views here.
from django.urls import reverse

def index(request):
    """View function for homepage of site."""
    # Render the HTML template index.html
    num_blogs = Blog.objects.all().count() 
    num_authors = BlogAuthor.objects.all().count() 
    num_comments = BlogComment.objects.all().count() 
    num_bloggers = Blog.objects.all()

    context = { 
        'num_blogs': num_blogs,
        'num_authors': num_authors,
        'num_comments': num_comments,
        'num_bloggers': num_bloggers
    }


    return render(request, 'index.html', context=context)

class BlogListView(generic.ListView): # lists all blogs view html
    model = Blog 
    paginate_by = 5

class BlogDetailView(generic.DetailView): #Blog detail lists info about a specific blog post (description, date, author, comment etc.)
    model = Blog 
    paginate_by = 5


class BloggerListView(generic.ListView):  # detail view for listing all blogger users unordered html list
    """Generic class-based detail view for a blog."""
    model = BlogAuthor
    paginate_by = 5


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog comment. Requires login"""
    model = BlogComment
    fields = ['description'] 

    def get_context_data(self, **kwargs):
        """Add associated blog to form template so can display its title in HTML."""
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """Add author and associated blog to form data before setting it as valid (so it is saved to model)"""
        # Add logged-in user as author of comment
        form.instance.author = self.request.user 
        # Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk']) 
        # Call super-class form validation behavior 
        return super(BlogCommentCreate, self).form_valid(form) 

    def get_success_url(self):
        """After posting comment return to associated blog."""
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],}) 

class BlogListbyAuthorView(generic.ListView): # lists info related to a specific blogger user by pk (<int:pk>)
    model = BlogAuthor 
    paginate_by = 10
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        """Return list of Blog objects created by BlogAuthor (author id specified in URL)"""
        id = self.kwargs['pk']
        target_author= get_object_or_404(BlogAuthor, pk = id)
        return Blog.objects.filter(author=target_author) 

    def get_context_data(self, **kwargs):
        """Add BlogAuthor to context so they can be displayed in the template"""
        # Call the base implementation first to get a context
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return context

