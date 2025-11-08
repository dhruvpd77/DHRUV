from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from semesters.models import Semester, Subject, Question
from .models import QuizAttempt, QuizAnswer
import random

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
    
    return render(request, 'quiz/select_mode.html', {
        'subject': subject,
        'unit': unit,
        'total_questions': total_questions
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
        # Random Mode: Just pick 10 random questions (can repeat)
        if len(all_questions) < 10:
            messages.warning(request, f'Only {len(all_questions)} questions available for this unit.')
            quiz_questions = all_questions
        else:
            quiz_questions = random.sample(all_questions, 10)
    
    # Store question IDs in session
    request.session['quiz_questions'] = [q.id for q in quiz_questions]
    request.session['subject_id'] = subject_id
    request.session['unit'] = unit
    request.session['quiz_mode'] = quiz_mode
    
    return render(request, 'quiz/take_quiz.html', {
        'subject': subject,
        'unit': unit,
        'questions': quiz_questions,
        'quiz_mode': quiz_mode
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
    questions = Question.objects.filter(id__in=question_ids)
    
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
                'is_correct': is_correct
            })
    
    quiz_attempt.score = score
    quiz_attempt.save()
    
    # Store mode and subject/unit for continue option
    quiz_mode = request.session.get('quiz_mode', 'random')
    subject_id = request.session.get('subject_id')
    unit = request.session.get('unit')
    
    # Clear quiz question session but keep mode and subject/unit for continue
    del request.session['quiz_questions']
    
    return render(request, 'quiz/quiz_results.html', {
        'score': score,
        'total': len(question_ids),
        'results': results,
        'quiz_attempt': quiz_attempt,
        'quiz_mode': quiz_mode,
        'subject_id': subject_id,
        'unit': unit
    })
