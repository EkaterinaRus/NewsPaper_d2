from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'postTitle',  # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь
            'datetimeCreation',  # количество товаров должно быть больше или равно тому, что указал пользователь
            'categoryType',  # цена должна быть меньше или равна тому, что указал пользователь
        }

