from django.shortcuts import render, redirect, get_object_or_404  # type: ignore[import]
from .models import Student
from django.contrib.auth.decorators import login_required  # type: ignore[import]

def home(request):
    if request.method == "POST":
        name=request.POST["name"]
        roll=int(request.POST["roll"])
        subject=request.POST["subject"]
        marks=int(request.POST["marks"])
        
        students=Student.objects.create(name=name, roll=roll, subject=subject, marks=marks)

        return redirect('core_home')
    
    students = Student.objects.all()
    return render(request, 'core/home.html', {'students': students})

# This makes the view private
#@login_required
def dashboard(request):

    students = Student.objects.all()

    action = None

    if request.method == "POST":

        action = request.POST.get("action")

    return render(request, 'core/dashboard.html', {
        'students': students,
        'action': action
    })
    

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('dashboard')

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    
    if request.method == "POST":
        student.name=request.POST["name"]
        student.roll=int(request.POST["roll"])
        student.marks=int(request.POST["marks"])
        student.subject=request.POST["subject"]
        student.save()
        return redirect('dashboard')
    return render(request, 'core/edit.html', {'student': student})
    