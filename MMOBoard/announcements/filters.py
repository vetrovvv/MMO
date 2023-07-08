from django_filters import FilterSet,DateFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Announcement,ANCTResponse



# создаём фильтр
class AnnouncementFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Announcement

        fields = {'created_at_date':['gte'],
                  'announcement_author_id': ['exact'],
                  'category': ['exact']
                 }

class ANCTResponseFilter(FilterSet):
    class Meta:
        model = ANCTResponse
        fields = {
                  'announcement': ['exact'],
                 }

class CategFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Announcement
        fields = {
                  'category': ['exact'],
                 }