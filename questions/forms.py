import json

from django import forms
from questions.models import User, Question, Tag, Comment
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
import re

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

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text',]
        widgets = {
            'text': forms.Textarea(attrs={'class':'form-control',
                                          'cols': "5",
                                          'rows':'5',
                                          'placeholder':"Enter your answer here.."})
        }




    def __init__(self, user_id=None, question_number=None,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self._user_id = user_id
        self._question_number = question_number



    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
           raise forms.ValidationError('please type Comment')
        return text

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author_id = self._user_id
        comment.question_id = self._question_number
        if commit:
            comment.save()
        return comment


class AskForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control ', 'maxlength':'50'}))


    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self._user_id = user_id

    class Meta:
        model = Question
        fields = ['title', 'text' ]
        widgets= {
            'title': forms.TextInput(attrs={'class':'form-control', 'maxlength':'100'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '300', 'cols': '5', 'rows': '5'})
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        self._tag_list = re.findall('(\w+)', tags)
        if self._tag_list:
            return tags
        raise forms.ValidationError('please, input tags')

    def save(self, commit=True):
        question = super().save(commit=False)
        tag_objects_list = []
        for tag in self._tag_list:
            tags = Tag.objects.filter(title=tag)
            if tags:
                tag_objects_list.append(tags[0])
            else:
                new_tag = Tag.objects.create(title=tag)
                tag_objects_list.append(new_tag)
        question.author_id = self._user_id
        if commit:
            question.save()
            question.tags.add(*tag_objects_list)
        return question
        # tags = self.cleaned_data['tags']
        # tag_list = re.findall('(\w+)', tags)



class AjaxForm(forms.Form):

    jsonfield = forms.CharField(max_length=1024)

    def clean_jsonfield(self):
        jdata = self.cleaned_data['jsonfield']
        try:
            json_data = json.loads(jdata)
        except:
            raise forms.ValidationError("Invalid data in jsonfield" )

        return jdata


# class QuestionForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['text'].widget.attrs.update({'class':'long'})
#
#
#     class Meta:
#         model = Question
#         exclude = ['is_active', 'author','create_date', 'tags']