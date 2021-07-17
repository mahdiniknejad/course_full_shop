from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class AuthForm(AuthenticationForm):
    remember_me = forms.BooleanField(label='مرا به خاطر بسپار', required=False)


class UserRegisterForm(forms.ModelForm):
    YEAR_CHOICES = ( (i , i) for i in range(timezone.now().year - 79 - 621, timezone.now().year -18 - 621))
    MONTH_CHOICES = ( (i , i) for i in range(1,13))
    DAY_CHOICES = ( (i , i) for i in range(1, 32))
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-text input-text--primary-style', 'placeholder': 'رمز'}),
        label='رمز عبور',
        help_text='رمز عبور باید شامل ۸ یا بیشتر کاراکتر عدد و حروف باشدلطفا از رمزی با ایمنی بالا استفاده کنید'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-text input-text--primary-style', 'placeholder': 'تکرار رمز'}),
        label='تکرار رمزعبور',
        help_text='رمز عبور و ترار آن باید یکسان باشند'
    )
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'select-box select-box--primary-style'}) ,initial='1379')
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'select-box select-box--primary-style'}), initial='1')
    day = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.Select(attrs={'class': 'select-box select-box--primary-style'}), initial='1')


    class Meta:
        model = User
        fields = ('email', 'number', 'first_name', 'last_name', 'gender')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-text input-text--primary-style', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'input-text input-text--primary-style', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'input-text input-text--primary-style', 'placeholder': 'ایمیل'}),
            'gender': forms.Select(attrs={'class': 'select-box select-box--primary-style u-w-100'})
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     pw1 = cleaned_data.get('password1')
    #     pw2 = cleaned_data.get('password2')

    #     if len(pw1) < 8:
    #         raise ValidationError(
    #             'لطفا رمز عبور مناسب وارد کنید'
    #         )
    #     valid_password_char = 0
    #     for c in pw1:
    #         if 96 < ord(c) < 123:
    #             valid_password_char += 1
    #             break
        
    #     for c in pw1:
    #         if 64 < ord(c) < 91:
    #             valid_password_char += 1
    #             break
        
    #     for c in pw1:
    #         if 47 < ord(c) < 58:
    #             valid_password_char += 1
    #             break

    #     if valid_password_char != 3:
    #         raise ValidationError(
    #             'رمز عبور باید شامل حروف بزرگ و کوچک و عدد باشد'
    #         )         

    #     if pw1 != pw2:
    #         raise ValidationError(
    #             'تکرار رمز عبور صحیح نمیباشد'
    #         )