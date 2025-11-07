from django.contrib import admin
from .models import Semester, Subject, Question

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'semester', 'created_at']
    list_filter = ['semester']
    search_fields = ['name', 'code']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'unit', 'correct_answer', 'added_by', 'verified_by']
    list_filter = ['subject', 'unit', 'correct_answer']
    search_fields = ['question_text', 'added_by', 'verified_by']
