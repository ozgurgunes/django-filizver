# -*- coding: utf-8 -*-
import re
import datetime
from mongoengine import *
from mongoengine.django.auth import User as BaseUser
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class ActivationMixin(object):
    """
    A mixin that adds the field and methods necessary to support
    account activation and email confirmation.
    """
    activation_key = StringField(max_length=40)

    email_unconfirmed = EmailField(max_length=100, 
                            verbose_name=_(u'Unconfirmed email address'),
                            help_text=_(u'Temporary email address when the '
                                'user requests an email change.'))

    email_confirmation_key = StringField(max_length=40, 
                                verbose_name= _(u'Unconfirmed email verification key'))

    email_confirmation_key_created = DateTimeField(verbose_name = _(u'Creation date '
                                                'of email confirmation key'))

    def change_email(self, email):
        """
        Changes the email address for a user.

        A user needs to verify this new email address before it becomes
        active. By storing the new email address in a temporary field 
        -- ``temporary_email`` -- we are able to set this email address 
        after the user has verified it by clicking on the verification URI 
        in the email. This email gets send out by ``send_verification_email``.

        :param email:
            The new email address that the user wants to use.

        """
        self.email_unconfirmed = email

        salt, hash = generate_sha1(self.username)
        self.email_confirmation_key = hash
        self.email_confirmation_key_created = get_datetime_now()
        self.save()

        # Send email for activation
        self.send_confirmation_email()
        
        return self

    def send_confirmation_email(self):
        """
        Sends an email to confirm the new email address.

        This method sends out two emails. One to the new email address that
        contains the ``email_confirmation_key`` which is used to verify this
        this email address with :func:`User.objects.confirm_email`.

        The other email is to the old email address to let the user know that
        a request is made to change this email address.

        """
        context= {'user': self,
                  'new_email': self.email_unconfirmed,
                  'protocol': get_protocol(),
                  'confirmation_key': self.email_confirmation_key,
                  'site': Site.objects.get_current()}


        # Email to the old address
        subject_old = ''.join(render_to_string(
                        'accounts/emails/confirmation_email_subject_old.txt',
                        context).splitlines())
        
        message_old = render_to_string(
                        'accounts/emails/confirmation_email_message_old.txt',
                        context)

        send_mail(subject_old,
                  message_old,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.email])

        # Email to the new address
        subject_new = ''.join(render_to_string(
                        'accounts/emails/confirmation_email_subject_new.txt',
                        context).splitlines())

        message_new = render_to_string(
                        'accounts/emails/confirmation_email_message_new.txt',
                        context)

        send_mail(subject_new,
                  message_new,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.email_unconfirmed,])

    def activation_key_expired(self):
        """
        Checks if activation key is expired.

        Returns ``True`` when the ``activation_key`` of the user is expired 
        and ``False`` if the key is still valid.

        The key is expired when it's set to the value defined in
        ``ACCOUNTS_ACTIVATED`` or ``activation_key_created`` is beyond the
        amount of days defined in ``ACCOUNTS_ACTIVATION_DAYS``.

        """
        expiration_days = datetime.timedelta(
                            days=accounts_settings.ACCOUNTS_ACTIVATION_DAYS)
        expiration_date = self.date_joined + expiration_days
        if self.activation_key == accounts_settings.ACCOUNTS_ACTIVATED:
            return True
        if get_datetime_now() >= expiration_date:
            return True
        return False

    def send_activation_email(self):
        """
        Sends a activation email to the user.

        This email is send when the user wants to activate their 
        newly created user.

        """
        context= {'user': self,
                  'protocol': get_protocol(),
                  'activation_days': accounts_settings.ACCOUNTS_ACTIVATION_DAYS,
                  'activation_key': self.activation_key,
                  'site': Site.objects.get_current()}

        subject = ''.join(render_to_string(
                    'accounts/emails/activation_email_subject.txt',
                    context).splitlines())

        message = render_to_string(
                    'accounts/emails/activation_email_message.txt',
                    context)
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.email,])
                  
    @classmethod                  
    def create_user(cls, username, email, password, active=False,
                    send_email=True):
        """
        A simple wrapper that creates a new :class:`User`.

        :param username:
            String containing the username of the new user.

        :param email:
            String containing the email address of the new user.

        :param password:
            String containing the password for the new user.

        :param active:
            Boolean that defines if the user requires activation by clicking 
            on a link in an email. Defauts to ``True``.

        :param send_email:
            Boolean that defines if the user should be send an email. You 
            could set this to ``False`` when you want to create a user in 
            your own code, but don't want the user to activate through email.

        :return: :class:`User` instance representing the new user.

        """

        user = cls(username, email, password)

        if isinstance(user.username, unicode):
            username = user.username.encode('utf-8')
        salt, activation_key = generate_sha1(username)
        user.is_active = active
        user.activation_key = activation_key
        user.save()

        if send_email:
            user.send_activation_email()
 
        return user

    @classmethod                  
    def activate_user(cls, username, activation_key):
        """
        Activate an :class:`User` by supplying a valid ``activation_key``.

        If the key is valid and an user is found, activates the user and
        return it. Also sends the ``activation_complete`` signal.

        :param activation_key:
            String containing the secret SHA1 for a valid activation.

        :return:
            The newly activated :class:`User` or ``False`` if not successful.

        """
        if SHA1_RE.search(activation_key):
            try:
                user = cls.get(activation_key=activation_key)
            except cls.DoesNotExist:
                return False
            if not user.activation_key_expired():
                user.activation_key = accounts_settings.ACCOUNTS_ACTIVATED
                user.is_active = True
                user.save()
                # Send the activation_complete signal
                accounts_signals.activation_complete.send(sender=None, 
                    user=user)
                return user
        return False

    @classmethod                  
    def confirm_email(cls, username, confirmation_key):
        """
        Confirm an email address by checking a ``confirmation_key``.

        A valid ``confirmation_key`` will set the newly wanted email address
        as the current email address. Returns the user after success or
        ``False`` when the confirmation key is invalid.

        :param confirmation_key:
            String containing the secret SHA1 that is used for verification.

        :return:
            The verified :class:`User` or ``False`` if not successful.

        """
        if SHA1_RE.search(confirmation_key):
            try:
                user = cls.select_related().get(username=username,
                                    email_confirmation_key=confirmation_key,
                                    email_unconfirmed__isnull=False)
            except cls.DoesNotExist:
                return False
            else:
                user.email = user.email_unconfirmed
                user.email_unconfirmed, user.email_confirmation_key = '',''
                user.save()
                # Send the confirmation_complete signal
                accounts_signals.confirmation_complete.send(sender=None, 
                    user=user)
                return user
        return False

    @classmethod                  
    def delete_expired_users(cls):
        """
        Checks for expired users and delete's the ``User`` associated with
        it. Skips if the user ``is_staff``.

        :return: A list containing the deleted users.

        """
        deleted_users = []
        for user in cls.filter(is_staff=False, is_active=False):
            if user.activation_key_expired():
                deleted_users.append(user)
                user.delete()
        return deleted_users    


class ProfileMixin(object):

    GENDER_CHOICES = (
        ('F', _(u'Female')),
        ('M', _(u'Male')),
    )
    
    gender          = StringField(max_length=1, choices=GENDER_CHOICES)
    birth_date      = DateField()
    picture         = ImageField()
    about           = StringField()

    education       = StringField(max_length=128)
    occupation      = StringField(max_length=64)
    location        = StringField(max_length=64)

    website         = URLField()
    mobile          = StringField()
    country         = StringField()    


class User(BaseUser, ActivationMixin):
    timezone = StringField(max_length=100)
    locale = StringField(max_length = 10,
                                    choices = settings.LANGUAGES,
                                    default = settings.LANGUAGE_CODE)

