from rest_framework import serializers
from .models import Author, Post


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_full_name")

    class Meta:
        model = Author
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    def get_tags(self, instance):
        return list(instance.tags.names())

    class Meta:
        model = Post

        fields = [
            "id",
            "author",
            "title_en",
            "title_ha",
            "thumbnail",
            "short_description_en",
            "short_description_ha",
            "tags",
            "slug",
            "created_on",
        ]


class PostRetriveSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    def get_tags(self, instance):
        return list(instance.tags.names())

    class Meta:
        model = Post
        fields = "__all__"
