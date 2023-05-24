from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
import uuid
from django.utils import timezone
# Create your models here.

class UserRegisterCode(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.TextField(max_length=200, blank=False, unique=False)
    code = models.IntegerField()
    expiration = models.DateTimeField(db_index=True)
    attempt = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class UserRecoveryCode(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.TextField(max_length=200, blank=False, unique=False)
    verificationCode = models.IntegerField()
    expiration = models.DateTimeField(db_index=True)
    attempt = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class RecoveryAccountSpecialId(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    accountToRecover = models.ForeignKey(User, related_name="user_to_recover", on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    attempt = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.email
    
    