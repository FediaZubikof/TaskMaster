from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def user_registration(request):
    """ Зарегистрируйте новую учетную запись пользователя. """
    if not request.user.is_authenticated:
        if request.method == "POST":
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                registration_form.save()
                messages.success(request, 'Поздравляем!!. Пожалуйста, войдите в систему.')
                return redirect('login')
        else:
            registration_form = RegistrationForm()
        context = {'registration_form': registration_form}
        return render(request, 'user_accounts/registration.html', context)
    else:
        return redirect('tasks')


def user_login(request):
    """  Аутентифицируйте пользователя и войдите в систему. """
    if not request.user.is_authenticated:
        if request.method == 'POST':
            uname = request.POST.get('username')
            upass = request.POST.get('password')
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Успешно вошли в систему!')
                return redirect('tasks')
            else:
                messages.info(request, 'Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.')
                return redirect('login')
        else:
            login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'user_accounts/login.html', context)
    else:
        return redirect('tasks')


def user_logout(request):
    """ Выйдите из системы с текущим пользователем, прошедшим проверку подлинности. """
    logout(request)
    return redirect('login')
