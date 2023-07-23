from rest_framework import serializers
from .models import Testimonials, FAQs


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = "__all__"
