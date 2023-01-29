from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as deconnnecter
from django.contrib.auth import login as connecter, authenticate
from django.http import HttpResponse
from .forms import SignupForm, LoginForm
from .models import Doctor, PatientTest, PatientProfile
from .cardio_test import pil_loader, Net, check_cardiomegaly
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import subprocess
import json
import hashlib
import uuid
import os
import time

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()
# Create your views here.

@login_required
def index(request):
	return render(request, 'dash_index.html', {"menu": 1})

@login_required
def sondage(request):
	return render(request, 'dash_sondage.html', {"menu": 2})

@login_required
def d_home(request):
	return render(request, 'sub_pages/d_board.html', {"menu": 2})



####################[USER MANAGEMENT]~~~~~~~~~~~~~~
# GROUP MANAGE
@login_required
def d_user_groups(request):
	return render(request, 'sub_pages/d_user_group_list.html', {"menu": 2})
@login_required
def d_user_groups_create(request):
	group_name = request.args.get('group_name')
	new_group, created = Group.objects.get_or_create(name=group_name)
	return json.dumps({'status':'done'})
@login_required
def d_user_groups_edit(request):
	group_id = request.args.get('group_id')
	group_name = request.args.get('group_name')
	group = Group.objects.filter(id=int(group_id)).first()
	group.name = group_name
	group.save()
	return json.dumps({'status':'done'})
@login_required
def new_analyse(request):
	data = PatientTest.objects.filter(patient=request.user)
	dt = []
	for it in data:
		d = {
			"id": it.id,
			"created_at": it.created_at,
			"percentage": it.percentage
		}
		if float(it.percentage) > 90:
			d["cardio"] = True
		else:
			d["cardio"] = False
		dt.append(d)
	return render(request,'sub_pages/d_upload_data.html', {"items": dt})

@login_required
def list_analyses(request):
	return render(request,'sub_pages/d_analyse_data.html')

@login_required
def user_list(request):
	doctors = Doctor.objects.filter(status=1)
	doctor_not_active = Doctor.objects.filter(status=0)
	return render(request,'sub_pages/user_list.html', {"doctors": doctors, "doctor_not_active": doctor_not_active})

@login_required
def approve_doctor(request):
	doctor_id = request.GET.get('doctor_id')
	doctor = Doctor.objects.filter(id=int(doctor_id)).first()
	doctor.status = 1
	doctor.save()
	return HttpResponse('{"status": 200}')

@login_required
def deny_doctor(request):
	doctor_id = request.GET.get('doctor_id')
	doctor = Doctor.objects.filter(id=int(doctor_id)).first()
	doctor.status = -1
	doctor.save()
	return HttpResponse('{"status": 200}')

@login_required
def user_profile(request):
	if request.method == "POST":
		pos = request.POST.get
		user = request.user
		user.username = pos("username")
		user.first_name = pos("first_name")
		user.last_name = pos("last_name")
		user.email = pos("email")

		profile = PatientProfile.objects.filter(patient=request.user).first()
		profile.birthday = pos("birthday")
		profile.gender = pos("gender")
		profile.save()

		user.save()
		return HttpResponse(json.dumps({"status":"ok"}))
	else:
		profile = PatientProfile.objects.filter(patient = request.user).first()
		return render(request,'sub_pages/user_profile.html', {"profile": profile})

@login_required
def user_profile_security(request):
	if request.method == "POST":
		pos = request.POST.get
		user = request.user
		username = user.username
		password = pos("current_password")
		new_password = pos("new_password")
		confirm_password = pos("confirm_password")
		if new_password != confirm_password:
			return HttpResponse(json.dumps({"status": "nono"}))
		if user.check_password(password):
			user.set_password(new_password)
			user.save()
			return HttpResponse(json.dumps({"status": "ok"}))
		else:
			return HttpResponse(json.dumps({"status": "no"}))
	else:
		return render(request,'sub_pages/user_profile_security.html')

@login_required
def test_cardio(request):
	xray = request.FILES['fileUpload']
	xray_name = str(uuid.uuid1()) + '.' + xray.name.split('.')[-1]
	fs = FileSystemStorage()
	BASE_DIR = getattr(settings, "BASE_DIR", None)
	xray_filename = fs.save(os.path.join(BASE_DIR,'uploads/', xray_name), xray)
	xray_url = 'uploads/' + xray_name 

	fh =  hash_file(os.path.join(BASE_DIR,'uploads/', xray_name))
	check_existing = PatientTest.objects.filter(xray_hash=fh)
	if len(check_existing) > 0:
		ma = check_existing.first().percentage
		time.sleep(1)
		if ma > 90:
			return HttpResponse(json.dumps({"percentage": ma, "isCardiamegaly": True}))
		else:
			return HttpResponse(json.dumps({"percentage": 0, "isCardiamegaly": False}))

	percentage, isCardiamegaly = subprocess.check_output(["python", "dashboard/cardio_test.py", os.path.join(BASE_DIR,'uploads\\', xray_name)]).decode().split("RRR ")[1].split("|")
	percentage1, isCardiamegaly1 = subprocess.check_output(["python", "dashboard/cardio_test.py", os.path.join(BASE_DIR,'uploads\\', xray_name)]).decode().split("RRR ")[1].split("|")
	percentage2, isCardiamegaly2 = subprocess.check_output(["python", "dashboard/cardio_test.py", os.path.join(BASE_DIR,'uploads\\', xray_name)]).decode().split("RRR ")[1].split("|")
	
	tb = [float(percentage), float(percentage1), float(percentage2)]
	ma = max(tb)
	pt = PatientTest()

	# xray_url = models.CharField(max_length=300, blank=True)
	# xray_hash = models.CharField(max_length=300, blank=True)
	# percentag
	pt.patient = request.user
	pt.xray_url = os.path.join(BASE_DIR,'uploads/', xray_name)
	pt.xray_hash = fh
	pt.percentage = ma
	pt.save()
	if ma > 90:
		return HttpResponse(json.dumps({"percentage": ma, "isCardiamegaly": True}))
	else:
		return HttpResponse(json.dumps({"percentage": 0, "isCardiamegaly": False}))

def register(request):
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == "POST":
		form = SignupForm(request.POST, instance=User())
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.save()

			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			return redirect('/dashboard/')
		else:
			return render(request, 'dash_register.html', {"form": form})

	form = SignupForm()
	return render(request, 'dash_register.html', {"form": form})

def register_doctor(request):
	if request.user.is_authenticated:
		return redirect('/dashboard/')
	if request.method == "POST":
		identity_card = request.FILES['identity_card']
		medical_license = request.FILES['medical_license']
		fs = FileSystemStorage()
		identity_card_filename = fs.save(identity_card.name, identity_card)
		medical_license_filename = fs.save(medical_license.name, medical_license)
		identity_card_url = fs.url(identity_card_filename)
		medical_license_url = fs.url(medical_license_filename)
		return json.dumps({"status":200})

	form = SignupForm()
	return render(request, 'dash_register.html', {"form": form})



def login(request):
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
			return render(request, 'dash_login.html', {"form": form})
	return render(request, 'dash_login.html', {"form": form})

def logout(request):
	deconnnecter(request)
	return redirect('/')

def forgot_password(request):
	return render(request, 'dash_forgot-password.html')
