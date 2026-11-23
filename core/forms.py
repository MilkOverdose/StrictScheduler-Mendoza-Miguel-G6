from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils import timezone
from .models import Schedule

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'contact_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_number']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['title', 'description', 'scheduled_date', 'start_time', 'end_time', 'priority', 'status']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        scheduled_date = cleaned_data.get('scheduled_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if scheduled_date and scheduled_date < timezone.localdate():
            self.add_error('scheduled_date', "Scheduled date cannot be in the past.")

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', "End time must be after start time.")

        return cleaned_data