from django import forms
from questions.models import User, Question, Tag
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


# class SignUpForm(forms.ModelForm):
#     repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }), max_length=20)
#     class Meta:
#         model = User
#         fields = ['username', 'nickname', 'email', 'password', 'upload']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
#             'nickname': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50' }),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '50' }),
#             'password': forms.PasswordInput(attrs={'class': 'form-control', 'maxlength': '20' }),
#             'upload': forms.FileInput(attrs={'class': 'form-control-file'})
#         }

    #
    #
    # def clean(self):
    #     cleaned_data = super(SignUpForm, self).clean()
    #     nick = cleaned_data.get("nickname")
    #     password = cleaned_data.get('password')
    #     repeat_password = cleaned_data.get("repeat_password")
    #     if repeat_password != password:
    #         raise forms.ValidationError('different passwords')
    #     try:
    #         u = User.objects.get(nickname=nick)
    #         raise forms.ValidationError('This nickname already exist')
    #     except User.DoesNotExist:
    #         pass

class SignUpForm(UserCreationForm):
    password1 = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'form-control', 'maxlength': '20' }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'maxlength': '20'}))
    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'upload']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50' }),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '50' }),
            'upload': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def clean_upload(self):
        image = self.cleaned_data.get('upload')
        if image:
            return image
        raise forms.ValidationError('please input image')


    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.upload = self.cleaned_data.get('upload')
        if commit:
            user.save()
        return user

class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': '50', 'id':'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'maxlength': '20', 'id':'Password'}))


class UserSettingsForm(UserChangeForm):



    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'password', 'upload']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50' }),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '50' }),
            'upload': forms.FileInput(attrs={'class': 'form-control-file'})
        }

# class QuestionForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['text'].widget.attrs.update({'class':'long'})
#
#
#     class Meta:
#         model = Question
#         exclude = ['is_active', 'author','create_date', 'tags']