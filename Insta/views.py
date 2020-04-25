from django.views.generic import TemplateView, ListView, DetailView

from annoying.decorators import ajax_request

from Insta.models import Post, Like, InstaUser, UserConnection

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse, reverse_lazy

from Insta.forms import CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin



#HelloWorld is a TemplateView
#according to model view template graph, view needs both view and model
#need to import models, but not template bcs we already set its dir in settings.py

class HelloWorld(TemplateView):
    template_name = 'test.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'

#this will return self.object_list(models of post) to template(index.html)
class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    #override default get_queryset so that not all posts are returned
    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)


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

#different from above, not class based view
#this means this function exist to respond to ajax request, that's why it don't need to render to a template
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    print(post_pk)
    post = Post.objects.get(pk=post_pk)

    try:
        like = Like(post=post, user=request.user)
        #save to database, will have exception if this user already liked the post (bcz we set unique-together in models.py)
        like.save()
        result = 1

    except Exception as e:
        #handle exception, which means remove like
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        #result 0 or 1 tells if it's remove like or add like
        result = 0

    #ajax return type is json, return to index.js
    return {
        'result': result,
        'post_pk': post_pk
    }

