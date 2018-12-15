from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from .models import User 

 
def index(request):
    return render(request,'login_app/index.html')

def process_register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key,val in errors.items():
                messages.error(request,val)
            return redirect('/')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            pass_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=first_name,last_name=last_name,email=email,pass_hash=pass_hash.decode())
            request.session['user_id'] = user.id
            messages.success(request,"Successfully Registered!!!")
            return redirect('/success')
        

def process_login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,val in errors.items():
                messages.error(request,val)
            return redirect('/')
        else:
            email = request.POST['login_email']
            # pass_hash = request.POST['password']
            user = User.objects.get(email = request.POST['login_email'])
            request.session['user_id'] = user.id
            messages.success(request,"Successfully Logged in!!!")
        return redirect('/success')

def success(request):
    if 'user_id' not in request.session:
        messages.error(request,"Page cannot be accessed unless user logs in")
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'] )
    return render(request,'login_app/success.html',{'user':user})

def process_logout(request):
    del request.session['user_id']
    return redirect('/')

