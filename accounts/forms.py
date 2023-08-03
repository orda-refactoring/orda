from typing import Any, Dict
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm

class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
    label="아이디",
    widget=forms.TextInput(
        attrs={
            'class': 'appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none ',
            'style': 'width: 96%',
            'placeholder': '아이디를 입력하세요',
            'id': "아이디",
            }          
        )
    )
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '비밀번호를 입력하세요',
                'id': "비밀번호",
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(
            attrs={
                'class': 'appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '아이디를 입력하세요',
                'id': "아이디",
            }
        )
    )
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '비밀번호를 입력하세요',
                'id': "비밀번호",
                'pattern': '^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'
            }
        ),
        help_text="최소 8자 이상의 비밀번호를 입력해주세요. 숫자와 영문 대소문자를 포함해야 합니다."
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '비밀번호를 확인하세요',
                'id': "비밀번호 확인",
            }
        ),
    )
    nickname = forms.CharField(
        label="닉네임",
        widget=forms.TextInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '닉네임를 입력하세요',
                'id': "닉네임",
            }
        )
    )
    email = forms.EmailField(
        label="이메일", 
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '이메일을 입력하세요',
                'id': "이메일",
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
            }
        )
    )
    profile_img = forms.ImageField(
        label="프로필 이미지", 
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class" : "d-none ",
                'id': "프로필 이미지",
            }
        )
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                'lang': 'ko',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "nickname", "email", "profile_img")


class CustomUserChangeForm(UserChangeForm):
    nickname = forms.CharField(
        label="닉네임",
        widget=forms.TextInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '닉네임를 입력하세요',
                'id': "닉네임",
            }
        )
    )
    email = forms.EmailField(
        label="이메일", 
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '이메일을 입력하세요',
                'id': "이메일",
            }
        )
    )
    message = forms.CharField(
        label="상태메시지", 
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%; height:100px',
                'placeholder': '상태메세지를 입력하세요',
                'id': "상태메세지",
            }
        )
    )
    profile_img = forms.ImageField(
        label="프로필 이미지", 
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class" : "d-none ",
                'id': "프로필 이미지",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("nickname", "email", "message", "profile_img",)


class CustomUserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="기존 비밀번호 입력",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '기존 비밀번호를 입력하세요',
                'id': "기존 비밀번호 입력",
            }
        )
    )
    new_password1 = forms.CharField(
        label="새 비밀번호 입력",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '새 비밀번호를 입력하세요',
                'id': "새 비밀번호 입력",
            }
        )
    )
    new_password2 = forms.CharField(
        label="새 비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '새 비밀번호를 확인하세요',
                'id': "새 비밀번호 확인",
            }
        )
    )