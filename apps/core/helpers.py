import uuid

from django.utils.text import slugify


def get_file_path(instance, filename: str) -> str:
    model = type(instance)
    upload_dir = '{}/{}'.format(
        slugify(model._meta.app_label),
        slugify(model.__name__)
    )

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), ext)
    return 'images/{}/{}'.format(upload_dir, filename)
