import uuid
from urlparse import urlparse

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.db import models

class Organization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=400)
    slug = models.SlugField(unique=True)
    public_link = models.URLField(max_length=2000, null=True, blank=True)
    public_email = models.EmailField(max_length=254, null=True, blank=True)
    
    def __unicode__(self):
        return self.name
        

class Contributor(models.Model):
    organization = models.ForeignKey(Organization)
    key = models.CharField(max_length=255, null=False, blank=False, primary_key=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    display_name = models.CharField(max_length=400, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile-pics', default='anon.jpg')

    def save(self, *args, **kwargs):
        """
        We need a unique key for each bookmarklet. Let's create that key
        when we create a new bookmarklet entry in the DB
        """

        if not self.key:
            generated_key = uuid.uuid4()
            self.key = str(generated_key)
        
        super(Contributor, self).save(*args, **kwargs)
            
    def __unicode__(self):
        return self.key
    

class InterUserManager(BaseUserManager):
    def create_user(self, email, date_joined, first_name, last_name, confirmation_code, password=None):
        """
        Creates and saves a User with the given email, registrar and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_joined = date_joined,
            first_name = first_name,
            last_name = last_name,
            authorized_by = authorized_by,
            confirmation_code = confirmation_code
        )

        user.set_password(password)
        user.save()

        return user


class InterUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=45, blank=True)
    last_name = models.CharField(max_length=45, blank=True)
    confirmation_code = models.CharField(max_length=45, blank=True)

    objects = InterUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'

    
class Item(models.Model):
    contributor = models.ForeignKey(Contributor)
    description = models.CharField(max_length=117, null=True, blank=True)
    link = models.URLField(max_length=2000, null=True, blank=True)
    short_link = models.CharField(max_length=1000, null=True, blank=True)
    contributed_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        It's helpful to trim down the link to just the TLD. Let's do
        that when we save a new item
        """

        if not self.short_link:
            link_pieces = urlparse(self.link)
            self.short_link = link_pieces.netloc
        
        super(Item, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title