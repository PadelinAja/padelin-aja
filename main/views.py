# =======================================
# ===           IMPORTS               ===
# =======================================
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt 
def register_view(request):
    """Handles user registration."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not all([username, email, password]):
            return JsonResponse({'success': False, 'errors': 'All fields required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'errors': 'Username already exists.'}, status=400)
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error during registration: {e}")
            return JsonResponse({'success': False, 'errors': 'Could not create user.'}, status=500)
    return render(request, 'register.html') 

@csrf_exempt
def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid credentials.'}, status=400)
    return render(request, 'login.html') 

def logout_view(request):
    """Logs the user out."""
    logout(request)
    return redirect('main:show_main')
