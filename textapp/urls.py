from django.contrib import admin
from django.urls import path
from .views import listfunc ,Create ,detailfunc ,mypagefunc ,loginfunc  ,goodfunc ,profilefunc ,editmypagefunc ,deletefunc ,editdetailfunc ,chatfunc ,chatroomfunc ,aoyamafunc ,keiofunc ,profilefunc ,goodlistfunc ,homefunc ,logoutfunc,Login ,Logout, succeedfunc ,failfunc ,squeezefunc ,createfunc ,privacyfunc ,termsfunc
from . import views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView 

urlpatterns = [
    path('list/',listfunc,name='list'),
    path('create/',createfunc,name='create'),
    path('detail/<int:pk>',detailfunc,name='detail'),
    path('mypage/',mypagefunc,name='mypage'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('good/<int:pk>',goodfunc,name='good'),
    path('profile/',profilefunc,name='profile'),
    path('editmypage/',editmypagefunc,name='editmypage'),
    path('delete/<int:pk>',deletefunc,name='delete'),
    path('editdetail/<int:pk>', editdetailfunc,name='editdetail'),
    path('chatroom/<int:pk>',chatroomfunc,name='chatroom'),
    path('list/aoyama/',aoyamafunc,name='aoyama'),
    path('list/keio/' ,keiofunc,name='keio'),
    path('profile/<int:pk>',profilefunc,name='profile'),
    path('goodlist/',goodlistfunc,name="goodlist"),
    path('',homefunc,name='home'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('succeed/<int:pk>', succeedfunc, name='succeed'),
    path('fail/<int:pk>',failfunc,name="fail"),
    path('squeeze/',squeezefunc, name="squeeze"),
    path('privacy/',privacyfunc, name="privacy"),
    path('terms/',termsfunc, name="terms"),
    path('ads.txt', TemplateView.as_view(template_name='textapp/ads.txt',content_type='text/plain')),
]