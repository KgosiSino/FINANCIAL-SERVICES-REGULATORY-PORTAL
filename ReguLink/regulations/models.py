from django.db import models

class RegulatoryBody(models.Model):
    name = models.CharField(max_length=200)  # BoB, NBFIRA, FIA
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class RegulatoryDocument(models.Model):
    DOCUMENT_TYPES = (
        ('act', 'Act'),
        ('regulation', 'Regulation'),
        ('directive', 'Directive'),
        ('guideline', 'Guideline'),
        ('form', 'Form'),
    )

    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    regulatory_body = models.ForeignKey(RegulatoryBody, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True)
    published_date = models.DateField()

    def __str__(self):
        return self.title
