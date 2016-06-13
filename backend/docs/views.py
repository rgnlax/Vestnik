# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from models import Article, Archieve
import json
from utils.templator import *

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def documents_generate(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        a = Article.create(json=data["article"])
        docs = Document.fromJson(data["documents"])

        file_name = process_documents(docs, a)
        archive = Archieve.create(file_name)

        return JsonResponse({"url": archive.identifier})

def documents_download(request, document_id):
    a = get_object_or_404(Archieve, identifier=document_id)

    response = HttpResponse(open(a.path, 'rb').read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % a.name
    return response

