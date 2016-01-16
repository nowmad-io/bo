from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.tokens import default_token_generator
from djoser import utils, serializers, signals, settings

# Create your views here.
class RegistrationView(utils.SendEmailViewMixin, generics.CreateAPIView):
    """
    Use this endpoint to register new user.
    """
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator
    subject_template_name = 'activation_email_subject.txt'
    plain_body_template_name = 'activation_email_body.txt'

    def perform_create(self, serializer):
        instance = serializer.save()
        signals.user_registered.send(sender=self.__class__, user=instance, request=self.request)
        if settings.get('SEND_ACTIVATION_EMAIL'):
            self.send_email(**self.get_send_email_kwargs(instance))

    def get_email_context(self, user):
        context = super(RegistrationView, self).get_email_context(user)
        context['url'] = settings.get('ACTIVATION_URL').format(**context)
        print context
        return context
