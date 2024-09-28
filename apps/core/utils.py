from django.conf import settings


def build_client_absolute_url(path: str) -> str:
    domain = settings.CLIENT_DOMAIN
    url_scheme = settings.URL_SCHEME

    return '{url_scheme}://{domain}{path}'.format(
        url_scheme=url_scheme,
        domain=domain,
        path=path,
    )
