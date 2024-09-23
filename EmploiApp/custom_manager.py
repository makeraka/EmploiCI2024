from django.db import models

class ProfDispoWeekManagerActivation(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(busy=False)
