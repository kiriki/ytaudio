import django
from django.http import HttpResponse


def index_test(request):
    ver = django.__version__
    return HttpResponse(f'index_test OK, django {ver}')
