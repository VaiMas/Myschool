from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('teachers/', views.TeachersListView.as_view(), name='teachers'),
    path('teachers/<int:teacher_id>', views.teacher, name='teacher'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mygrades/', views.GradesByUserListView.as_view(), name='my-grades'),
    path('mylessons/', views.LessonsByUserListView.as_view(), name='my-lessons'),
    path('mylessons/new', views.GradeByUserCreateView.as_view(), name='grade-new'),
    path('mylessons/<int:pk>/update', views.GradeByUserUpdateView.as_view(), name='grade-update'),
    path('mylessons/<int:pk>/delete', views.GradeByUserDelateView.as_view(), name='grade-delete'),
    path('profile/', views.profile, name='profile'),

]
