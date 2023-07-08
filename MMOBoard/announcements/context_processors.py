from django.conf import settings
from .models import *

def get_all_categories(request):
    categories = Category.objects.filter()
    return {
        'all_categories': categories
    }

