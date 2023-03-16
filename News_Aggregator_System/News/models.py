from django.db import models

# Create your models here.
class DefaulNewsCategory(models.Model):
    n_id=models.AutoField(primary_key=True)
    ref=models.CharField(max_length=20,default='world')
    lang=models.CharField(max_length=20,default='en')
    sort=models.CharField(max_length=20,default='relevancy')

class WatchList(models.Model):
    w_id=models.AutoField(primary_key=True)
    u_id=models.CharField(max_length=20)
    article=models.TextField()
    title=models.TextField()
    img=models.TextField()
    author=models.TextField()

class UserInfo(models.Model):
    u_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=30)
    last_login_date=models.DateField()


class AdminInfo(models.Model):
    admin_id=models.IntegerField(primary_key=True)
    admin_password=models.CharField(max_length=20)