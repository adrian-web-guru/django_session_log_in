from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.cache import cache
from .models import AirplaneCollector
from .serializers import AirplaneCollectorSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from datetime import date

class AirplaneCollectorView(viewsets.ModelViewSet):
    queryset = AirplaneCollector.objects.all()
    serializer_class = AirplaneCollectorSerializer
          

class CreateAuthUserView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs): # POST /create-user/ No JWT needed
        
        data = request.data

        pwd = make_password(request.data.get('password'))
        data.update({
            'password':pwd # hash
        })

        response = self.validate_create_user(data)

        return response

    def validate_create_user(self,payload): # BL to validated model creation

        serialized = AirplaneCollectorSerializer(data=payload)

        if serialized.is_valid():
            obj = serialized.save()
            obj.is_superuser = True
            obj.save()
            result = {"payload_response": serialized.data, 
                        "status": status.HTTP_201_CREATED}

        else:
            result = {"payload_response":serialized._errors, 
                    "status": status.HTTP_400_BAD_REQUEST}

        return Response(result)


class SessionView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs): # GET api/session-status/ -< return (True if cache still < 120)

        response = {}
        name = request.data.get('name')

        if name is not None:
            name_fixed = name.replace(' ', '_').lower()

            result = self.find_user_or_collector(name_fixed)
            response = self.handle_response(result)
        else:
            response = {"Wrong payload":True}
    
        return Response(response)
    
    def post(self, request, *args, **kwargs): # POST api/session-status/ store cache

        data = request.data
        response = {}

        request = self.createSession(request)

        if self.logInAuth(data):
            response = {"session_information":request.session}
        elif response is not None: 
            response = "You have to log in first @WheelsUp a session!" 
        return Response(response)


    ################ Utilities ##################

    def find_user_or_collector(self, username): # finds user between model / admin

        user = {}

        existing_users = User.objects.all()
        user = [ _user for _user in existing_users.values() if _user['username']==username] 

        if not user:
            airplane_collectors = AirplaneCollector.objects.all()
            user = [ _user for _user in airplane_collectors.values() if _user['username']==username] 
        return user.pop()

    def handle_response(self, response):    # If correct user has been sent, does it has a valid (alive) session at cache?
        response = "Invalid request" if not response else True
        return response if self.isSessionValid() else "Error!"

    def isSessionValid(self):   # iterates over existing sessions at cache 
 
        result = {}
        _sessions = Session.objects.all() if Session.objects.count() >= 1 else 1

        for session in _sessions:
            user_session = session.get_decoded()   
            if user_session['id_session'][0] == str(session.session_key):  # validates if session still active
                result = {"Session": True, "status": status.HTTP_200_OK}
                return Response(result)
            else: 
                result = {"data": "No Session!", "safe":'False', "status": status.HTTP_401_UNAUTHORIZED}
                return Response(result)
        return result

    def logInAuth(self, payload):   # log in django form with {username,password}
 
        if payload is not None: 
            login_form = AuthenticationForm(data=payload)
            result = {}

            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    result = True
                else:
                    result = False
        else:
            result =  'Error!'
        
        return result

    def createSession(self, request):       # here is where the session is created and store w/ cache
 
        username = request.data.get('username') 
        if username is None:
            return 
        
        name_fixed = username.replace(' ', '_').lower()

        result = self.find_user_or_collector(name_fixed)
        user_id = str(result['id'])
        time_stamp = date.today()

        request.session['id_session'] = request.session.session_key,
        request.session['created_date'] = date.today()
        request.session['username'] = username

        request.session.modified = True

        cache_time = 120
        session_time = 120

        cache_key = f'{user_id}_{time_stamp}_{name_fixed}'
        cache.set(cache_key, 'cache-', cache_time)
        request.session.set_expiry(session_time)

        return request