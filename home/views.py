from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as connecter, authenticate


import os
import os.path
import uuid
from django.conf import settings
from dashboard.forms import SignupForm, LoginForm
from dashboard.models import Doctor, PatientProfile

import json
# Create your views here.
def index(request):
	return render(request, 'home_index.html') 

def analyst(request):
	return render(request, 'home_patient_analyst.html')

def doctor_login(request):
	error = ""
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == "POST":
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			print('try authenticate')
			user = authenticate(username=username, password=password)
			if user:
				if user.is_superuser or profile.status == 1:
					connecter(request, user)
					return redirect('/dashboard/')
				else: 
					return redirect('/doctor_login')
			else:
				error = "Username/Password incorrect"
		else:
			errors = "Please enter a correct username and password. Note that both fields may be case-sensitive."
			return render(request, 'doctor_login.html', {"form": form, "errors": errors})
	else:
		form = LoginForm()
	return render(request, 'doctor_login.html', {"form": form, "errors": error})

def doctor_signup(request):
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == "POST":
		if User.objects.filter(email=request.POST.get('email')).exists():
			raise ValidationError("Email exists")
		BASE_DIR = getattr(settings, "BASE_DIR", None)
		identity_card = request.FILES['identity_card']
		medical_license = request.FILES['medical_license']
		fs = FileSystemStorage()
		id_name = str(uuid.uuid1()) + '.' + identity_card.name.split('.')[-1]
		med_name = str(uuid.uuid1()) + '.' + medical_license.name.split('.')[-1]
		identity_card_filename = fs.save(os.path.join(BASE_DIR,'home/static/uploads', id_name), identity_card)
		medical_license_filename = fs.save(os.path.join(BASE_DIR,'home/static/uploads' , med_name), medical_license)
		identity_card_url = '/static/uploads/' + id_name
		medical_license_url = '/static/uploads/' + med_name
		#SuperKing1.0

		#'username','email', 'first_name', 'last_name', 'password1', 'password2'
		data = {
			"username":  request.POST.get('username'),
			"email":  request.POST.get('email'),
			"first_name":  request.POST.get('first_name'),
			"last_name":  request.POST.get('last_name'),
			"password1":  request.POST.get('password'),
			"password2":  request.POST.get('password_confirm')
		}
		sign_form = SignupForm(data)
		if sign_form.is_valid():
			user = sign_form.save()
			user.refresh_from_db()
			user.active = False
			user.save()
			doctor = Doctor()
			doctor.user = user
			doctor.identity_card_url = identity_card_url
			doctor.medical_license_url = medical_license_url
			doctor.save()
			return redirect('/signup_done/')
		return HttpResponse("Error")
	else:
		sign_form = SignupForm()
	return render(request, 'doctor_signup.html', {"form": sign_form})

def patient_login(request):
	error = ""
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == "POST":
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user:
				connecter(request, user)
				return redirect('/dashboard/')
			else:
				error = "Username/Password incorrect"
		else:
			errors = "Please enter a correct username and password. Note that both fields may be case-sensitive."
			return render(request, 'home_patient_login.html', {"form": form, "errors": errors})
	else:
		form = LoginForm()
	suc = False
	if 'registered' in request.GET:
		suc = True
	return render(request, 'home_patient_login.html', {"form": form, "errors": error, "suc": suc})

def patient_signup(request):
	error = ""
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == "POST":
		if User.objects.filter(email=request.POST.get('email')).exists():
			error = 'This email is already exist'
			sign_form = SignupForm()
			return render(request, 'home_patient_register.html', {"form": sign_form, "error": error})

		data = {
			"username":  request.POST.get('email'),
			"email":  request.POST.get('email'),
			"first_name":  request.POST.get('first_name'),
			"last_name":  request.POST.get('last_name'),
			"password1":  request.POST.get('password'),
			"password2":  request.POST.get('password_confirm')
		}

		

		sign_form = SignupForm(data)
		if sign_form.is_valid():
			user = sign_form.save()
			user.refresh_from_db()
			user.active = False
			user.save()
			pp = PatientProfile()
			pp.patient = user
			pp.gender = "unknown"
			pp.birthday = ""
			pp.save()
			return redirect('/patient_login/?registered=True')
		else:
			error = 'Unknown error'
		return render(request, 'home_patient_register.html', {"form": sign_form ,"error": error})
	else:
		sign_form = SignupForm()
	return render(request, 'home_patient_register.html', {"form": sign_form ,"error": error})


def doctor_login_post(request):
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			connecter(request, user)
			return redirect('/dashboard/')
		else:
			print(form.errors)
			return render(request, 'doctor_login.html', {"form": form})
	return render(request, 'doctor_login.html', {"form": form})

