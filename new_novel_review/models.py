from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Work(models.Model):
    title = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    def scene_count(self):
        return self.scene_set.count()
    def post_count(self):
        return self.post_set.filter(hide=False).count()
    def read_count(self):
        return self.read_set.count()
    def __str__(self):
        return self.title
    class Meta:
        constraints = [UniqueConstraint(fields=['title', 'creator'], name='unique_work')]

class Scene(models.Model):
    title = models.CharField(max_length=500)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def poll_count(self):
        return self.poll_set.count()

class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'scene'], name='unique_poll')]

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="media/post_images/")
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    hide = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.work} : {self.user.username}'
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'work'], name='unique_post')]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.post
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'post'], name='unique_like')]

class Read(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    def __str__(self):
        return self.work
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'work'], name='unique_read')]