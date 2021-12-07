from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile, Subject_grade, Subject, Teacher_subject
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class DateInput(forms.DateInput):
    input_type = 'date'

class NewGradeForm(forms.ModelForm):
    class Meta:
        widgets = {'date': DateInput()}
        model = Subject_grade
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewGradeForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['student'].queryset = User.objects.filter(user_type="S")



