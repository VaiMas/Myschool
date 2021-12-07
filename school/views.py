from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserUpdateForm, ProfileUpdateForm, NewGradeForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Subject_grade, CustomUser, Subject, Teacher_subject
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext as _
from django.db.models import Avg


User = get_user_model()


def index(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _(f"Profile updated"))
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


class TeachersListView(generic.ListView):
    model = User
    template_name = 'teachers.html'
    context_object_name = 'teachers_list'
    paginate_by = 5
    queryset = User.objects.filter(user_type='T')

def teacher(request, teacher_id):
    single_teacher = get_object_or_404(User.objects.filter(user_type='T'), pk=teacher_id)
    return render(request, 'teacher.html', {'teacher': single_teacher})


def search(request):
    query = request.GET.get('query')
    search_results = User.objects.filter(Q(fname__icontains=query) | Q(lname__icontains=query))
    return render(request, 'search.html', {'users': search_results, 'query': query})


class GradesByUserListView(LoginRequiredMixin, generic.ListView):
    model = Subject_grade
    template_name = 'user_grades.html'
    paginate_by = 2

    def get_queryset(self):
        return Subject_grade.objects.filter(student=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(GradesByUserListView, self).get_context_data(**kwargs)
        context['average'] = Subject_grade.objects.all().aggregate(Avg('grade'))
        return context


class GradeByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Subject_grade
    success_url = "/school/mylessons/"
    template_name = 'new_grade.html'
    form_class = NewGradeForm

class GradeByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Subject_grade
    success_url = "/school/mylessons/"
    template_name = 'edit_grade.html'
    form_class = NewGradeForm

    def test_func(self):
        return self.request.user

class GradeByUserDelateView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Subject_grade
    success_url = "/school/mylessons/"
    template_name = 'delete_grade.html'

    def test_func(self):
        return self.request.user

from collections import defaultdict

class LessonsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Subject_grade
    template_name = 'user_lessons.html'
    paginate_by = 5

