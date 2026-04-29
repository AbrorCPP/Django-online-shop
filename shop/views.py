from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages

def home_page(request):
    return render(request,"home_page.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username = username,
            password = password
        )

        if user:
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,"Username yoki parol noto'g'ri !")
            return redirect("/login/")

    return render(request,"login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
    
        #Guard_clause
        if password1 != password2:
            messages.error(request,"Parol1 bilan Parol2 bir xil emas !")
            return redirect(register_page)
           

        user_exists = User.objects.filter(username = username).exists()

        if user_exists:
            messages.error(request,"Bu username allaqachon olingan !")
            return redirect(register_page)
            
        new_user = User.objects.create(
            username = username,
        ) 

        new_user.set_password(raw_password = password2)

        new_user.save()

        return redirect(login_page)
    
    return render(request, "register.html")