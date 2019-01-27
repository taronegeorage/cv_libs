import os

def getImList(path):
    """return the jpg file in the current dirs"""
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
