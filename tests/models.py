from django.db import models
from django.contrib.auth.models import User
from .fields import OrderField
from django.utils.text import slugify



class Test(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(max_length=100,unique=True, blank=True)
    title = models.CharField(max_length=100,db_index=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    completed = models.PositiveIntegerField(default=0)
    len = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField(User,
                                        related_name='test_liked',
                                        blank=True)
    users_dislike = models.ManyToManyField(User,
                                           related_name='test_disliked',
                                           blank=True)
    results = models.ManyToManyField(User,
                                     through='Result',
                                     related_name='test_result',
                                     blank=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Test, self).save(*args, **kwargs)



class Page(models.Model):
    test = models.ForeignKey(
        Test,
        related_name='page',
        on_delete=models.CASCADE,
    )
    order = OrderField(blank=True, for_fields=['test'])
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    text = models.TextField()
    right_answer = models.CharField(max_length=10, blank=True)
    question_commentory = models.TextField(blank=True)


    class Meta:
        ordering = ['order']




class Question(models.Model):
    page = models.ForeignKey(
        Page,
        related_name='question',
        on_delete=models.CASCADE,
    )
    order = OrderField(blank=True, for_fields=['page'])
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


    class Meta:
        ordering = ['order']



class Result(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    test = models.ForeignKey(Test,
                             on_delete=models.CASCADE)
    result = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-result']