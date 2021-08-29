import time

from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from authors.models import Author
from modules import validate_img_extension


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now=True)
    icon = models.CharField(default="pi-angle-double-right", max_length=30,
                            help_text="Icons can be picked from https://www.primefaces.org/primevue/showcase-v2/#/icons")

    def __str__(self):
        return self.sub_category_name

    @property
    def total_blogs(self):
        return Blog.objects.filter(sub_category=self).count()


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    sub_category = models.ManyToManyField(SubCategory, blank=True, )
    added_on = models.DateTimeField(auto_now=True)
    icon = models.CharField(default="pi-angle-double-right", max_length=30,
                            help_text="Icons can be picked from https://www.primefaces.org/primevue/showcase-v2/#/icons")

    def __str__(self) -> str:
        return self.category_name

    @property
    def total_blogs(self):
        return Blog.objects.filter(category=self).count()


# Create your models here.
class Blog(models.Model):
    """
        Blog table
    """
    colors = [("r", "danger"), ("s", "success"),
              ("i", "info"), ]
    title = models.CharField(
        max_length=250, help_text="Unique, catchy topic of the article", unique=True, null=True, blank=True)
    body = CKEditor5Field(
        'Add a body', help_text="Full body of the article, supports markup", config_name='default', null=True,
        blank=True)
    introductory_file = models.ImageField(
        upload_to="blog_intros", null=True, blank=True, help_text="Cover image to introduce the rest of the blog",
        validators=[validate_image_file_extension, validate_img_extension])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    blog_color = models.CharField(
        choices=colors, null=True, blank=True, max_length=10)
    posted_on = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(
        User, blank=True, related_name="upvoters")
    downvotes = models.ManyToManyField(
        User, blank=True, related_name="downvoters")
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ManyToManyField(Category, verbose_name="category")
    sub_category = models.ManyToManyField(
        SubCategory, blank=True, verbose_name="subCategory")
    schedule_to = models.DateField(
        null=True, help_text="If you are want to schedule the blog to a future date.", blank=True)
    contributors = models.ManyToManyField(
        Author, blank=True, related_name="coauthors")

    def __str__(self):
        return self.title

    @property
    def total_upvotes(self):
        return self.upvotes.count()

    @property
    def total_downvotes(self):
        return self.downvotes.count()

    @property
    def total_comments(self):
        return BlogComment.objects.filter(comment_to=self).count()


class BlogComment(models.Model):
    comment_to = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_body = models.TextField()
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="commentLikes")

    def __str__(self):
        return self.comment_to.title

    @property
    def total_replies(self):
        return CommentReply.objects.filter(reply_to=self).count()


class CommentReply(models.Model):
    reply_to = models.ForeignKey(BlogComment, on_delete=models.CASCADE)
    reply_body = models.TextField()
    reply_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="replyLikes")

    def __str__(self):
        return self.reply_to.comment_to.title


class Notification(models.Model):
    """
        Notifications to a specific user or to general users
    """
    to = models.ManyToManyField(
        User, related_name="receiver")
    title = models.CharField(max_length=100)
    is_general = models.BooleanField(default=True)
    icon = models.CharField(max_length=60, blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, help_text="The current logged in admin")
    body = CKEditor5Field(
        'Notification body', config_name='extends', null=True, blank=True)
    notified_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.to.username


class Subscribers(models.Model):
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

    """
        User subscription, can be to a specific author, Category, whole blog
        Can be for just a month, six, one year or forever!

        Same as following

    """
    email = models.EmailField()

    def __str__(self):
        return self.email


class Bookmark(models.Model):
    """
        User's saved articles
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    bookmarked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ReadArticles(models.Model):
    """
        The articles the user has opened in a certain time
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    read_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# signals
@receiver(pre_save, sender=Blog)
def pre_save_gallery_receiver(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title[:30] +
                            '-' + str(time.time()))
