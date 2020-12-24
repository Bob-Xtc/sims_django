import uuid


def create_uuid():
    return ''.join(str(uuid.uuid4()).split('-'))

