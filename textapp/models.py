from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver 

from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


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
    buyer = models.CharField(max_length=30, null=True, blank=True)
    campus = models.CharField(max_length=30, null=True, blank=True)
    sold = models.BooleanField(default=False)

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
    author = models.CharField(blank=True, max_length=20)
    created_date= models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return str(self.target)

class Usermodel(models.Model):
    intro = models.TextField(blank=True, default='')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile',null='True')
    gender = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.user)

class Todomodel(models.Model):
    user = models.ForeignKey('Usermodel',on_delete=models.CASCADE)
    memo = models.CharField(max_length=30)
    created_date = models.DateTimeField(default=timezone.now)
    types = models.CharField(max_length=20)
    target = models.ForeignKey('Textbookmodel',on_delete=models.CASCADE)
    dopk = models.IntegerField(default=0)
    #出品したものが購入された：bought
    #メッセージきた:msg
    #いいね:good
    
    class Meta:
        ordering = ['created_date']
    
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
    buyer = models.CharField(max_length=20)
    seller = models.CharField(max_length=20)
    target = models.OneToOneField('Textbookmodel',on_delete=models.CASCADE, related_name='chatroomlist' ,null=True)
    created_date=models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.target)

class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email




