from django.contrib import admin
from django.urls import path
from .views import listfunc ,Create ,detailfunc ,mypagefunc ,loginfunc  ,goodfunc ,profilefunc ,editmypagefunc ,Editmypage ,deletefunc ,editdetailfunc ,chatfunc ,chatroomfunc ,aoyamafunc ,keiofunc ,profilefunc ,goodlistfunc ,homefunc

urlpatterns = [
    path('list/',listfunc,name='list'),
    path('create/',Create.as_view(),name='create'),
    path('detail/<int:pk>',detailfunc,name='detail'),
    path('mypage/',mypagefunc,name='mypage'),
    path('login/',loginfunc,name='login'),
    
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
]