from django.db import models
from django.db.models.fields import CharField, DateField
from datetime import date 
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User #Blog author or commenter

# Create your models here.
class BlogAuthor(models.Model):
    """Model represents a Blogger"""
    # Fields
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True) 
    bio = models.TextField(max_length=400, help_text='Enter your bio details here.')
    
    # Metadata
    class Meta:
        ordering = ['user', 'bio'] 

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Blog Author"""
        return reverse('blogs-by-author', args=[str(self.id)]) 

    def __str__(self):
        """String for representing the Model object (in the admin site etc.)"""
        return self.user.username 
        
    
class Blog(models.Model):
    """Model represents a Blog post"""
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True) 
    description = models.TextField(max_length=2000, help_text='Enter your blog text here.')
    post_date = models.DateField(default=date.today) 

# Metadata
    class Meta:
        ordering = ['-post_date']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of a Blog """
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Blog object (in the admin site etc.)"""
        return self.name 

class BlogComment(models.Model):
    """Model represents a Blog comment"""
    description = models.TextField(max_length=1000, help_text='Enter your comment here.')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    # Foreign Key used because BlogComment can only have one author/User, but users can have multiple comments 
    post_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE) 

# Metadata
    class Meta:
        ordering = ['post_date']

    def __str__(self):
        """String for representing the Blog Comment object (in the admin site etc.)"""
        len_title = 75 
        if len(self.description) > len_title:
            titlestring=self.description[:len_title] + '...'
        else:
            titlestring=self.description
        return titlestring 










