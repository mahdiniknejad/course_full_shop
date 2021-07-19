from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, auth_login, HttpResponseRedirect
from .forms import AuthForm, UserRegisterForm
from django.urls import resolve
from django.contrib.auth import get_user_model
from jalali_date import datetime2jalali
from django.contrib import messages
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.views import View

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

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

            current_site = get_current_site(request)
            mail_subject = 'حساب کاربری خود را تایید کنید'
            message = render_to_string('emails/active_email.html', {
                'user': user,
                'domain': '127.0.0.1:8000/',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            send_mail(mail_subject, message, current_site.domain, (user.email,))

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


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, ('حساب کاربری شما با موفقیت فعال شد'))
            return redirect('/')
        else:
            messages.warning(request, ('متاسفانه حساب کاربری شما فعال نگردید لطفا از صحت ادرس ارسالی به ایمیل اطمینان حاصل کنید'))
            return redirect('/')
