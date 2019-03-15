from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from .models import *
import datetime

# Create your views here.
def signup(request):
    if request.method == 'GET':
        return render(request, 'authentication/signup.html')
    
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('user_email')).count() > 0:
            messages.error(request, 'USER ALREADY EXISTS')
            return HttpResponseRedirect(reverse('schedule:signup'))
        else:
        	username = request.POST.get('user_name')
        	email = request.POST.get('user_email')
        	password = request.POST.get('user_password')
        	user = User.objects.create_user(username=username, email=email, password=password)
        	user.save()
        	messages.success(request, 'USER CREATED SUCCESSFULLY')
        	return HttpResponseRedirect(reverse('schedule:login'))

            

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('schedule:dashboard'))
        return render(request, 'authentication/login.html')
    
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('user_name')).count() == 0:
            messages.error(request, "NO SUCH USER FOUND")
            return HttpResponseRedirect(reverse('schedule:login'))
        else:
            username = request.POST.get('user_name')
            password = request.POST.get('user_password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'LOGIN SUCCESSFULL')
                return HttpResponseRedirect(reverse('schedule:dashboard'))
            else:
                messages.error(request, 'USERNAME/PASSWORD WRONG')
                return HttpResponseRedirect(reverse('schedule:login'))


#@login_required(login_url='/')
def dashboard(request):
	if request.user.is_authenticated:
	    upcoming_schedule_list = Schedule.objects.filter(user__username=request.user.username, date__gte=datetime.datetime.today())
	    previous_schedule_list = Schedule.objects.filter(user__username=request.user.username, date__lte=datetime.datetime.today())
	    return render(request, 'schedule/schedule.html', {'upcoming_schedule_list':upcoming_schedule_list, 'previous_schedule_list':previous_schedule_list})
	else:
		return HttpResponseRedirect(reverse('schedule:login'))

def addSchedule(request):
	if request.user.is_authenticated:
	    if request.method == 'GET':
	        return render(request, 'schedule/add-schedule.html')

	    if request.method == 'POST':
	        obj_schedule = Schedule()
	        obj_schedule.user = request.user
	        obj_schedule.title = request.POST.get('schedule_topic')
	        obj_schedule.date = request.POST.get('schedule_date')
	        obj_schedule.start_time = request.POST.get('schedule_start_time')
	        obj_schedule.end_time = request.POST.get('schedule_end_time')
	        start_time = request.POST.get('schedule_start_time')
	        end_time = request.POST.get('schedule_end_time')

	        if start_time.split(":")[0] > end_time.split(":")[0]:
	        	messages.success(request, 'Start time cannot be smaller than End time')
	        	return HttpResponseRedirect(reverse('schedule:addSchedule'))
	        elif start_time.split(":")[1] > end_time.split(":")[1]:
	        	messages.success(request, 'Start time cannot be smaller than End time')
	        	return HttpResponseRedirect(reverse('schedule:addSchedule'))
	        else:
	        	obj_schedule.save()
		        messages.success(request, 'SCHEDULE CREATED SUCCESSFULLY')
		        return HttpResponseRedirect(reverse('schedule:dashboard'))
	        print(start_time, end_time)        
	else:
		return HttpResponseRedirect(reverse('schedule:login'))


def updateSchedule(request, id):
	if request.user.is_authenticated:
	    if request.method == 'GET':
	        obj_schedule = get_object_or_404(Schedule, id=id)
	        return render(request, 'schedule/update-schedule.html', {'schedule':obj_schedule})

	    if request.method == 'POST':
	        obj_schedule = get_object_or_404(Schedule, id=id)
	        obj_schedule.topic = request.POST.get('schedule_topic')
	        obj_schedule.date = request.POST.get('schedule_date')
	        obj_schedule.start_time = request.POST.get('schedule_start_time')
	        obj_schedule.end_time = request.POST.get('schedule_end_time')
	        start_time = request.POST.get('schedule_start_time')
	        end_time = request.POST.get('schedule_end_time')

	        if start_time.split(":")[0] > end_time.split(":")[0]:
	        	messages.success(request, 'Start time cannot be smaller than End time')
	        	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	        elif start_time.split(":")[1] > end_time.split(":")[1]:
	        	messages.success(request, 'Start time cannot be smaller than End time')
	        	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	        else:
	        	obj_schedule.save()
		        messages.success(request, 'SCHEDULE CREATED SUCCESSFULLY')
		        return HttpResponseRedirect(reverse('schedule:dashboard'))
	else:
		return HttpResponseRedirect(reverse('schedule:login'))


def deleteSchedule(request, id):
	if request.user.is_authenticated:
	    if request.method == 'GET':
	        obj_schedule = get_object_or_404(Schedule, id=id)
	        obj_schedule.delete()
	        messages.success(request, 'SCHEDULE DELETED SUCCESSFULLY')
	        return HttpResponseRedirect(reverse('schedule:dashboard'))
	else:
		return HttpResponseRedirect(reverse('schedule:login'))

def mark(request, id, val):
	if request.user.is_authenticated:
	    if request.method == 'GET':
	        obj_schedule = get_object_or_404(Schedule, id=id)
	        obj_schedule.done = False if int(val) == 0 else True
	        obj_schedule.save()
 
	        if int(val) == 0:
	        	messages.success(request, "MARKED INCOMPLETE")
	        else:
	        	messages.success(request, "MARKED COMPLETE")
	        
	        return HttpResponseRedirect(reverse('schedule:dashboard'))
	else:
		return HttpResponseRedirect(reverse('schedule:login'))