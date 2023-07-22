from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
import os


User = get_user_model()


def make_author_image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split(".")[-1]
    filename = f"{instance.user.get_full_name()}.{ext}"
    return os.path.join("uploads/author/", filename)


def make_thumbnail_image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split(".")[-1]
    filename = f"{instance.title_en}.{ext}"
    return os.path.join("uploads/post/", filename)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    image = ResizedImageField(
        upload_to=make_author_image_file_path,
        size=[400, 400],
        quality=-1,
        scale=0.5,
        crop=["middle", "center"],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"


class Post(models.Model):
    title_en = models.CharField(max_length=150, blank=False, null=False, help_text="English Title")
    title_ha = models.CharField(max_length=150, blank=False, null=False, help_text="Hausa Title")
    short_description_en = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        help_text="English Short Description",
    )
    short_description_ha = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        help_text="Hausa Short Description",
    )
    thumbnail = ResizedImageField(
        upload_to=make_thumbnail_image_file_path,
        size=[1920, 1080],
        quality=-1,
        scale=0.5,
        crop=["middle", "center"],
        null=False,
        blank=False,
    )
    body_en = RichTextUploadingField(blank=False, config_name="default")
    body_ha = RichTextUploadingField(blank=False, config_name="default")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False, blank=False, related_name="post_author")
    tags = TaggableManager()
    slug = models.SlugField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_en)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
