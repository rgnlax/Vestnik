# -*- coding: utf-8 -*-
import hashlib

def id_generator(string):
    return hashlib.md5(string).hexdigest()
