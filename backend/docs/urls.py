from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^documents/generate', views.documents_generate),
    url(r'^documents/download/(?P<document_id>\w{0,64})', views.documents_download, name="documents_download")
]