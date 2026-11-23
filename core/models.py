from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, blank=True)


class Goal(models.Model):
    CATEGORY_CHOICES = [
        ('ACADEMIC', 'Academic'),
        ('FITNESS', 'Fitness & Health'),
        ('WORK', 'Work & Career'),
        ('PERSONAL', 'Personal Growth'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('PAUSED', 'Paused'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='PERSONAL')
    target_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['target_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Routine(models.Model):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKDAYS', 'Weekdays (Mon–Fri)'),
        ('WEEKENDS', 'Weekends'),
        ('WEEKLY', 'Weekly'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='routines'
    )
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name='routines'
    )
    title = models.CharField(max_length=150)
    frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES, default='DAILY')
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} - {self.goal.title}"
