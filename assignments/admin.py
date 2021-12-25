from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.User, UserAdmin)
admin.site.register(models.To_Do_Item)
admin.site.register(models.Event_Item)
admin.site.register(models.Class_Item)
admin.site.register(models.Document)
