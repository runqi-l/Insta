from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.


#After creating this model, should remember to migrate, otherwise database is wrong
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to='static/image/profiles',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True
    )
    def get_connections(self):
        #.get can only get one, so we use filter
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    #check if self is followed by this user
    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()



class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='my_posts'
    )
    title = models.TextField(blank=True, null=True) #no title or blank is fine
    image = ProcessedImageField(
        upload_to='static/image/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

    def get_like_count(self):
        return self.likes.count()


#record A(creator) follows B
class UserConnection(models.Model):
    #editable false means this created is immutable field
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username


#link model, link instauser and post
class Like(models.Model):
    #this post, is a foreign key point to Post model
    post = models.ForeignKey(
        Post,
        # if one post is deleted, likes on this post get deleted too
        on_delete=models.CASCADE,

        # we can use post1.likes to get list of like relationship(A like post1, B like post1)
        related_name='likes'
    )

    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        #A.likes can find all likes clicked by A, also list of like relationship, but only A like xxx
        related_name='likes'
    )

    class Meta:
        # A like post1 cannot be duplicate, this combination(user, post) is unqiue
        unique_together = ("post", "user");

    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title
