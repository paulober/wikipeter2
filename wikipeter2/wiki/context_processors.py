from django.http.request import HttpRequest
from django.urls.base import resolve
from .models import Class, MasterCategory

def baseClasses(request: HttpRequest):
    current_url = resolve(request.path_info).url_name

    if 'members' in current_url or 'login' in current_url or 'dashboard' in current_url:
        return {}
    else:
        classes = Class.objects.all().values_list('id', 'name')
        master_categories = MasterCategory.objects.all().values_list('id', 'title')
        return {
            "ctx_classes": classes,
            "ctx_master_categories": master_categories
        }
