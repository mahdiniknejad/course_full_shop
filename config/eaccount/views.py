from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, auth_login, HttpResponseRedirect
from .forms import AuthForm, UserRegisterForm
from django.urls import resolve
from django.contrib.auth import get_user_model
from jalali_date import datetime2jalali
from django.contrib import messages

import datetime
import uuid
import jdatetime


User = get_user_model()
# Create your views here.


class EditedLoginView(LoginView):
    template_name = './accounts/signin.html'
    form_class = AuthForm

    def get_success_url(self):
        _next = self.request.GET.get('next')
        url_name = resolve(_next).url_name
        app_name = resolve(_next).app_name
        if _next is not None:
            return reverse_lazy(f"{app_name}:{url_name}")
        return reverse_lazy('main:main', kwargs={})

    def get_form(self, form_class=None):
        form = super(EditedLoginView, self).get_form(form_class)
        form.fields['username'].widget.attrs = {
            'class': 'input-text input-text--primary-style',
            'id': 'login-email',
            'placeholder': 'ایمیل را وارد کنید',
        }
        form.fields['password'].widget.attrs = {
            'class': 'input-text input-text--primary-style',
            'id': 'login-password',
            'placeholder': 'رمز عبور را وارد کنید',
        }
        return form

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class EditedLogoutView(LogoutView):
    next_page = 'main:main'


def RegisterView(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            password = cd.get('password1')
            year = cd.get('year')
            month = cd.get('month')
            day = cd.get('day')
            birth = jdatetime.date(int(year), int(
                month), int(day)).togregorian()
            user.set_password(password)
            rand_u = str(uuid.uuid4())
            rand_u = "guest@{rand_username}".format(rand_username=rand_u[0:8])
            user.username = rand_u
            user.is_active = False
            user.birth = birth
            user.save()
            messages.add_message(
                request,
                messages.INFO,
                'حساب با موفقیت ساخته شد برای فعال سازی حساب کافی است ایمیل فرستاده شده را تایید کنید', 
            )

    else:
        form = UserRegisterForm(request.POST or None)

    context = {
        'form': form,
    }
    return render(request, './accounts/signup.html', context)
