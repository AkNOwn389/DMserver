from django.db import models
import uuid
# Create your models here.

class UserRegisterCode(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.TextField(max_length=200, blank=False, unique=False)
    code = models.IntegerField()
    expiration = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.email