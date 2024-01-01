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
    path('home/',views.index,name='home'),
    path('signOn',views.signOn,name='register'),
    path('home/signOn/<str:username>/<str:password>', views.signOn, name='signOn'),
    path('home/app/<str:username>', views.app, name='adminhome'),
    path('register', views.register,name='register'),
    path('home/registeradmin', views.registerAdmin, name= 'adminRegistration'),
    path('home/addApps', views.addApps, name='addApps'),
    path('home/addApps/<int:id>', views.addApps, name='deleteAppDetails'),
    path('home/saveTasks', views.saveTasks, name='saveTasks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                           document_root=settings.MEDIA_ROOT)