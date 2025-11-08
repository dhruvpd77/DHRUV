from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.select_semester, name='select_semester'),
    path('semester/<int:semester_id>/', views.select_subject, name='select_subject'),
    path('subject/<int:subject_id>/disclaimer/', views.disclaimer, name='disclaimer'),
    path('subject/<int:subject_id>/units/', views.select_unit, name='select_unit'),
    path('subject/<int:subject_id>/unit/<int:unit>/mode/', views.select_quiz_mode, name='select_mode'),
    path('subject/<int:subject_id>/unit/<int:unit>/quiz/', views.take_quiz, name='take_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('about/', views.about_us, name='about_us'),
]

