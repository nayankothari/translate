"""
Import some basic modules for logging and translations with the help of django rest framework.
for translation we use translate module, pip install translate, for more details about 
source and target languate kindly consider README.md file
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from translate import Translator
from .models import Translation
import threading

# Create a lock object to handle multiple reqyests using locks or semaphores.
translation_lock = threading.Lock()


log = logging.getLogger(__name__)


class TranslationView(APIView):    
    def get(self, request):    
        """
        Simple get request to handle translation.
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
                log.info("Return translated result from database.")
                return Response({'translation': translation.translated_text})
            
            # Acquire the lock before performing translation
            translation_lock.acquire()

            # If translation does not exist, save new translation to the database
            translator = Translator(from_lang=source_lang, to_lang=target_lang)
            translated_text = translator.translate(source_text)
            Translation.objects.create(
                source_text=source_text,
                source_lang=source_lang,
                target_lang=target_lang,
                translated_text=translated_text
            )      
            log.info("Create new translation record in database.")      
            translation_lock.release()
            return Response({'translation': translated_text})
        except Exception as e:
            log.exception(e.__str__())  
            return Response({'error': 'Server not responding.'}, status=400)    
                  