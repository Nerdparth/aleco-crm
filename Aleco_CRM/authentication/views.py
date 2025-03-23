from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("dashboard")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_authentication = authenticate(request, username = username, password = password)
        login(request, user = user_authentication)
        return redirect("custom_admin_view")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("dashboard")