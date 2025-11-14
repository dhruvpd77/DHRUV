from django.urls import path
from . import views

app_name = 'semesters'

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create-semester/', views.create_semester, name='create_semester'),
    path('admin/edit-semester/<int:semester_id>/', views.edit_semester, name='edit_semester'),
    path('admin/delete-semester/<int:semester_id>/', views.delete_semester, name='delete_semester'),
    path('admin/create-subject/', views.create_subject, name='create_subject'),
    path('admin/edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('admin/delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('admin/upload-questions/', views.upload_questions, name='upload_questions'),
    path('admin/manage-semesters/', views.manage_semesters, name='manage_semesters'),
    path('admin/manage-subjects/<int:semester_id>/', views.manage_subjects, name='manage_subjects'),
    path('admin/manage-questions/<int:subject_id>/', views.manage_questions, name='manage_questions'),
    path('admin/add-question/<int:subject_id>/', views.add_question, name='add_question'),
    path('admin/edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('admin/delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('admin/delete-unit-questions/<int:subject_id>/<int:unit>/', views.delete_unit_questions, name='delete_unit_questions'),
    path('admin/delete-all-questions/<int:subject_id>/', views.delete_all_questions, name='delete_all_questions'),
    path('admin/manage-units/<int:subject_id>/', views.manage_units, name='manage_units'),
    path('admin/edit-unit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
    path('admin/create-unit/<int:subject_id>/<int:unit_number>/', views.create_unit, name='create_unit'),
]

