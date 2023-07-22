from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .models import Post
from rest_framework.permissions import AllowAny
from .serializers import PostRetriveSerializer, PostListSerializer
from utils.mixins import SerializerByActionMixin


class PostViewSet(SerializerByActionMixin, GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Post.objects.all()
    serializer_map = {
        "list": PostListSerializer,
        "retrieve": PostRetriveSerializer,
    }
    permission_classes = [AllowAny]
    lookup_field = "slug"
