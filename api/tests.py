from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Translation

class TranslationAPITestCase(APITestCase):
    def test_translation_endpoint(self):
        url = reverse('translation')
        
        # Test case 1: Successful translation request
        data = {
            'source_text': 'Hello',
            'source_lang': 'en',
            'target_lang': 'es',
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['translation'], 'Hola')
        
        # Test case 2: Missing parameters
        data = {
            'source_text': 'Hello',
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing parameters')
        
        # Test case 3: Cached translation
        translation = Translation.objects.create(
            source_text='Hello',
            source_lang='en',
            target_lang='es',
            translated_text='Hola',
        )
        data = {
            'source_text': 'Hello',
            'source_lang': 'en',
            'target_lang': 'es',
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['translation'], 'Hola')
