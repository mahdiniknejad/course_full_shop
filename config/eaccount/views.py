from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, auth_login, HttpResponseRedirect
from .forms import AuthForm, UserRegisterForm
from django.urls import resolve
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
        pass
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, './accounts/signup.html', context)
