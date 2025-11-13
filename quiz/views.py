from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from semesters.models import Semester, Subject, Question
from .models import QuizAttempt, QuizAnswer
import random
import time
import requests
import json
from django.conf import settings
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None

@login_required
def select_semester(request):
    semesters = Semester.objects.all()
    return render(request, 'quiz/select_semester.html', {'semesters': semesters})

@login_required
def select_subject(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    subjects = Subject.objects.filter(semester=semester)
    return render(request, 'quiz/select_subject.html', {
        'semester': semester,
        'subjects': subjects
    })

@login_required
def disclaimer(request, subject_id):
    """Show disclaimer before starting quiz"""
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'quiz/disclaimer.html', {
        'subject': subject
    })

def about_us(request):
    """About Us page with creator information"""
    return render(request, 'quiz/about_us.html')

@login_required
def select_unit(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    # Get distinct units for this subject
    units = Question.objects.filter(subject=subject).values_list('unit', flat=True).distinct().order_by('unit')
    return render(request, 'quiz/select_unit.html', {
        'subject': subject,
        'units': units
    })

@login_required
def select_quiz_mode(request, subject_id, unit):
    """Select quiz mode: Random or Practice All"""
    subject = get_object_or_404(Subject, id=subject_id)
    total_questions = Question.objects.filter(subject=subject, unit=unit).count()
    
    # Check for active random mode quiz session
    continue_quiz = None
    session_key = f'random_quiz_{subject_id}_{unit}'
    if session_key in request.session:
        quiz_data = request.session[session_key]
        start_time = quiz_data.get('start_time')
        if start_time:
            elapsed_time = time.time() - start_time
            remaining_time = 600 - elapsed_time  # 10 minutes = 600 seconds
            if remaining_time > 0:
                continue_quiz = {
                    'remaining_time': int(remaining_time),
                    'remaining_minutes': int(remaining_time // 60),
                    'remaining_seconds': int(remaining_time % 60)
                }
            else:
                # Time expired, clear the session
                del request.session[session_key]
    
    return render(request, 'quiz/select_mode.html', {
        'subject': subject,
        'unit': unit,
        'total_questions': total_questions,
        'continue_quiz': continue_quiz
    })

@login_required
def take_quiz(request, subject_id, unit):
    subject = get_object_or_404(Subject, id=subject_id)
    quiz_mode = request.GET.get('mode', 'random')  # Get mode from URL parameter
    
    # Get all questions from the unit
    all_questions = list(Question.objects.filter(subject=subject, unit=unit))
    
    if not all_questions:
        messages.error(request, 'No questions available for this unit.')
        return redirect('quiz:select_unit', subject_id=subject_id)
    
    # Initialize session key for tracking shown questions in Practice All mode
    session_key = f'practice_all_shown_{subject_id}_{unit}'
    
    if quiz_mode == 'practice_all':
        # Practice All Mode: Show questions that haven't been shown yet
        shown_question_ids = request.session.get(session_key, [])
        available_questions = [q for q in all_questions if q.id not in shown_question_ids]
        
        if not available_questions:
            # All questions have been shown, reset and start over
            messages.info(request, 'You have completed all questions! Starting fresh...')
            request.session[session_key] = []
            available_questions = all_questions
        
        # Select up to 10 questions from available ones
        if len(available_questions) <= 10:
            quiz_questions = available_questions
        else:
            quiz_questions = random.sample(available_questions, 10)
        
        # Mark these questions as shown
        shown_question_ids.extend([q.id for q in quiz_questions])
        request.session[session_key] = shown_question_ids
        
        remaining = len(all_questions) - len(shown_question_ids)
        if remaining > 0:
            messages.info(request, f'Practice All Mode: {remaining} questions remaining in this unit.')
        else:
            messages.success(request, 'You have completed all questions in this unit!')
    else:
        # Random Mode: Check if continuing an existing quiz
        session_key = f'random_quiz_{subject_id}_{unit}'
        continue_quiz = request.GET.get('continue', 'false') == 'true'
        
        if continue_quiz and session_key in request.session:
            # Continue existing quiz - use stored questions
            stored_question_ids = request.session.get('quiz_questions', [])
            quiz_questions = [q for q in all_questions if q.id in stored_question_ids]
            # Preserve order
            quiz_questions = sorted(quiz_questions, key=lambda q: stored_question_ids.index(q.id))
            
            # Calculate remaining time
            quiz_data = request.session[session_key]
            start_time = quiz_data.get('start_time')
            if start_time:
                elapsed_time = time.time() - start_time
                remaining_time = 600 - elapsed_time
                if remaining_time <= 0:
                    # Time expired, start new quiz
                    messages.warning(request, 'Time expired. Starting a new quiz.')
                    continue_quiz = False
        else:
            # Start new quiz
            if len(all_questions) < 10:
                messages.warning(request, f'Only {len(all_questions)} questions available for this unit.')
                quiz_questions = all_questions
            else:
                quiz_questions = random.sample(all_questions, 10)
            
            # Store quiz start time for random mode (10 minute timer)
            request.session[session_key] = {
                'start_time': time.time()
            }
    
    # Store question IDs in session
    request.session['quiz_questions'] = [q.id for q in quiz_questions]
    request.session['subject_id'] = subject_id
    request.session['unit'] = unit
    request.session['quiz_mode'] = quiz_mode
    
    # Calculate remaining time for template
    remaining_time = None
    if quiz_mode == 'random':
        session_key = f'random_quiz_{subject_id}_{unit}'
        if session_key in request.session:
            quiz_data = request.session[session_key]
            start_time = quiz_data.get('start_time')
            if start_time:
                elapsed_time = time.time() - start_time
                remaining_time = max(0, int(600 - elapsed_time))
    
    return render(request, 'quiz/take_quiz.html', {
        'subject': subject,
        'unit': unit,
        'questions': quiz_questions,
        'quiz_mode': quiz_mode,
        'remaining_time': remaining_time
    })

@login_required
def submit_quiz(request):
    if request.method != 'POST':
        return redirect('quiz:select_semester')
    
    # Try to get from session first, then from POST (for timer auto-submit)
    question_ids = request.session.get('quiz_questions', [])
    subject_id = request.session.get('subject_id') or request.POST.get('subject_id')
    unit = request.session.get('unit') or request.POST.get('unit')
    quiz_mode = request.session.get('quiz_mode') or request.POST.get('quiz_mode', 'random')
    
    # Convert to proper types
    try:
        if subject_id:
            subject_id = int(subject_id)
        if unit:
            unit = int(unit)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quiz data. Please start again.')
        return redirect('quiz:select_semester')
    
    # If session data is missing, try to reconstruct from form data
    if not question_ids or not subject_id or not unit:
        # Get subject_id and unit from POST (for timer auto-submit)
        if not subject_id or not unit:
            messages.error(request, 'Quiz session expired. Please start again.')
            return redirect('quiz:select_semester')
        
        # If we have subject_id and unit but missing question_ids, try to get from database
        # This handles cases where session expired but we still have form data
        subject = get_object_or_404(Subject, id=subject_id)
        all_questions = Question.objects.filter(subject=subject, unit=unit)
        
        if all_questions.exists():
            # Extract question IDs from form data (from radio button names)
            form_question_ids = []
            for key in request.POST.keys():
                if key.startswith('question_'):
                    try:
                        q_id = int(key.replace('question_', ''))
                        form_question_ids.append(q_id)
                    except ValueError:
                        continue
            
            if form_question_ids:
                # Use questions from form
                question_ids = form_question_ids
            else:
                # Fallback: use first 10 questions
                question_ids = list(all_questions[:10].values_list('id', flat=True))
            
            # Restore session for this submission
            request.session['quiz_questions'] = question_ids
            request.session['subject_id'] = subject_id
            request.session['unit'] = unit
            request.session['quiz_mode'] = quiz_mode
        else:
            messages.error(request, 'No questions found for this quiz. Please start again.')
            return redirect('quiz:select_semester')
    
    subject = get_object_or_404(Subject, id=subject_id)
    # Get questions and preserve order
    questions_dict = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
    questions = [questions_dict[qid] for qid in question_ids if qid in questions_dict]
    
    # Calculate score
    score = 0
    quiz_mode = request.session.get('quiz_mode', 'random')
    
    # Get time taken for random mode
    time_taken = None
    if quiz_mode == 'random':
        time_taken_str = request.POST.get('time_taken', '0')
        try:
            time_taken = int(time_taken_str)
        except (ValueError, TypeError):
            time_taken = None
    
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        subject=subject,
        unit=unit,
        score=0,
        total_questions=len(question_ids),
        quiz_mode=quiz_mode,
        time_taken=time_taken
    )
    
    # Evaluate all questions:
    # - Answered questions: Check if correct/incorrect, add to score if correct
    # - Unanswered questions: Mark as "Not Attempted", no score added
    # Example: 6 answered (4 correct, 2 wrong) + 4 unanswered = Score: 4/10
    results = []
    
    # Debug: Log all POST data to see what's being submitted
    # print("POST data:", dict(request.POST))
    
    for question in questions:
        # Get selected answer - check both POST and form data
        selected = request.POST.get(f'question_{question.id}')
        
        # If not found, try alternative format (some browsers might send differently)
        if not selected:
            # Try to get from POST list
            selected_list = request.POST.getlist(f'question_{question.id}')
            if selected_list:
                selected = selected_list[0]
        
        if selected and selected.strip():
            # Answer was selected - evaluate it (correct or incorrect)
            is_correct = (selected == question.correct_answer)
            if is_correct:
                score += 1  # Only correct answers add to score
            
            # Save the answer to database
            QuizAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_answer=selected,
                is_correct=is_correct
            )
            
            # Add to results with evaluation (correct/incorrect)
            results.append({
                'question': question,
                'selected': selected,
                'correct': question.correct_answer,
                'is_correct': is_correct,
                'attempted': True
            })
        else:
            # Question not attempted (timer expired or user didn't answer)
            # Mark as "Not Attempted" - no score, but show in results
            # Don't create QuizAnswer record for unanswered questions
            results.append({
                'question': question,
                'selected': None,
                'correct': question.correct_answer,
                'is_correct': False,
                'attempted': False
            })
    
    # Final score = only from answered questions (correct answers)
    # Example: 6 answered (4 correct) + 4 unanswered = Score: 4/10
    quiz_attempt.score = score
    quiz_attempt.save()
    
    # Store mode and subject/unit for continue option
    quiz_mode = request.session.get('quiz_mode', 'random')
    subject_id = request.session.get('subject_id')
    unit = request.session.get('unit')
    
    # Clear quiz question session and random quiz session
    del request.session['quiz_questions']
    # Clear random quiz session if it exists
    if subject_id and unit:
        session_key = f'random_quiz_{subject_id}_{unit}'
        if session_key in request.session:
            del request.session[session_key]
    
    return render(request, 'quiz/quiz_results.html', {
        'score': score,
        'total': len(question_ids),
        'results': results,
        'quiz_attempt': quiz_attempt,
        'quiz_mode': quiz_mode,
        'subject_id': subject_id,
        'unit': unit
    })

@login_required
@require_http_methods(["POST"])
def get_question_solution(request, question_id):
    """Generate AI-powered solution explanation for a question"""
    question = get_object_or_404(Question, id=question_id)
    
    # Get AI provider from settings
    ai_provider = getattr(settings, 'AI_PROVIDER', 'groq').lower()
    
    # Build the prompt for the AI - Focus on direct solution steps
    prompt = f"""Solve this MCQ question and provide ONLY the solution steps and calculations. Be direct and concise.

Question: {question.question_text}

Options:
A. {question.option_a}
B. {question.option_b}
C. {question.option_c}
D. {question.option_d}

Correct Answer: {question.correct_answer}

Provide ONLY:
1. Direct solution steps with calculations
2. How to arrive at the answer {question.correct_answer}
3. Brief explanation of why {question.correct_answer} is correct

Do NOT give lengthy explanations. Just show the solution method, calculations, and why the answer is {question.correct_answer}. Be concise and to the point."""

    try:
        solution = None
        
        # Route to appropriate AI provider
        if ai_provider == 'groq':
            solution = get_groq_solution(prompt)
        elif ai_provider == 'huggingface':
            solution = get_huggingface_solution(prompt)
        elif ai_provider == 'gemini':
            solution = get_gemini_solution(prompt)
        elif ai_provider == 'ollama':
            solution = get_ollama_solution(prompt)
        elif ai_provider == 'openai':
            solution = get_openai_solution(prompt)
        else:
            return JsonResponse({
                'error': f'Unknown AI provider: {ai_provider}. Supported: groq, huggingface, gemini, ollama, openai'
            }, status=500)
        
        if solution:
            return JsonResponse({
                'success': True,
                'solution': solution
            })
        else:
            return JsonResponse({
                'error': 'Failed to generate solution. Please check your API configuration.'
            }, status=500)
        
    except Exception as e:
        error_message = str(e)
        error_type = 'unknown'
        user_friendly_message = None
        
        # Check for specific OpenAI API errors
        if 'insufficient_quota' in error_message or 'quota' in error_message.lower():
            error_type = 'quota_exceeded'
            user_friendly_message = (
                "⚠️ API Quota Exceeded\n\n"
                "Your OpenAI API key has exceeded its quota or doesn't have billing set up.\n\n"
                "To fix this:\n"
                "1. Go to https://platform.openai.com/account/billing\n"
                "2. Add a payment method to your account\n"
                "3. Check your usage limits at https://platform.openai.com/usage\n"
                "4. If you're on a free tier, you may need to upgrade to a paid plan\n\n"
                "Alternatively, you can use a different API key with available credits."
            )
        elif 'invalid_api_key' in error_message.lower() or 'authentication' in error_message.lower():
            error_type = 'invalid_key'
            user_friendly_message = (
                "🔑 Invalid API Key\n\n"
                "The OpenAI API key is invalid or has been revoked.\n\n"
                "To fix this:\n"
                "1. Go to https://platform.openai.com/api-keys\n"
                "2. Create a new API key\n"
                "3. Update it in your settings.py or environment variables"
            )
        elif 'rate_limit' in error_message.lower():
            error_type = 'rate_limit'
            user_friendly_message = (
                "⏱️ Rate Limit Exceeded\n\n"
                "Too many requests. Please wait a moment and try again."
            )
        
        # Use user-friendly message if available, otherwise use original error
        final_message = user_friendly_message if user_friendly_message else f'Error generating solution: {error_message}'
        
        return JsonResponse({
            'error': final_message,
            'error_type': error_type
        }, status=500)


def get_groq_solution(prompt):
    """Get solution from Groq API (FREE - No payment required!)"""
    api_key = getattr(settings, 'GROQ_API_KEY', '')
    if not api_key:
        raise Exception('Groq API key not configured. Get free key at: https://console.groq.com/keys')
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",  # Free and fast model
        "messages": [
            {"role": "system", "content": "You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 600,
        "temperature": 0.5
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']


def get_huggingface_solution(prompt):
    """Get solution from Hugging Face Inference API (FREE)"""
    api_key = getattr(settings, 'HUGGINGFACE_API_KEY', '')
    if not api_key:
        raise Exception('Hugging Face API key not configured. Get free key at: https://huggingface.co/settings/tokens')
    
    # Using Meta Llama 3 model (free)
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": f"<|system|>\nYou are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations.\n<|user|>\n{prompt}\n<|assistant|>",
        "parameters": {
            "max_new_tokens": 600,
            "temperature": 0.5,
            "return_full_text": False
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    
    if isinstance(result, list) and len(result) > 0:
        return result[0].get('generated_text', '')
    return result.get('generated_text', '')


def get_gemini_solution(prompt):
    """Get solution from Google Gemini API (FREE tier)"""
    if genai is None:
        raise Exception('Google Generative AI library not installed. Install with: pip install google-generativeai')
    
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        raise Exception('Gemini API key not configured. Get free key at: https://makersuite.google.com/app/apikey')
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    full_prompt = f"You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations.\n\n{prompt}"
    response = model.generate_content(full_prompt)
    return response.text


def get_ollama_solution(prompt):
    """Get solution from Ollama (FREE - Runs locally, no API key needed)"""
    base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
    url = f"{base_url}/api/generate"
    
    data = {
        "model": "llama2",  # You can change to llama3, mistral, etc.
        "prompt": f"You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations.\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.5,
            "num_predict": 600
        }
    }
    
    response = requests.post(url, json=data, timeout=120)
    response.raise_for_status()
    result = response.json()
    return result.get('response', '')


def get_openai_solution(prompt):
    """Get solution from OpenAI API (requires payment method)"""
    if OpenAI is None:
        raise Exception('OpenAI library not installed. Install with: pip install openai')
    
    api_key = getattr(settings, 'OPENAI_API_KEY', '')
    if not api_key:
        raise Exception('OpenAI API key not configured.')
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.5
    )
    return response.choices[0].message.content
