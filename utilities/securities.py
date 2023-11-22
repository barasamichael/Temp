import hashlib

def get_gravatar_hash(emailAddress = None):
    """Returns gravatar hash based on email address"""
    return hashlib.md5(emailAddress.lower().encode("utf-8")).hexdigest()
