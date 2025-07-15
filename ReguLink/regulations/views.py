from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from audit.models import AuditLog


# def document_list(request):
#     documents = RegulatoryDocument.objects.all().order_by('-published_date')
#     return render(request, 'document_list.html', {'documents': documents})


# def document_list(request):
#     documents = RegulatoryDocument.objects.all().order_by('-published_date')
#     bodies = RegulatoryBody.objects.all()

#     selected_body = request.GET.get('body')
#     selected_type = request.GET.get('type')

#     if selected_body and selected_body != "all":
#         documents = documents.filter(regulatory_body__id=selected_body)

#     if selected_type and selected_type != "all":
#         documents = documents.filter(document_type=selected_type)

#     context = {
#         'documents': documents,
#         'bodies': bodies,
#         'selected_body': selected_body,
#         'selected_type': selected_type
#     }
#     return render(request, 'document_list.html', context)


def document_list(request):
    documents = RegulatoryDocument.objects.all().order_by('-published_date')
    bodies = RegulatoryBody.objects.all()

    selected_body = request.GET.get('body')
    selected_type = request.GET.get('type')
    query = request.GET.get('q')

    if selected_body and selected_body != "all":
        documents = documents.filter(regulatory_body__id=selected_body)

    if selected_type and selected_type != "all":
        documents = documents.filter(document_type=selected_type)

    if query:
        documents = documents.filter(title__icontains=query)

    # Log this view
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action="Viewed document list",
            details=f"body={selected_body}, type={selected_type}, q='{query}'"
        )

    context = {
        'documents': documents,
        'bodies': bodies,
        'selected_body': selected_body,
        'selected_type': selected_type
    }
    return render(request, 'document_list.html', context)































# def document_detail(request, pk):
#     document = get_object_or_404(RegulatoryDocument, pk=pk)
#     return render(request, 'document_detail.html', {'document': document})


def document_detail(request, pk):
    document = get_object_or_404(RegulatoryDocument, pk=pk)

    # Log this view
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action="Viewed document detail",
            details=f"Document: {document.title} (ID: {document.pk})"
        )

    return render(request, 'document_detail.html', {'document': document})

# def search_documents(request):
#     query = request.GET.get('q')
#     documents = RegulatoryDocument.objects.all()
#     if query:
#         documents = documents.filter(title__icontains=query)
#     return render(request, 'search_results.html', {
#         'documents': documents,
#         'query': query
#     })



def search_documents(request):
    query = request.GET.get('q')
    documents = RegulatoryDocument.objects.all()

    if query:
        documents = documents.filter(title__icontains=query)

    # Log this search
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action="Searched documents",
            details=f"Query: '{query}'"
        )

    return render(request, 'search_results.html', {
        'documents': documents,
        'query': query
    })




# def generate_checklist(request):
#     documents = RegulatoryDocument.objects.all().order_by('-published_date')

#     # Same filtering logic as your list view
#     selected_body = request.GET.get('body')
#     selected_type = request.GET.get('type')
#     query = request.GET.get('q')

#     if selected_body and selected_body != "all":
#         documents = documents.filter(regulatory_body__id=selected_body)
#     if selected_type and selected_type != "all":
#         documents = documents.filter(document_type=selected_type)
#     if query:
#         documents = documents.filter(title__icontains=query)

#     # Create the PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="checklist.pdf"'

#     p = canvas.Canvas(response)
#     p.setFont("Helvetica-Bold", 16)
#     p.drawString(100, 800, "Regulatory Compliance Checklist")

#     y = 770
#     p.setFont("Helvetica", 12)
#     for doc in documents:
#         text = f"{doc.title} ({doc.get_document_type_display()}) - {doc.regulatory_body.name}"
#         p.drawString(80, y, text)
#         y -= 20
#         if y < 50:
#             p.showPage()
#             y = 800
#     p.save()
#     return response


def generate_checklist(request):
    documents = RegulatoryDocument.objects.all().order_by('-published_date')
    selected_body = request.GET.get('body')
    selected_type = request.GET.get('type')
    query = request.GET.get('q')

    if selected_body and selected_body != "all":
        documents = documents.filter(regulatory_body__id=selected_body)
    if selected_type and selected_type != "all":
        documents = documents.filter(document_type=selected_type)
    if query:
        documents = documents.filter(title__icontains=query)

    # Log this action
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action="Generated compliance checklist PDF",
            details=f"body={selected_body}, type={selected_type}, q='{query}'"
        )

    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="checklist.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Regulatory Compliance Checklist")
    y = 770
    p.setFont("Helvetica", 12)
    for doc in documents:
        text = f"{doc.title} ({doc.get_document_type_display()}) - {doc.regulatory_body.name}"
        p.drawString(80, y, text)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
    p.save()
    return response
