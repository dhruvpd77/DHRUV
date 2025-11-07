from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:select_semester')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
