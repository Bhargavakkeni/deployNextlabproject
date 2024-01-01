from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

'''
URLS or API endpoints:
    /home leads to login page.
    /home/signOn is to handle register, login fuctionalites.
    /home/app/<str:username> is to handle admin view.
    /home/register leads to register page.
    /home/addApps is to handle functinality of adding app details to database.
    /home/addApps/<int:id> is to handle delete funcionality of app details in admin view.
    /home/saveTasks is to handle saving tasks completed by user.
'''

urlpatterns = [
    path('',views.index),
    path('signOn', views.signOn, name='signOn'),
    path('app/<str:username>', views.app, name='adminhome'),
    path('register', views.register,name='register'),
    path('registeradmin', views.registerAdmin, name= 'adminRegistration'),
    path('addApps', views.addApps, name='addApps'),
    path('addApps/<int:id>', views.addApps, name='deleteAppDetails'),
    path('saveTasks', views.saveTasks, name='saveTasks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                           document_root=settings.MEDIA_ROOT)