from django.contrib import admin
from .models import Author, Post
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


def get_thumbnail_preview(obj):
    if obj.pk:  # if object has already been saved and has a primary key, show picture preview
        return mark_safe(
            """<img src="{src}" alt="{title}" width="100%" height="auto" style="max-width:400px" />""".format(
                src=obj.thumbnail.url,
                title=obj.title_en,
            )
        )
    return _("(choose a thumbnail and save and continue editing to see the preview)")


get_thumbnail_preview.allow_tags = True
get_thumbnail_preview.short_description = _("Thumbnail Preview")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "image")
    search_fields = ("user",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title_en", "author", "created_on", "last_updated_on")
    search_fields = ("title_en", "author", "created_on", "last_updated_on")
    readonly_fields = (
        "slug",
        "created_on",
        "last_updated_on",
        get_thumbnail_preview,
    )
    fields = (
        "title_en",
        "title_ha",
        "thumbnail",
        get_thumbnail_preview,
        "short_description_en",
        "short_description_ha",
        "body_en",
        "body_ha",
        "author",
        "tags",
        "slug",
        "created_on",
        "last_updated_on",
    )
