import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from translate import Translator
from .models import Translation


log = logging.getLogger(__name__)


class TranslationView(APIView):
    def get(self, request):
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
            return Response({'translation': translation.translated_text})
        
        # If translation does not exist, save new translation to the database
        translator = Translator(from_lang=source_lang, to_lang=target_lang)
        translated_text = translator.translate(source_text)
        Translation.objects.create(
            source_text=source_text,
            source_lang=source_lang,
            target_lang=target_lang,
            translated_text=translated_text
        )
        
        return Response({'translation': translated_text})
