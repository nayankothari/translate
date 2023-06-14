"""
Import some basic modules for logging and translations with the help of django rest framework.
for translation we use translate module, pip install translate, for more details about 
source and target languate kindly consider README.md file
"""
import logging
import threading
from .models import Translation
from translate import Translator
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create a lock object to handle multiple reqyests using locks or semaphores.
translation_lock = threading.Lock()


log = logging.getLogger(__name__)


class TranslationView(APIView):    
    # Use authentication to prevent api from unauthorized access.
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):    
        """
        GET request to handle translations, This API is limited to translate 5000 characters in one request.
        """        
        try:
            source_text = request.query_params.get('source_text')
            source_lang = request.query_params.get('source_lang')
            target_lang = request.query_params.get('target_lang')
            
            if not source_text or not source_lang or not target_lang:
                return Response({'error': 'Missing parameters'}, status=400)
            
            # Check if translation exists in the database
            translation = Translation.objects.filter(
                source_text=source_text,
                source_lang=source_lang,
                target_lang=target_lang
            ).first()
            
            if translation:
                log.info("Return translated result from database fro user {}".format(request.user.username))
                return Response({'translation': translation.translated_text})
            
            # Acquire the lock before performing translation
            translation_lock.acquire()

            # If translation does not exist, save new translation to the database            
            translator = Translator(from_lang=source_lang, to_lang=target_lang)
            source_text = str(source_text)[:5000] # We can use for loop if need to translate more than 5000 characters.
            translated_text = translator.translate(source_text)
            Translation.objects.create(
                source_text=source_text,
                source_lang=source_lang,
                target_lang=target_lang,
                translated_text=translated_text
            )      
            log.info("Create new translation record in database by user {}".format(request.user.username))      
            translation_lock.release()
            return Response({'translation': translated_text})
        except Exception as e:
            log.exception(e.__str__())  
            return Response({'error': 'Internal server error.'}, status=500)    


class get_token(APIView):
    """
    This module is use to get both tokens.
    """
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')        
            if username and password:
                # Authenticate the user and generate token accordingly
                user = authenticate(username=username, password=password)
                if user:                
                    refresh = RefreshToken.for_user(user)
                    # Return token as response
                    log.info(f"Token generated successfully for user {request.user.username}")
                    return Response({
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh)
                    })

            return Response({'error': 'Invalid credentials'}, status=401)

        except Exception as e:
            log.exception(e)
            return Response({'error': 'Internal server error.'}, status=500)            