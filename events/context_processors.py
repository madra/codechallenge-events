'''context processors'''
from django.conf import settings


def global_vars(request):
    '''variables we use globally in templates'''
    data = {
        'APP_NAME': settings.APP_NAME,

    }
    return data
