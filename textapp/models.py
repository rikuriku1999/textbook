from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 

# Create your models here.

class Textbookmodel(models.Model):
    title = models.CharField(max_length=100)
    content =models.TextField()
    author = models.CharField(max_length=100)
    images = models.ImageField(upload_to='', null=True ,blank=True ,default='noimage.jpg')
    good = models.IntegerField(null=True, blank=True, default=0)
    goodtext = models.CharField(max_length=200, null=True, blank=True, default='a')
    published_date = models.DateTimeField(blank=True,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    live = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    collegecategory = models.CharField(max_length=30 ,blank=True)
    facultycategory = models.CharField(max_length=30 ,blank=True) 
    status = models.CharField(max_length=30 ,blank=True)
    trading = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Commentmodel(models.Model):
    text = models.TextField()
    target = models.ForeignKey('Textbookmodel', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    created_date= models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return str(self.target)

class Usermodel(models.Model):
    intro = models.TextField(blank=True, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null='True')
    gender = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.user)

class Chatmodel(models.Model):
    sender = models.CharField(max_length=30)
    receiver = models.CharField(max_length=30)
    created_date= models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=100, blank=False)
    target = models.ForeignKey('Chatroommodel',on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_date']

class Chatroommodel(models.Model):
    buyer = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    seller = models.CharField(max_length=30)
    target = models.OneToOneField('Textbookmodel',on_delete=models.CASCADE, related_name='chatroomlist' ,null=True)
    created_date=models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.target)





