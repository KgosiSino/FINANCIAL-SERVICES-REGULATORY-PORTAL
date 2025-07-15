from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('search/', views.search_documents, name='search_documents'),
    path('generate_checklist/', views.generate_checklist, name='generate_checklist'),
]
