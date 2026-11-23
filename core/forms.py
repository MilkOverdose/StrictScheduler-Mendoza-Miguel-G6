from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils import timezone
from .models import Goal, Routine

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'contact_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_number']
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'category', 'target_date', 'status']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_target_date(self):
        target_date = self.cleaned_data.get('target_date')
        if target_date and target_date < timezone.localdate():
            raise forms.ValidationError("Target date cannot be in the past.")
        return target_date


class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['goal', 'title', 'frequency', 'start_time', 'end_time', 'notes', 'is_active']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Ensure users only pick from their own goals
        if user is not None:
            self.fields['goal'].queryset = Goal.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', "End time must be after start time.")
        return cleaned_data