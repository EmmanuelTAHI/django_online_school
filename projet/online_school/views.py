from django.shortcuts import render

def index(request):
    return render(request, 'online_school/index.html')

def about(request):
    return render(request, 'online_school/about.html')

def contact(request):
    return render(request, 'online_school/contact.html')

def courses(request):
    return render(request, 'online_school/courses.html')

def course_details(request):
    return render(request, 'online_school/course-details.html')

def events(request):
    return render(request, 'online_school/events.html')

def pricing(request):
    return render(request, 'online_school/pricing.html')

def starter_page(request):
    return render(request, 'online_school/starter-page.html')

def trainers(request):
    return render(request, 'online_school/trainers.html')
