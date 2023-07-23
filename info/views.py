from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import Testimonials, FAQs
from .serializers import TestimonialSerializer, FAQSerializer
from rest_framework.permissions import AllowAny


class TestimonialViewSet(GenericViewSet, ListModelMixin):
    queryset = Testimonials.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]


class FAQViewSet(GenericViewSet, ListModelMixin):
    queryset = FAQs.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
