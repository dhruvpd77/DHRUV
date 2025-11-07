from django.db import models
from django.contrib.auth.models import User
from semesters.models import Subject, Question

class QuizAttempt(models.Model):
    QUIZ_MODE_CHOICES = [
        ('random', 'Random Mode'),
        ('practice_all', 'Practice All Mode'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.IntegerField()
    score = models.IntegerField()
    total_questions = models.IntegerField(default=10)
    quiz_mode = models.CharField(max_length=20, choices=QUIZ_MODE_CHOICES, default='random')
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.subject.name} - Unit {self.unit} - {self.score}/{self.total_questions}"
    
    class Meta:
        ordering = ['-attempted_at']

class QuizAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    is_correct = models.BooleanField()
    
    def __str__(self):
        return f"{self.quiz_attempt.user.username} - Question {self.question.id}"
    
    class Meta:
        ordering = ['id']
