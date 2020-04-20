from django.views.generic import TemplateView, ListView, DetailView

from Insta.models import Post

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse, reverse_lazy

from Insta.forms import CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin



#HelloWorld is a TemplateView
#according to model view template graph, view needs both view and model
#need to import models, but not template bcs we already set its dir in settings.py

class HelloWorld(TemplateView):
    template_name = 'test.html'


#this will return self.object_list(models of post) to template(index.html)
class PostsView(ListView):
    model = Post
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    #if we use reverse, wrong bcs it tries to go to the url while deleting, not allowed
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

