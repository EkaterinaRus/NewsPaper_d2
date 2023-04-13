from django.urls import path
from .views import PostList, PostDetail, PostSearchList, PostAddView, PostEditView, PostDeleteView  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostList.as_view(), name='news'),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>/', PostDetail.as_view(), name='newsdetail'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('search', PostSearchList.as_view()),
    path('add/', PostAddView.as_view(), name='news_add'),  # Ссылка на создание товара

    path('<int:pk>/edit', PostEditView.as_view(), name='news_edit'),  # Ссылка на создание товара

    path('<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
]
