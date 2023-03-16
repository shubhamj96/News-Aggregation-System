from django.apps import AppConfig
from django.contrib import admin
from News.models import AdminInfo

admin.site.registe(AdminInfo)

class AdminConfig(AppConfig):
    name = 'Admin'
