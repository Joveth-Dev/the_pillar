from django.core.exceptions import ValidationError


def validate_image_size(file):
    max_size_mb = 2

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_mb}MB.')


def validate_unique(authors):
    author_names = set()
    for author in authors:
        name = str(author)
        if name in author_names:
            raise ValidationError(f'Duplicate entry found : "{name}"')
