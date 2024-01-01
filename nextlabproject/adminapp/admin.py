from django.contrib import admin
from .models import LoginDetails, AppDetails, TaskDetails

class ListLoginDetails(admin.ModelAdmin):
    list_display =('username', 'password','admin')

class ListAppDetails(admin.ModelAdmin):
    list_display =('icons', 'appName', 'appLink', 'category', 'subCategory', 'points')

class ListTaskDetails(admin.ModelAdmin):
    list_display =('username', 'tasksId', 'points', 'screenShot')

admin.site.register(LoginDetails, ListLoginDetails)
admin.site.register(AppDetails, ListAppDetails)
admin.site.register(TaskDetails, ListTaskDetails)

