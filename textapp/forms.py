from django import forms
from . import models

COLLEGE_CHOICES = (
    ('慶應義塾大学','慶應義塾大学'),
    ('早稲田大学','早稲田大学'),
    ('青山学院大学','青山学院大学'))

GENDER_CHOICES = (
    ('男性','男性'),
    ('女性','女性'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Commentmodel
        fields = ('text',)

class UserForm(forms.Form):
    class Meta:
        model = models.Usermodel
        fields = ('college','gender','intro')
    
    college = forms.ChoiceField(
        widget=forms.Select,
        choices=COLLEGE_CHOICES,
        required=True,
    )
    intro = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        max_length=1000
    )
    gender = forms.ChoiceField(
        widget=forms.Select,
        choices=GENDER_CHOICES
    )

class DetailForm(forms.Form):
    class Meta:
        model = models.Textbookmodel
        fields = ('title','content','images',)

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(),
        max_length=30,
    )
    content = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.Textarea,
    )
    
class ChatForm(forms.ModelForm):
    class Meta:
        model = models.Chatmodel
        fields = ('text',)
    text = forms.CharField(
        max_length=200,
        required = True,
        widget = forms.TextInput,
    )

class SearchForm(forms.Form):
    search = forms.CharField(
        initial='',
        label='search',
        required = False, # 必須ではない
    )
