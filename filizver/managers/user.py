# -*- coding: utf-8 -*-
from django.utils import timezone
from manifest.accounts.managers import BaseUserManager
from manifest.accounts.utils import generate_sha1

class UserManager(BaseUserManager):
    pass