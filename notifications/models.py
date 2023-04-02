from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class MyNotification(models.Model):
    user = models.ForeignKey(User, blank=False, related_name="user_notifyer", on_delete=models.CASCADE)
    subjectUser = models.ManyToManyField(User, blank=False, related_name='subjectUser')
    subject_id = models.TextField(blank=True)
    title = models.TextField(max_length=500, blank=False)
    description = models.TextField(max_length=1500)
    notifType = models.IntegerField(blank=False)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        ordering = ["seen", "-date",]
    def __str__(self):
        return self.title