from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from .models import LoginDetails, AppDetails, TaskDetails
from .serializers import LoginSerializer, AppDetailsSerializer, TaskDetailsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

'''
Views module contains following functions:
index, register, signOn(api_view), app, addApps(api_view), saveTasks(api_view)
'''



logging.basicConfig(level=logging.INFO, format="%(asctime)s-[%(levelname)s] [%(threadName)s] (%(module)s):%(lineno)d %(message)s",
                    filename='logging.log')


def index(request):
    '''
    index function returns login page.
    '''
    return render(request,'login.html')


def register(request):
    '''
    register fuction returns register page.
    '''
    return render(request, 'register.html')

def registerAdmin(request):
    '''
    registerAdmin function returns page for admin registration
    '''
    return render(request, 'registeradmin.html')


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def signOn(request):
    '''
    signOn function uses api_view of the django rest framework to handle api requests related to signOn functionality.
    GET - checks the user login credentials if verified redirects to app function.
    POST - Stores the user login credentioal to LoginDetails database.
    It returns mydict(type dictionary) as context containing either verify or error key.
    '''

    if request.method == 'GET':
        logging.info('In signOn GET is triggered.')
        mydict = {}
        if request.GET:
            username = request.GET['username']
            logins = LoginDetails.objects.filter(username = username).values()
            password = request.GET['password']
            for login in logins:
                if username == login['username'] and password == login['password']:
                    return redirect(f'app/{username}')
            else:
                logging.info(f'could not found username {username}')
                mydict['error'] = True
            return render(request, 'login.html', context=mydict)
        else:
            return render(request, 'login.html')
        
    elif request.method == 'POST':
        logging.info('In signOn POST is triggered.')
        mydict={}
        if LoginDetails.objects.filter(username=request.POST['username']).exists():
            logging.debug('Username already existed.')
            return render(request, 'register.html', {'exist':True})
        try:
            serializer = LoginSerializer(data=request.data)
        except Exception as e:
            mydict['error'] = True
            logging.debug('Error occured while saving login details: error {}, recieved data {}'.format(e,request.data))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return render(request, 'register.html',{'verify':True})
        else:
            logging.debug(f"Couldn't save login details as recieved data is not valid. Recieved data {serializer.validated_data}")
            mydict['error'] = True
            return render(request, 'register.html', context=mydict)
        
    elif request.method == 'PUT':
        logging.info('In signOn PUT is triggered.')
        try:
            object = LoginDetails.objects.all().get(username = username)
        except Exception as e:
            logging.debug(f"Error occured while fetchig user details in PUT.")
            return render(request, 'login.html',{'error':True})
        serializer = LoginSerializer(object, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return render(request, 'login.html')
        else:
            logging.debug(f"Couldn't update logindetails as recieved data is not valid.")
            return render(request,'login.html',{'error':True})
        
    elif request.method == 'DELETE':
        logging.info('In signON DELETE is triggered.')
        try:
            object = LoginDetails.objects.all().get(username = username)
        except Exception as e:
            logging.debug(f"Error occured while fetchig user details in DELETE.")
            return render(request, 'login.html',{'error':True})
        if object:
            object.delete()
            return render(request, 'login.html')

    else:
        logging.info("Recieved request is neither GET or POST.")
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
def app(request, *args, **kwargs):
    '''
    app function is to render page view based on user. If admin render admin template else render user template.
    Returns mydict(type dictionary) as context. It contains username(string), appDetails(list of dictionaries) as common for admin and user.
    Additionaly for user it contains remainingTasks(int), results(dict)
    '''
    username = kwargs['username']
    mydict = {
        'username': username,
    }
    appDetails = AppDetails.objects.all().values()
    #print('appDetails',type(appDetails))
    mydict['appDetails'] = appDetails
    check = list(LoginDetails.objects.filter(username = username).values())
    if check[0]['admin'] == True:
        logging.info('username is admin returning admin page.')
        return render(request,'admin.html',context=mydict)
    else:
        logging.info('Username is not admin returning user page.')

        try:
            tasksIdList = TaskDetails.objects.filter(username = username).values('tasksId')
            logging.info('fetching tasks id list.')
        except Exception as e:
            logging.debug('Error occured while fetching tasks ids from tasksdetails table in app function {}'.format(e))
            return render(request, 'user.html', {'error':True})
        
        try:
            results = TaskDetails.objects.filter(username = username).aggregate(
                totalPoints = models.Sum('points'),
                tasksCompleted = models.Count('tasksId')
            )
        except Exception as e:
            logging.debug('Error occured while fetching user task Details {}'.format(e))
            return render(request, 'user.html', {'error':True})
        
        mydict['remainingTasks'] = len(appDetails) - results['tasksCompleted']
        
        #This block is to return tasks(appDetails) that are not completed by user.
        if tasksIdList:
            logging.info('fetched list of tasksIds is {}'.format(tasksIdList))
            appDetails = list(appDetails)
            for taskId in tasksIdList:
                for appDetail in appDetails:
                    if taskId['tasksId'] == appDetail['id']:
                        appDetails.remove(appDetail)
            mydict['appDetails'] = appDetails

        if results['totalPoints']:
            mydict['results'] = results
        else:
            results['totalPoints'] = 0
            mydict['results'] = results
        
        return render(request,'user.html',context=mydict)
    

    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def addApps(request,id='', *args, **kwargs):
    '''
    addApps function uses api_view of the django rest framework to handle api requests related to Apps functionality.
    GET - returns deatils of apps in json format.
    POST - stores app details into AppDetails data base.
    DELETE - deletes app details based on id found in url.
    '''

    if request.method == 'GET':
        logging.info('GET in addApps is triggered.')
        #checks for given id.
        if id:
            try:
                appDetail = AppDetails.objects.all().get(pk=id)
                serializer = AppDetailsSerializer(appDetail)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                logging.debug(f"Couldn't found appDetail with id {id}. Occured error {e}")
                return Response(status=status.HTTP_404_NOT_FOUND)
        appDetails = AppDetails.objects.all().values()
        serializer = AppDetailsSerializer(appDetails, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        logging.info('Recieved app data in addApps post method.')
        try:
            serializer = AppDetailsSerializer(data=request.data)
        except Exception as e:
            logging.debug('Error occured while serializing the data {e}'.format(e))
            return render(request, 'admin.html',{'error':True})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return render(request, 'admin.html',{'verify':True})
        else:
            logging.debug('Error occured while saving the data {e}'.format(e))
            return render(request, 'admin.html',{'error':True})
    
    elif request.method == 'PUT':
        logging.info('In addApps PUT is triggered.')
        try:
            object = AppDetails.objects.all().get(pk = id)
        except Exception as e:
            logging.debug(f"Error occured while fetchig app details in PUT.")
            return render(request, 'admin.html',{'error':True})
        serializer = AppDetailsSerializer(object, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return render(request, 'admin.html')
        else:
            logging.debug(f"Couldn't update app details as recieved data is not valid.")
            return render(request,'admin.html',{'error':True})
        
    elif request.method == 'DELETE':
        try:
            appdetails = AppDetails.objects.all().get(pk=id)
        except Exception as e:
            logging.debug('Error while fetching appDetails with id {} in addApps delete request method'.format(id))
            return render(request, 'admin.html',{'error':True})
        if appdetails:
            appdetails.delete()
            return render(request, 'admin.html',{'verify':True})
    
    else:
        logging.info('Recieved request which is not GET, POST, DELETE')
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def saveTasks(request,id='', *args, **kwargs):
    '''
    saveTasks function uses api_view of the django rest framework to handle api requests related to tasks functionality.
    GET - Send details related to the tasks completed by user.
    POST - Stores tasks completion details to TasksDetails database.
    '''
    #id = kwargs['id']
    if request.method == 'GET':
        logging.info('GET in saveTasks is triggered.')
        #checks for given id.
        if id:
            try:
                taskDetail = TaskDetails.objects.all().get(pk=id)
                serializer = TaskDetailsSerializer(taskDetail)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                logging.debug(f"Couldn't found appDetail with id {id}. Occured error {e}")
                return Response(status=status.HTTP_404_NOT_FOUND)
        taskDetails = TaskDetails.objects.all().values()
        serializer = TaskDetailsSerializer(taskDetails, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        try:
            serializer = TaskDetailsSerializer(data=request.data)
        except Exception as e:
            logging.debug('Error occured while serialzing the data. Received data {} error {}'.format(request.data,e))
            return render(request, 'user.html', {'error':False})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return render(request, 'user.html', {'verify':True})
        else:
            logging.debug('Error while saving the data. Recieved data {}'.format(serializer.validated_data))
            return render(request, 'user.html', {'error':False})
    
    elif request.method == 'PUT':
        logging.info('In saveTasks PUT is triggered.')
        try:
            object = TaskDetails.objects.all().get(pk = id)
        except Exception as e:
            logging.debug(f"Error occured while fetchig task details in PUT.")
            return render(request, 'user.html',{'error':True})
        serializer = TaskDetailsSerializer(object, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return render(request, 'user.html')
        else:
            logging.debug(f"Couldn't update task details as recieved data is not valid.")
            return render(request,'user.html',{'error':True})
        
    elif request.method == 'DELETE':
        try:
            taskDetails = TaskDetails.objects.all().get(pk=id)
        except Exception as e:
            logging.debug('Error while fetching Task Details with id {} in saveTasks delete request method'.format(id))
            return render(request, 'user.html', {'error':True})
        if taskDetails:
            taskDetails.delete()
            return render(request, 'user.html', {'verify':True})
    
    else:
        logging.info('Recieved request is not GET, POST, PUT, DELETE')
        return Response(status=status.HTTP_400_BAD_REQUEST)
