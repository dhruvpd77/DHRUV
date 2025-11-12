from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from .models import UserLogin
from quiz.models import QuizAttempt

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:select_semester')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Track initial login time
            UserLogin.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Account created successfully!')
            return redirect('quiz:select_semester')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:select_semester')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Track login time
                UserLogin.objects.create(
                    user=user,
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                messages.success(request, f'Welcome back, {username}!')
                return redirect('quiz:select_semester')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    from quiz.models import QuizAttempt
    quiz_history = QuizAttempt.objects.filter(user=request.user).select_related('subject')
    
    # Calculate average score percentage
    average_percentage = 0
    if quiz_history.exists():
        total_percentage = 0
        for attempt in quiz_history:
            percentage = (attempt.score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
            total_percentage += percentage
        average_percentage = round(total_percentage / quiz_history.count())
    
    # Get best score
    best_score = quiz_history.order_by('-score').first() if quiz_history.exists() else None
    
    context = {
        'quiz_history': quiz_history,
        'average_percentage': average_percentage,
        'best_score': best_score,
    }
    return render(request, 'accounts/profile.html', context)

@staff_member_required
def admin_user_management(request):
    """Admin dashboard for user management and tracking"""
    # Get all users with statistics
    users = User.objects.annotate(
        login_count=Count('login_history'),
        quiz_attempts_count=Count('quiz_attempts'),
        total_score=Sum('quiz_attempts__score'),
        total_questions=Sum('quiz_attempts__total_questions')
    ).order_by('-date_joined')
    
    # Overall statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_logins = UserLogin.objects.count()
    total_quiz_attempts = QuizAttempt.objects.count()
    
    # Recent logins (last 10)
    recent_logins = UserLogin.objects.select_related('user').order_by('-login_time')[:10]
    
    # Top performers
    top_performers = []
    for user in users:
        if user.quiz_attempts_count > 0 and user.total_questions and user.total_questions > 0:
            avg_score = (user.total_score / user.total_questions) * 100
            top_performers.append({
                'user': user,
                'avg_score': round(avg_score, 1),
                'attempts': user.quiz_attempts_count
            })
    
    top_performers = sorted(top_performers, key=lambda x: x['avg_score'], reverse=True)[:10]
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'total_logins': total_logins,
        'total_quiz_attempts': total_quiz_attempts,
        'recent_logins': recent_logins,
        'top_performers': top_performers,
    }
    return render(request, 'accounts/admin_user_management.html', context)

@staff_member_required
def admin_user_detail(request, user_id):
    """Detailed view of a specific user"""
    user = get_object_or_404(User, id=user_id)
    
    # Login history
    login_history = UserLogin.objects.filter(user=user).order_by('-login_time')
    total_logins = login_history.count()
    last_login_obj = login_history.first()
    
    # Quiz attempts
    quiz_attempts = QuizAttempt.objects.filter(user=user).select_related('subject').order_by('-attempted_at')
    total_attempts = quiz_attempts.count()
    
    # Add percentage to each attempt for template display
    for attempt in quiz_attempts:
        if attempt.total_questions > 0:
            attempt.percentage = round((attempt.score / attempt.total_questions) * 100, 1)
        else:
            attempt.percentage = 0
    
    # Calculate statistics
    total_score = sum(attempt.score for attempt in quiz_attempts)
    total_questions = sum(attempt.total_questions for attempt in quiz_attempts)
    avg_percentage = (total_score / total_questions * 100) if total_questions > 0 else 0
    
    best_attempt = quiz_attempts.order_by('-score').first() if quiz_attempts.exists() else None
    worst_attempt = quiz_attempts.order_by('score').first() if quiz_attempts.exists() else None
    
    # Subject-wise performance
    subject_stats = {}
    for attempt in quiz_attempts:
        key = f"{attempt.subject.name} - Unit {attempt.unit}"
        if key not in subject_stats:
            subject_stats[key] = {
                'subject': attempt.subject.name,
                'unit': attempt.unit,
                'attempts': 0,
                'total_score': 0,
                'total_questions': 0,
            }
        subject_stats[key]['attempts'] += 1
        subject_stats[key]['total_score'] += attempt.score
        subject_stats[key]['total_questions'] += attempt.total_questions
    
    for key in subject_stats:
        stats = subject_stats[key]
        if stats['total_questions'] > 0:
            stats['avg_percentage'] = round((stats['total_score'] / stats['total_questions']) * 100, 1)
        else:
            stats['avg_percentage'] = 0
    
    context = {
        'user': user,
        'login_history': login_history[:20],  # Show last 20 logins
        'total_logins': total_logins,
        'last_login_obj': last_login_obj,
        'quiz_attempts': quiz_attempts[:50],  # Show last 50 attempts
        'total_attempts': total_attempts,
        'total_score': total_score,
        'total_questions': total_questions,
        'avg_percentage': round(avg_percentage, 1),
        'best_attempt': best_attempt,
        'worst_attempt': worst_attempt,
        'subject_stats': subject_stats,
    }
    return render(request, 'accounts/admin_user_detail.html', context)
