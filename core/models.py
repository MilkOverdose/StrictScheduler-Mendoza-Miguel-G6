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



class Schedule(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    scheduled_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_date', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.scheduled_date})"