"""
Quick script to create test data for the quiz system
Run this after migrations: python manage.py shell < create_test_data.py
"""

from django.contrib.auth.models import User
from semesters.models import Semester, Subject, Question

print("Creating test data...")

# Create admin user (if not exists)
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Admin user created (username: admin, password: admin123)")
else:
    print("✓ Admin user already exists")

# Create a test user
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user('testuser', 'test@example.com', 'test123')
    print("✓ Test user created (username: testuser, password: test123)")
else:
    print("✓ Test user already exists")

# Create test semester
semester, created = Semester.objects.get_or_create(
    name="Semester 3",
    defaults={'description': 'Third semester courses'}
)
if created:
    print("✓ Semester created")
else:
    print("✓ Semester already exists")

# Create test subject
subject, created = Subject.objects.get_or_create(
    name="Python Programming",
    semester=semester,
    defaults={'code': 'CS301'}
)
if created:
    print("✓ Subject created")
else:
    print("✓ Subject already exists")

# Create some sample Python questions for Unit 1
sample_questions = [
    {
        'question_text': 'What will be the output of print(type(5))?',
        'option_a': "<class 'int'>",
        'option_b': "<class 'float'>",
        'option_c': "<class 'double'>",
        'option_d': "<class 'integer'>",
        'correct_answer': 'A',
    },
    {
        'question_text': 'Which character is used to make a single line comment?',
        'option_a': '/',
        'option_b': '//',
        'option_c': '#',
        'option_d': '!',
        'correct_answer': 'C',
    },
    {
        'question_text': '''What will be the output of:
x = 10
y = 20
print(x + y)''',
        'option_a': '1020',
        'option_b': '30',
        'option_c': 'x + y',
        'option_d': 'Error',
        'correct_answer': 'B',
    },
]

count = 0
for i, q_data in enumerate(sample_questions, 1):
    q, created = Question.objects.get_or_create(
        subject=subject,
        unit=1,
        question_text=q_data['question_text'],
        defaults={
            'option_a': q_data['option_a'],
            'option_b': q_data['option_b'],
            'option_c': q_data['option_c'],
            'option_d': q_data['option_d'],
            'correct_answer': q_data['correct_answer'],
            'added_by': 'System',
            'verified_by': 'Admin'
        }
    )
    if created:
        count += 1

print(f"✓ Created {count} sample questions for Unit 1")

print("\n" + "="*50)
print("Test data created successfully!")
print("="*50)
print("\nYou can now:")
print("1. Login as admin (username: admin, password: admin123)")
print("2. Login as user (username: testuser, password: test123)")
print("3. Upload your Excel file with questions from admin dashboard")
print("\nRun server: python manage.py runserver")

