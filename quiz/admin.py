from django.contrib import admin
from .models import QuizAttempt, QuizAnswer

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'unit', 'score', 'total_questions', 'attempted_at']
    list_filter = ['subject', 'unit', 'attempted_at']
    search_fields = ['user__username', 'subject__name']

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempt', 'question', 'selected_answer', 'is_correct']
    list_filter = ['is_correct']
