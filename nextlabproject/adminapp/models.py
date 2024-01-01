from django.db import models

'''
Models module contain following models:
LoginDetails, AppDetails, TasksDetails.
'''

class LoginDetails(models.Model):
    '''
    LoginDetails model is used to store user login details including admin and enduser.
    It contains two fields username and password. Here 'username' is used as Primary Key.
    It is in a one to many relationship in a TaskDetails model.
    '''
    username = models.CharField(max_length = 255, primary_key = True)
    password = models.CharField(max_length = 155)
    admin = models.BooleanField(default = False)


class AppDetails(models.Model):
    '''
    AppDetails model is used to store app details that are being added by admin user.
    It contains 7 fields id(PK), icons, appName, appLink, category, subCategory, points.
    '''
    icons = models.ImageField(upload_to='images/')
    appName = models.CharField(max_length = 200)
    appLink = models.URLField()
    category = models.CharField(max_length = 255)
    subCategory = models.CharField(max_length = 255)
    points = models.IntegerField()


class TaskDetails(models.Model):
    '''
    TaskDetails model is used to store user completed completed task details.
    It contains four fields id(PK), username(ForeignKey), tasksId, points, screenShot.
    It is in a many to one relationship with LoginDetails model.
    '''
    username = models.ForeignKey(LoginDetails, on_delete = models.CASCADE)
    tasksId = models.IntegerField()
    points = models.IntegerField()
    screenShot = models.ImageField(upload_to='screenshots/')