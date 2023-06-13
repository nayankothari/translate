from django.db import models


class Translation(models.Model):
    source_text = models.TextField()
    source_lang = models.CharField(max_length=10)
    target_lang = models.CharField(max_length=10)
    translated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source_lang

    class Meta:
        verbose_name_plural = "Translation"
        
