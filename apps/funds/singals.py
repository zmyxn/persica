from django.db.models.signals import pre_save, post_save, post_init
from django.dispatch import receiver
from .models import CapitalFlow
from django.contrib import messages

