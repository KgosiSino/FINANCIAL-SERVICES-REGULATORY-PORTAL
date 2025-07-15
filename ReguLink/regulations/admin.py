from django.contrib import admin
from .models import RegulatoryDocument, RegulatoryBody

from django import forms
from .models import RegulatoryDocument

class RegulatoryDocumentForm(forms.ModelForm):
    class Meta:
        model = RegulatoryDocument
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

@admin.register(RegulatoryDocument)
class RegulatoryDocumentAdmin(admin.ModelAdmin):
    form = RegulatoryDocumentForm
    list_display = ('title', 'document_type', 'regulatory_body', 'published_date')
    list_filter = ('document_type', 'regulatory_body')
    search_fields = ('title',)
    ordering = ('-published_date',)


@admin.register(RegulatoryBody)
class RegulatoryBodyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)