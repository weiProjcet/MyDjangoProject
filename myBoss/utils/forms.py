import re
from django import forms

from myBoss.models import User
from .getSelfInfo import getPageData

"""
    登录时的表单
"""


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': '请输入用户名'}),
        error_messages={
            'required': '用户名不能为空'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': '请输入密码'}),
        error_messages={
            'required': '密码不能为空'
        }
    )


"""
    注册时的表单
"""


class RegistryForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'class': 'form-control',
            'placeholder': '请输入用户名',
            'data-mask': '[a-zA-Z0-9\\.]+'
        }),
        error_messages={
            'required': '用户名不能为空'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': '请输入密码'}),
        error_messages={
            'required': '密码不能为空'
        }
    )
    check_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'placeholder': '请输入密码'}),
        error_messages={
            'required': '确认密码不能为空'
        }
    )

    # 字段自定义验证
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9.]+$', username or ''):
            raise forms.ValidationError('用户名只能包含字母、数字和点')
        return username


"""
    修改用户信息时的表单
"""
educations, workExperience, jobList = getPageData()


class selfInfoForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
        })
    )
    educational = forms.ChoiceField(
        choices=[(item, item) for item in educations],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    workExperience = forms.ChoiceField(
        choices=[(item, item) for item in workExperience],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    work = forms.ChoiceField(
        choices=[(item, item) for item in jobList],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入意向城市'}),
    )

    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'btn btn-white btn-file'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'educational', 'workExperience', 'work', 'address', 'avatar']
