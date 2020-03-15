from django import forms
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)

User=get_user_model()

COLLEGE_CHOICES = (
    ('慶應義塾大学','慶應義塾大学'),
    ('早稲田大学','早稲田大学'),
    ('青山学院大学','青山学院大学'))

GENDER_CHOICES = (
    ('男性','男性'),
    ('女性','女性'))

STATUS_CHOICES = (
    ('e','全て'),
    (False,'販売中のみ')
)

QUALITY_CHOICES = (
    ('','状態を選択'),
    ('きれい','きれい'),
    ('少し書き込みあり','少し書き込みあり'),
    ('かなり書き込みあり','かなり書き込みあり'),
    ('あまりきれいでない','あまりきれいでない')
    
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Commentmodel
        fields = ('text',)
    
    text = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        max_length=30,
        initial=''
    )

class UserForm(forms.Form):
    class Meta:
        model = models.Usermodel
        fields = ('username','college','gender','intro')
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'ユーザー名を入力（変更不可）'}
        ),
        required=True,
        max_length=20,
    )
    college = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'大学名、学部学科を入力'}
        ),
        #choices=COLLEGE_CHOICES,
        required=True,
        max_length=20,
    )
    intro = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder':'自己紹介文を入力'}
        ),
        max_length=1000
    )
    gender = forms.ChoiceField(
        widget=forms.Select,
        choices=GENDER_CHOICES
    )

class UserForm2(forms.Form):
    class Meta:
        model = models.Usermodel
        fields = ('college','intro')
    college = forms.CharField(
        widget=forms.TextInput(),
        #choices=COLLEGE_CHOICES,
        required=True,
        max_length=20,
    )
    intro = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder':'自己紹介文を入力'}
        ),
        max_length=1000
    )

class DetailForm(forms.Form):
    class Meta:
        model = models.Textbookmodel
        fields = ('title','content','images','collegecategory','status','price','campus',)

    images = forms.ImageField(
        required=True,
    )

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'例　経済学入門'}
        ),
        max_length=30,
    )
    content = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder':'例　経済学部の必修科目の教科書です。定価5000円です。テストに出そうな部分も書き込んであります。よろしくお願いします。'}
        )
    )
    collegecategory = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(),
    )
    status = forms.ChoiceField(
        widget=forms.Select,
        choices=QUALITY_CHOICES,
    )
    price = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={'placeholder':'例　2000'}
        )
    )
    campus = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'例　渋谷キャンパス'}
        )
    )

    
class ChatForm(forms.ModelForm):
    class Meta:
        model = models.Chatmodel
        fields = ('text',)
    text = forms.CharField(
        initial='',
        max_length=32,
        required = True,
        widget = forms.Textarea(
            attrs={'placeholder':'メッセージを入力'}
        )
    )

class SearchForm(forms.Form):
    search = forms.CharField(
        initial='',
        label='search',
        required = False, # 必須ではない
        widget=forms.TextInput(
        attrs={'placeholder':'キーワードを入力'}
    ))

class SqueezeForm(forms.Form):
    title = forms.CharField(
        initial='',
        label='title',
        required = False,
        widget=forms.TextInput(
            attrs={'placeholder':'タイトルを入力'}
        )
    )
    college = forms.CharField(
        initial='',
        label='college',
        required = False,
        widget = forms.TextInput(
            attrs={'placeholder':'大学名等を入力'}
        )
    )
    price = forms.IntegerField(
        initial='',
        label='price',
        required = False,
        widget=forms.NumberInput(
            attrs={'placeholder':'数字のみ　～円以下'}
        )

    ) 
    sellstatus = forms.ChoiceField(
        label='sellstatus',
        widget = forms.Select,
        choices = STATUS_CHOICES
    )



class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email
