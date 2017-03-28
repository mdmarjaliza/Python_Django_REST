from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm, SignupForm


class LoginView(View):
    def get(self, request):
        """
        Presenta el formulario de login
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        error_message = ""
        login_form = LoginForm()
        context = {"error": error_message, "form": login_form}
        return render(request, "users/login.html", context)

    def post(self, request):
        """
        Gestiona el login de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        error_message = ""
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("pwd")
            user = authenticate(username=username,
                                password=password)  # authenticate solo recupera el usuario de la BD
            if user is None:
                error_message = "Usuario o contraseña incorrecto"
            else:
                if user.is_active:
                    django_login(request, user)  # Le "asigna" al objeto request el usuario autenticado
                    return redirect(request.GET.get("next", "post_home"))
                else:
                    error_message = "Cuenta de usuario inactiva"

        context = {"error": error_message, "form": login_form}
        return render(request, "users/login.html", context)


class LogoutView(View):
    def get(self, request):
        """
        Hace el logout de un usuario y redirige al login
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        if request.user.is_authenticated():
            django_logout(request)
        return redirect("post_home")


class BlogsView(View):
    def get(self, request):
        """
        Muestra la lista de usuarios que tienen blog en la plataforma
        :param request: objeto HttpRequest con los datos de la peticion
        :return:
        """
        bloggers_list = User.objects.all()
        context = {"bloggers": bloggers_list}
        return render(request, "users/blogs.html", context)


class SignupView(View):
    def get(self, request):
        """
        Muestra el formulario de registro de nuevos usuarios
        :param request:
        :return:
        """
        error_message = ""
        signup_form = SignupForm()
        context = {"error": error_message, "form": signup_form}
        return render(request, "users/signup.html", context)

    def post(self, request):
        """
        Valida los datos de registro de un nuevo usuario y lo crea si son correctos
        :param request:
        :return:
        """
        message = None
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            encrypted_pass = make_password(signup_form.cleaned_data["password"])
            signup_form.instance.password = encrypted_pass
            signup_form.save()
            signup_form = SignupForm()
            message = "Usuario dado de alta satisfactoriamente."

        context = {"message": message, "form": signup_form}
        return render(request, "users/signup.html", context)