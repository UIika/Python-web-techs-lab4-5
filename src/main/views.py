from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


WEEKDAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}


class MovieListView(ListView):
    model = Channel
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channels"] = Channel.objects.all()
        context['weekday'] = self.request.GET.get('weekday', '')
        if not context['weekday']:
            context['weekday'] = Weekday(WEEKDAYS[datetime.now().weekday()]).value
        return context


def user_signup(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('username')).first():
            messages.error(request, 'Користувач з таким іменем вже існує')
            return render(request, 'signup.html')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Заповніть всі поля')
            return render(request, 'signup.html')
        if password1 != password2:
            messages.error(request, 'Паролі не співпадають')
            return render(request, 'signup.html')
        user = authenticate(username=username, password=password1)
        if user:
            messages.error(request, 'Користувач з таким іменем вже існує')
            return render(request, 'signup.html')
        if User.objects.filter(email=email).first():
            messages.error(request, 'Користувач з такою поштою вже існує')
            return render(request, 'signup.html')
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неправильний логін або пароль')
    return render(request, 'login.html')

def user_logout(request):
    next = request.POST.get('next', '/')
    logout(request)
    return HttpResponseRedirect(next)