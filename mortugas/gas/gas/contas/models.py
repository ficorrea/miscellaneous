import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin, UserManager)
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Login', max_length=30, unique=True,
                                validators=[validators.RegexValidator(
                                    re.compile('^[\w]'), 'invalid')]
                                )
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Login', max_length=100)
    is_active = models.BooleanField('Ativo?', default=True)
    is_staff = models.BooleanField('Administrador?', default=False)
    date_joined = models.DateTimeField('Data de criação', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)


class PasswordReset(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='Usuário', related_name='resets')
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.created_at)

    class Meta:
        ordering = ['-created_at']
