from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from PIL import Image
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    fname = models.CharField(verbose_name=_("First name"), max_length=150, null=True, blank=True)
    lname = models.CharField(verbose_name=_("Last name"), max_length=150, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USER_CHOICES = [
        ('T', 'Teacher'),
        ('S', 'Student')
    ]

    user_type = models.CharField(choices=USER_CHOICES, max_length=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def is_teacher(self):
        if self.user_type == 'T':
            return True
        else:
            return False


    def is_student(self):
        if self.user_type == 'S':
            return True
        else:
            return False

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"{self.fname} {self.lname} {self.email}"


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png",upload_to="profile_pics")

    def __str__(self):
        return f"{self.user} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.photo.path)

# Create your models here.
class Subject(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

class Teacher_subject(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='subjects')
    subject = models.ForeignKey('Subject', verbose_name='Subject', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Teacher's subject"
        verbose_name_plural = "Teacher's subjects"

    def __str__(self):
        return f' {self.teacher.fname} {self.teacher.lname} {self.subject.name}'


class Subject_grade(models.Model):
    teacher_subject = models.ForeignKey('Teacher_subject', verbose_name=_('Teacher subject'), on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(verbose_name=_('Date'), null=True, blank=True)

    GRADE = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    grade = models.IntegerField(
        verbose_name=_('Grade'),
        choices=GRADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.student.fname} {self.student.lname}  {self.grade} {self.date}"

    class Meta:
        verbose_name = "Subject grade"
        verbose_name_plural = 'Subject grades'
        ordering = ['-date']














