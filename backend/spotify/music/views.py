from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request,'index.html')

def user_signup(request):
    if request.method == 'POST':
        # taking up all values from Frontend to backend
        username = request.POST['username']
        email =  request.POST['email']
        password =  request.POST['password']
        confirm_password =  request.POST['confirm_password']
        # Checking if the passwords match
        if password == confirm_password:
            # Checking for email already Exist or not
            if User.objects.filter(email = email).exists():
                messages.info(request,"Email already Exists")
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username already Exists")
                return redirect('/signup')
            else:
                # Creating a new user and saving it into database
                user = User.objects.create_user(username=username,password=password,email=email)
                user.save()
                # after Succesful Creation of User we directly loggedin user 
                user_auth = auth.authenticate(username=username,password = password)
                auth.login(request,user_auth)
                return redirect('/')


        else:
            messages.error(request,"Passwords do not matches")
            return redirect("/signup")

    else:    
        return render(request,"signup.html")

@login_required(login_url="/login")
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Credential is Invalid")
            return redirect("/login")
        
    else:    
        return render(request,"login.html")


def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect("/login")
