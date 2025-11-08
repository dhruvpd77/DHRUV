from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from semesters.models import Semester, Subject, Question
from .models import QuizAttempt, QuizAnswer
import random
import time

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
            
            # Store quiz start time for random mode
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
    
    question_ids = request.session.get('quiz_questions', [])
    subject_id = request.session.get('subject_id')
    unit = request.session.get('unit')
    
    if not question_ids or not subject_id or not unit:
        messages.error(request, 'Quiz session expired. Please start again.')
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
    
    results = []
    for question in questions:
        selected = request.POST.get(f'question_{question.id}')
        if selected:
            is_correct = (selected == question.correct_answer)
            if is_correct:
                score += 1
            
            QuizAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_answer=selected,
                is_correct=is_correct
            )
            
            results.append({
                'question': question,
                'selected': selected,
                'correct': question.correct_answer,
                'is_correct': is_correct,
                'attempted': True
            })
        else:
            # Question not attempted - still show it in results
            results.append({
                'question': question,
                'selected': None,
                'correct': question.correct_answer,
                'is_correct': False,
                'attempted': False
            })
    
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
