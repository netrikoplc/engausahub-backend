from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from .models import Contact
from django.core.mail import EmailMessage


class ContactViewSet(GenericViewSet, CreateModelMixin):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        first_name = self.request.data["first_name"]
        last_name = self.request.data["last_name"]
        email = self.request.data["email"]
        subject = self.request.data["subject"]
        message = self.request.data["message"]
        try:
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=email,
                to=["info@engausahub.com"],
            )
            email_message.send()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
