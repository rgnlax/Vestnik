# -*- coding: utf-8 -*-

from docxtpl import DocxTemplate
from time import time
from zip import *
from enum import Enum
from Generator.settings import BASE_DIR
import shutil

WORK_DIR = 'documents'
TEMPLATES_DIR = 'docs/docx_templates'

class Document(Enum):
    CLAIM = 'claim'
    FORM = 'form'
    MEMO = 'memo'
    REVIEW = 'review'

    @classmethod
    def fromJson(cls, json):
        docs = []
        if json["claim"] == True:
            docs.append(Document.CLAIM)
        if json["memo"] == True:
            docs.append(Document.MEMO)
        if json["form"] == True:
            docs.append(Document.FORM)
        if json["review"] == True:
            docs.append(Document.REVIEW)

        return docs


def process_all_documents(article, process_pdf=False):
    # type: (Article, bool) -> object
    directory = _prepare_workdir()

    _process_doc(Document.FORM, directory, article)
    _process_doc(Document.CLAIM, directory, article)
    _process_doc(Document.MEMO, directory, article)
    _process_doc(Document.REVIEW, directory, article)

    return _zip_workdir(directory)

def process_documents(documents, article, process_pdf=False):
    # type: (list, Article, bool) -> object
    directory = _prepare_workdir()

    for document in documents:
        _process_doc(document, directory, article)

    return _zip_workdir(directory)

def _prepare_workdir():
    """
    Create new working directory with timestamp as the name
    """
    dir_name = str(int(time()))

    if not os.path.exists(_work_dir_path(dir_name)):
        os.makedirs(_work_dir_path(dir_name))

    return dir_name

def _zip_workdir(dir_name):
    """Archive current working directory and remove then"""
    zipdir(_work_dir_path(dir_name), includeDirInZip=False)
    shutil.rmtree(_work_dir_path(dir_name))
    return dir_name

def _process_doc(doc, dir, article):
    # type: (string, string, Article) -> none
    """
    Processing document from template
    doc - document name {claim, memo, form, request}
    dir - directory to save
    article - context for template
    :rtype: none
    """
    d = DocxTemplate(os.path.join(BASE_DIR, TEMPLATES_DIR, 'template_%s.docx' % doc))
    d.render({'article': article})
    d.save(os.path.join(BASE_DIR, WORK_DIR, dir, '%s.docx' % doc))

def _work_dir_path(dir):
    return os.path.join(BASE_DIR, WORK_DIR, dir)
def work_dir_archive_path(zip_name):
    return os.path.join(BASE_DIR, WORK_DIR, "%s.zip" % zip_name)