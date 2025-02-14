from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import Profile
from django.db import IntegrityError
# these for sending email to user
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


def user_create_view(request:HttpRequest):
    massage = ''
    if request.method == 'POST':

        try:
            new_user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
            new_user.save()
            subject = 'ARhhheennnpooo'.upper()
            message = f'Hi {new_user.first_name} {new_user.last_name}, thank you for registering in HC.'.upper()
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [new_user.email,]
            send_mail( subject, message, email_from, recipient_list )

            return render(request,'home/home.html')
        except Exception as e:
            massage = f'something went wrong, {e}'
    

    return render(request,'user/registraction.html',{'massage':massage})


def login_view(request:HttpRequest):
    massage = ''
    
    if request.method == 'POST':

        try:
            user = authenticate(request,username= request.POST['username'],password=request.POST['password'])

            if user:
                login(request,user)
                return redirect('home:home_view')
            else:
                massage = 'email or password is not valid'
        except Exception as e:
            massage = f'something went wrong, {e}'

    return render(request,'user/login.html',{'massage':massage})


def logout_view(request:HttpRequest):
    
    if request.user.is_authenticated:
        logout(request)
        return redirect('user:login_view')
    

def profile_view(request:HttpRequest,user_id):

    massage = ''
    try:
        new_profile = User.objects.get(id = user_id)
    except:
        return redirect('home:page_not_found_view')

    return render(request,'user/profile.html',{'profile':new_profile,'massage':massage})

def edit_profile_view(request:HttpRequest,user_id):

    massage = ''
    try:
        new_profile = User.objects.get(id = user_id)
    except:
        return redirect('home:page_not_found_view')
    
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                user:User = request.user
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                try:
                    profile:Profile = request.user.profile
                except:
                    profile = Profile(user=user)
                    profile.save()
                
                if 'image' in request.FILES: profile.image = request.FILES['image']
                profile.save()

                return redirect('user:profile_view',user_id = request.user.id)
            
        except IntegrityError as e:
            massage = f"Please select another username"
        except Exception as e:
            massage = f"something went wrong {e}"

    return render(request,'user/updateProfile.html',{'profile':new_profile,'massage':massage})
