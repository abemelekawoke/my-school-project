# views.py
from django.contrib.admin import site
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.db.models import Count, Q
from .models import StudentProfile, Grade
import json
from collections import OrderedDict

@staff_member_required
def custom_admin_index(request):
    context = site.each_context(request)
    context['title'] = site.index_title

    # 📊 Overall student metrics - Use single query with aggregation
    try:
        student_stats = StudentProfile.objects.aggregate(
            total=Count('id'),
            male=Count('id', filter=Q(Gender='Male')),
            female=Count('id', filter=Q(Gender='Female'))
        )
        
        total = student_stats['total'] or 0
        male = student_stats['male'] or 0
        female = student_stats['female'] or 0
    except Exception as e:
        # Fallback in case of any error
        total = StudentProfile.objects.count()
        male = StudentProfile.objects.filter(Gender='Male').count()
        female = StudentProfile.objects.filter(Gender='Female').count()

    context['student_count'] = total
    context['male_count'] = male
    context['female_count'] = female
    context['male_percent'] = round((male / total * 100), 2) if total else 0
    context['female_percent'] = round((female / total * 100), 2) if total else 0

    # 📈 Pivot grid: school × gender
    SCHOOL_CHOICES = {
        "#1": "ጎዩ ማህበረሰብ ት/ት ቤት 1",
        "#2": "ጎዩ ማህበረሰብ ት/ት ቤት 2",
    }
    GENDER_CHOICES = {
        "Male": "ወ",
        "Female": "ሴ",
    }

    # Build pivot data
    pivot_data = StudentProfile.objects.values('school', 'Gender').annotate(
        count=Count('id')
    ).order_by('school', 'Gender')

    pivot = {school: {gender: 0 for gender in GENDER_CHOICES} for school in SCHOOL_CHOICES}
    
    for row in pivot_data:
        school = row.get('school')
        gender = row.get('Gender')
        count = row.get('count', 0)
        
        if school in pivot and gender in pivot[school]:
            pivot[school][gender] = count

    pivot_display = []
    for school, gender_counts in pivot.items():
        pivot_display.append({
            'school_label': SCHOOL_CHOICES[school],
            'gender_counts': gender_counts,
            'total': sum(gender_counts.values())
        })

    context['pivot_display'] = pivot_display
    context['genders'] = GENDER_CHOICES

    # 📊 Grade distribution by gender - FIXED APPROACH
    # First, get all grades in the correct order
    # Manually define the order based on your system
    GRADE_ORDER = ['KG1', 'KG2'] + [str(i) for i in range(1, 13)]
    
    # Initialize counters
    grade_gender_counts = OrderedDict()
    for grade_code in GRADE_ORDER:
        grade_gender_counts[grade_code] = {'Male': 0, 'Female': 0}
    
    # Get all students with grades using select_related for efficiency
    students_with_grades = StudentProfile.objects.filter(
        New_grade__isnull=False
    ).select_related('New_grade')
    
    # Count manually in Python
    for student in students_with_grades:
        if student.New_grade:
            grade_code = student.New_grade.code
            gender = student.Gender
            
            if grade_code in grade_gender_counts and gender in grade_gender_counts[grade_code]:
                grade_gender_counts[grade_code][gender] += 1
    
    # Also include students without grades in an "Unknown" category
    unknown_count = StudentProfile.objects.filter(New_grade__isnull=True).count()
    if unknown_count > 0:
        grade_gender_counts['Unknown'] = {
            'Male': StudentProfile.objects.filter(New_grade__isnull=True, Gender='Male').count(),
            'Female': StudentProfile.objects.filter(New_grade__isnull=True, Gender='Female').count()
        }
        GRADE_ORDER.append('Unknown')
    
    # Prepare chart data
    chart_labels = []
    male_data = []
    female_data = []
    
    for grade in GRADE_ORDER:
        chart_labels.append(grade)
        male_data.append(grade_gender_counts[grade]['Male'])
        female_data.append(grade_gender_counts[grade]['Female'])

    context['grade_chart_labels'] = json.dumps(chart_labels)
    context['grade_male_data'] = json.dumps(male_data)
    context['grade_female_data'] = json.dumps(female_data)
    
    # Store raw data for debugging if needed
    context['grade_distribution_raw'] = grade_gender_counts

    # Additional statistics
    # Status distribution
    try:
        status_distribution = StudentProfile.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        context['status_distribution'] = list(status_distribution)
    except:
        context['status_distribution'] = []

    # Cycle distribution
    try:
        cycle_distribution = StudentProfile.objects.values('cycle').annotate(
            count=Count('id')
        ).order_by('cycle')
        context['cycle_distribution'] = list(cycle_distribution)
    except:
        context['cycle_distribution'] = []

    return TemplateResponse(request, "admin/index.html", context)