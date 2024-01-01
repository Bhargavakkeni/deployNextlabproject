from rest_framework import serializers
from .models import LoginDetails, AppDetails, TaskDetails

class LoginSerializer(serializers.ModelSerializer):
    '''
    LoginSerialize is a serializer for LoginDetails model.
    '''
    class Meta:
        model = LoginDetails
        fields = ['username', 'password','admin']

class AppDetailsSerializer(serializers.ModelSerializer):
    '''
    AppDetailsSerializer is a serializer for AppDetails model.
    '''
    icons = serializers.ImageField()
    class Meta:
        model = AppDetails
        fields = ['icons', 'appName', 'appLink', 'category', 'subCategory', 'points']

class TaskDetailsSerializer(serializers.ModelSerializer):
    '''
    TaskDetailsSerializer is a serializer for TaskDetails model.
    '''
    screenShot = serializers.ImageField()
    class Meta:
        model = TaskDetails
        fields = ['username', 'tasksId', 'points', 'screenShot']