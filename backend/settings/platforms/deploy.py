import os


def read_secret(key):
    file = open(os.path.join(os.sep, 'run', 'secrets', key))
    secret = file.read()
    secret = secret.rstrip().lstrip()
    file.close()
    return secret