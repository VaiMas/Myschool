from django.contrib import admin
# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Subject, Subject_grade, Profile, Teacher_subject
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','fname','lname', 'is_staff', 'user_type')
    list_filter = ('email','fname','lname', 'is_staff', 'user_type')
    fieldsets = (
        (None, {'fields': ('email','fname','lname', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'user_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','fname','lname', 'password1', 'password2', 'is_staff', 'user_type')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Subject)
admin.site.register(Teacher_subject)
admin.site.register(Subject_grade)

admin.site.register(Profile)

