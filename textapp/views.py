from django.shortcuts import render ,redirect ,get_object_or_404
from .models import Textbookmodel ,Commentmodel ,Usermodel ,Chatroommodel ,Chatmodel ,User ,Todomodel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import CreateView ,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login ,logout
from . import forms
from .forms import UserForm ,UserForm2

from django.contrib.auth import get_user_model
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm
)
from django.template.loader import render_to_string
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
from django.contrib import messages
from django.db.models import Q

# Create your views here.

object_list = ''

def listfunc(request):
    global object_list
    value=0
    form = forms.SearchForm(request.POST or None) 
    if request.user.is_active:
        try:
            user = Usermodel.objects.filter(user__exact=request.user).get()
            try:
                todo = Todomodel.objects.filter(user__exact=user)
                pk=[]
                for do in todo :
                    messages.warning(request,do.memo)
                    pk.append(do.dopk)
                print(pk)
            except Todomodel.DoesNotExist:
                todo = None
            boolean=Usermodel.objects.filter(user__exact=request.user).exists()
        except Usermodel.DoesNotExist:
            boolean = None
    search = ''
    if request.method == "POST":
        if form.is_valid():
            search = form.cleaned_data['search']
    if object_list == '':
        object_list = Textbookmodel.objects.filter(
            Q(title__contains = search)|
            Q(collegecategory__contains = search)|
            Q(campus__contains = search)|
            Q(content__contains = search)
            )
    object_lists = object_list
    object_list = ''
    if request.user.is_active:
        return render(request, 'list.html',{
            'object_lists':object_lists,
            'form':form,
            'boolean':boolean,
            })
        object_list = ''
    else:
        return render(request, 'list.html',{
            'object_lists':object_lists,
            'form':form,
            })
        object_list = ''
    object_list = ''
    


def squeezefunc(request):
    form = forms.SqueezeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data['title']
            college = form.cleaned_data['college']
            if form.cleaned_data['price'] :
                price = form.cleaned_data['price']
            else:
                price = 999999
            sellstatus = form.cleaned_data['sellstatus']
            global object_list
            print(price)
            print(sellstatus)
            if sellstatus == 'False':
                object_list = Textbookmodel.objects.filter(
                    title__contains = title,
                    collegecategory__contains = college,
                    price__lt = price,
                    ).filter(sold=False)
            else :
                object_list = Textbookmodel.objects.filter(
                    title__contains = title,
                    collegecategory__contains = college,
                    price__lte = price,
                    )
            print(object_list)
            return redirect('list')
    return render(request, 'squeeze.html',{
        'form':form,
    })



def aoyamafunc(request):
    object_list = Textbookmodel.objects.filter(collegecategory__contains = "青山学院大学")
    return render(request,'list.html',{
        'object_list':object_list,
    })

def keiofunc(request):
    object_list = Textbookmodel.objects.filter(collegecategory__contains = "慶應義塾大学")
    return render(request,'list.html',{
        'object_list':object_list,
    })


class Create(CreateView):
    #if request.user.is_active:
    template_name='create.html'
    model=Textbookmodel
    fields = ('title','content','author','images','price','collegecategory','facultycategory','status','campus')
    success_url = reverse_lazy('list')
    def form_valid(self,form):    
        self.object = post = form.save()
        messages.info(self.request, f'出品しました。タイトル:{post.title} ')
        return redirect(self.get_success_url())
        

@login_required
def chatroomfunc(request,pk):
    try :
        object_list = Textbookmodel.objects.get(pk=pk)
        profile = Usermodel.objects.filter(user__exact=request.user).get()
        chatroomlist = Chatroommodel(pk=pk)
        profile2 = Usermodel.objects.filter(username__exact=object_list.author).get()
        form = forms.ChatForm(request.POST or None)

        if Chatroommodel.objects.filter(target=object_list).exists():
            pass
        else:
            Chatroommodel.objects.create(
                buyer = profile.username,
                target = object_list,
                seller = object_list.author,
            )
            Textbookmodel.objects.filter(pk=pk).update(
                trading = True,
                buyer = profile.username
            )
            Todomodel.objects.create(
                user = profile2,
                memo = f'{object_list.title}が購入されました。取引をお願いします。',
                types = 'bought',
                target = object_list,
                dopk=pk
            )
            
        chat_list = Chatroommodel.objects.get(target=object_list)
        if profile.username in chat_list.buyer or profile.username in chat_list.seller:
            pass
        else :
            raise Http404
        chats=Chatmodel.objects.filter(target=chat_list)
        if request.method == "POST":
            if form.is_valid():
                chat = form.save(commit=False)
                if str(object_list.author) == str(profile.username):
                    print(object_list.author)
                    chat.sender = profile.username
                    chat.receiver = chat_list.buyer
                    chat.target = chat_list
                    chat.save()  
                    profile3 = Usermodel.objects.filter(username__exact=chat_list.buyer).get()
                    
                    Todomodel.objects.get_or_create(
                    user = profile3,
                    memo = f'{chat.sender}からメッセージが届きました。返信をお願いします。',
                    types = 'msg',
                    target = object_list,
                    dopk=pk
                    )
                    try:
                        Todomodel.objects.filter(user__exact=profile2).filter(types__exact='msg').delete()
                    except Todomodel.DoesNotExist :
                        pass

                else:
                    print(object_list.author)
                    print(profile.username)
                    chat.sender = profile.username
                    chat.receiver = chat_list.seller
                    chat.target = chat_list
                    chat.save()
                    profile3 = Usermodel.objects.filter(username__exact=chat_list.buyer).get()
                    Todomodel.objects.get_or_create(
                    user = profile2,
                    memo = f'{chat.sender}からメッセージが届きました。返信をお願いします。',
                    types = 'msg',
                    target = object_list,
                    dopk=pk
                    )
                    try:
                        Todomodel.objects.filter(user__exact=profile3).filter(types__exact='msg').delete()
                    except Todomodel.DoesNotExist :
                        pass
            else:
                form = forms.ChatForm()
        return render(request, 'chatroom.html',{
            'chatroomlist':chatroomlist,
            'chats':chats,
            'form':form,
            'object_list':object_list,
            'profile':profile,
            })
    except Usermodel.DoesNotExist :
        return redirect('editmypage')

@login_required
def succeedfunc(request,pk):
    profile = Usermodel.objects.get(user=request.user)
    object_list=Textbookmodel.objects.get(pk=pk)
    Textbookmodel.objects.filter(pk=pk).update(
        sold = True
    )
    Todomodel.objects.filter(target=object_list).all().delete()
    return redirect("list")

@login_required
def failfunc(request,pk):
    object_list=Textbookmodel.objects.get(pk=pk)
    Textbookmodel.objects.filter(pk=pk).update(
        trading =False
    )
    Todomodel.objects.filter(target=object_list).all().delete()
    return redirect("list")


@login_required
def chatfunc(request,pk):
    form = forms.ChatForm(request.POST or None)
    object_list=Textbookmodel.objects.get(pk=pk)
    chats=Chatmodel.objects.filter(sender=object_list)

    if request.method == "POST":
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = object_list.author
            chat.receiver = request.user
            chat.save()
            #user1 = Usermodel.objects.filter(user__exact=)
            Todomodel.objects.create(
            user = profile2,
            memo = f'{chat.sender}からメッセージが届きました。返信をお願いします。',
            types = 'msg'
            )
            #Todomodel.objects.filter(user__exact=).filter(types__exact='msg').delete()
        else:
            form = forms.CommentForm()
        
    return render(request, 'chat.html')

@login_required
def deletefunc(request,pk):
    post = Textbookmodel.objects.get(pk=pk)
    messages.info(request, f'出品を削除しました。　タイトル:{post.title}')
    Textbookmodel.objects.filter(pk=pk).delete()
    return redirect('mypage')

class PostDelete(generic.DeleteView):
    model = Textbookmodel
    success_url = reverse_lazy('mypage')

    def delete(self, request, *args, **kwargs):
        self.object = post = self.get_object()
        message = f'記事を削除しました。 タイトル:{post.title} pk:{post.pk}'
        post.delete()
        messages.info(self.request, message)
        return redirect(self.get_success_url())

@login_required
def createfunc(request):
    detail=Textbookmodel()
    boolean = Usermodel.objects.filter(user__exact=request.user).exists()
    if boolean == False:
        return redirect('editmypage')
    else :
        profile = Usermodel.objects.filter(user__exact=request.user).get()
        initial_dict = {
                'collegecategory': profile.college,
            }
        if request.method == 'GET':
            form = forms.DetailForm(request.POST or None ,initial=initial_dict)  
        else :
            form = forms.DetailForm(request.POST ,request.FILES )
            if form.is_valid():
                detail.title = form.cleaned_data['title']
                detail.content = form.cleaned_data['content']
                detail.collegecategory = form.cleaned_data['collegecategory']
                detail.status = form.cleaned_data['status']
                detail.price = form.cleaned_data['price']
                detail.campus = form.cleaned_data['campus']
                detail.images = form.cleaned_data['images']
                Textbookmodel.objects.create(
                    title=detail.title,
                    content=detail.content,
                    collegecategory=detail.collegecategory,
                    status=detail.status,
                    price=detail.price,
                    campus=detail.campus, 
                    images=detail.images,
                    author=profile.username,
                )
                messages.info(request, f'出品しました。　タイトル:{detail.title}')
                return redirect("list")
        return render(request,'editdetail.html',{
            'form':form,
            'detail':detail,
            })


@login_required
def editdetailfunc(request,pk):
    detail = Textbookmodel(pk=pk)
    boolean = Usermodel.objects.filter(user__exact=request.user).exists()
    post = Textbookmodel.objects.get(pk=pk)
    initial_dict = {
            'title':post.title,
            'content': post.content,
            'collegecategory': post.collegecategory,
            'price': post.price,
            'status': post.status,
            'campus':post.campus,
            'images':post.images,
        }
    if request.method == 'GET':
        form = forms.DetailForm(request.POST or None ,initial=initial_dict)
    else :
        form = forms.DetailForm(request.POST ,request.FILES ) 
        if form.is_valid():
            request.session['form_data'] = request.POST
            detail.title = form.cleaned_data['title']
            detail.content = form.cleaned_data['content']
            detail.collegecategory = form.cleaned_data['collegecategory']
            detail.status = form.cleaned_data['status']
            detail.price = form.cleaned_data['price']
            detail.campus = form.cleaned_data['campus']
            detail.images = form.cleaned_data['images']
            Textbookmodel.objects.filter(pk=pk).update(
                title=detail.title,
                content=detail.content,
                collegecategory=detail.collegecategory,
                status=detail.status,
                price=detail.price,
                campus=detail.campus, 
                images=detail.images,
            )
            messages.info(request, f'出品を更新しました。　タイトル:{detail.title}')
            return redirect("detail",pk=pk)
    return render(request,'editdetail.html',{
        'form':form,
        'detail':detail,
        'post':post,
        'boolean':boolean,
        })


def detailfunc(request,pk):
    boolean = False
    object_list = Textbookmodel.objects.get(pk=pk)
    comments = Commentmodel.objects.filter(target=object_list)
    form = forms.CommentForm(request.POST or None)
    print(request.user.is_active)
    if request.user.is_active:
        boolean = Usermodel.objects.filter(user__exact=request.user).exists()
        if boolean == True:
            profile = Usermodel.objects.filter(user__exact=request.user).get()
            print(profile.username)
    if request.user.is_active:
        if request.method == "POST":
            if boolean == False:
                return redirect('editmypage')
            else :
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.target = object_list
                    comment.author = profile.username
                    comment.save()
                else:
                    form = forms.CommentForm()
    else :
        messages.warning(request,f'ログインしてください')
    if request.user.is_active:
        if Usermodel.objects.filter(user__exact=request.user).exists() :
            return render(request, 'detail.html',{
                'object_list':object_list,
                'form':form,
                'comments':comments,
                'profile':profile,
                'boolean':boolean,
                })
        else:
            return render(request, 'detail.html',{
            'object_list':object_list,
            'form':form,
            'comments':comments,
            'boolean':boolean,
            })
    else:
        return render(request, 'detail.html',{
            'object_list':object_list,
            'form':form,
            'comments':comments,
            })


@login_required
def mypagefunc(request):
    profile = Usermodel.objects.filter(user__exact=request.user).get()
    object_list = Usermodel.objects.all()
    #buyroom = Chatroommodel.objects.filter(buyer__exact=profile.username)
    post = Textbookmodel.objects.filter(author__exact=profile.username)
    trading = Textbookmodel.objects.filter(
        Q(author__exact=profile.username) |
        Q(buyer__exact=profile.username)
    ).filter(trading=True).filter(sold=False)
    sold = Textbookmodel.objects.filter(
        Q(author__exact=profile.username) |
        Q(buyer__exact=profile.username)
    ).filter(sold=True)
    
    boolean=Usermodel.objects.filter(user__exact=request.user).exists()
    #trading3 = Textbookmodel.objects.filter(author__exact=trading2.seller,trading=True)
    #Textbookmodel.objects.filter(title__exact=trading2.target)
    if Textbookmodel.objects.exists():
        return render(request, 'mypage.html',{
            'object_list':object_list,
            'post':post,
            'trading':trading,
            'sold':sold,
            'boolean':boolean})
    else :
        return render(request, 'mypage.html',{
            'object_list':object_list,
            'trading':trading,
            'boolean':boolean,
            'sold':sold})
    
@login_required
def editmypagefunc(request):
    """ initial = {
        'username':'user',
        'college':'tu',
        'gender': '男性',
    } """

    boolean=Usermodel.objects.filter(user=request.user).exists()
    if boolean == True:
        profile2 = Usermodel.objects.filter(user__exact=request.user).get()
        initial_dict = {
        'college' : str(profile2.college),
        'intro' : str(profile2.intro),
        }
        print(profile2.intro)
        form = UserForm2(request.POST or None ,initial=initial_dict)
        print(boolean)
    else :
        form = UserForm(request.POST or None )
    if request.method == 'GET':
        pass
    else:
        if form.is_valid():
            print("yrosiku")
            if boolean == True:
                profile = Usermodel()
                profile.intro = form.cleaned_data['intro']
                profile.college = form.cleaned_data['college']
                Usermodel.objects.filter(user=request.user).update(
                    intro=profile.intro,
                    college=profile.college
                )
            else:
                profile = Usermodel()
                request.session['form_user'] = request.POST
                profile.username = form.cleaned_data['username']
                profile.gender = form.cleaned_data['gender']
                profile.intro = form.cleaned_data['intro']
                profile.college = form.cleaned_data['college']
                try: 
                    Usermodel.objects.get(username=profile.username)
                    return render(request, 'editmypage.html', {
                        'error':'このユーザー名は使用されています。やり直してください。',
                        'form':form,
                        'boolean':boolean
                        })
                except:
                    Usermodel.objects.create(
                        username=profile.username,
                        gender=profile.gender,
                        college=profile.college,
                        intro=profile.intro,
                        user=request.user
                    )
            return redirect('mypage')

    return render(request, 'editmypage.html', {
        'form':form,
        'boolean':boolean,})
    
@login_required
def profilefunc(request,pk):
    object_lists=Textbookmodel.objects.get(pk=pk)
    profile=Usermodel.objects.filter(username__exact=object_lists.author).get()
    object_list=Textbookmodel.objects.filter(author__exact=profile.username)
    print(profile.username)
    return render(request,'profile.html',{
        'profile':profile,
        'object_list':object_list,
    })


@login_required
def logoutfunc(request):
    logout(request)
    

def loginfunc(request):
    if request.method=='POST':
        email2 = request.POST['email']
        password2 = request.POST['password']
        user = authenticate(request, email=email2, password=password2)
        if email is not None:
            login(request, email)
            return redirect('list')
        else:
            return redirect('home')
    return render(request, 'login.html', {'some':100})


def homefunc(request):
    if request.method =='POST':
        username2 = request.POST['username']
        email2 = request.POST['email']
        password2 = request.POST['password']
        try:
            User.objects.get(email=email2)
            return render(request, 'home.html', {'error':'このユーザーは登録されています'})

        except :
            user = User.objects.create_user(username2, email2 , password2)
            return redirect('login')
    return render(request, 'home.html', {'some':100})

@login_required
def goodfunc(request,pk):
    post=Textbookmodel.objects.get(pk=pk)
    post2=request.user.get_username()
    if post2 in post.goodtext:
        return redirect('detail' ,pk=pk)
    else:
        post.good +=1
        post.goodtext=post.goodtext + ' ' + post2
        post.save()
    return redirect('detail' ,pk=pk)
    
@login_required
def goodlistfunc(request):
    goodlist=Textbookmodel.objects.filter(goodtext__contains=request.user)
    return render(request,"goodlist.html",{
        'goodlist':goodlist,
    })


User = get_user_model()


class UserCreate(generic.CreateView):
    template_name = 'user_create copy.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('mail_templates/create/subject.txt', context)
        message = render_to_string('mail_templates/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('login')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'login2 copy.html'

    
    

class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'list.html'