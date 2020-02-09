from django.contrib import admin
from .models import Textbookmodel  ,Usermodel ,Commentmodel ,Chatmodel ,Chatroommodel

# Register your models here.

admin.site.register(Textbookmodel)

admin.site.register(Usermodel)

admin.site.register(Commentmodel)

admin.site.register(Chatroommodel)

admin.site.register(Chatmodel)




