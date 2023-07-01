from django.urls import path
from .views import PostList, PostDetail, PostSearchList, PostAddView, PostEditView, PostDeleteView, PostCategoryView
    # subscribe_to_category, unsubscribe_to_category
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', cache_page(100)(PostList.as_view()), name='news'),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>/', cache_page(50*10)(PostDetail.as_view()), name='newsdetail'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('search', PostSearchList.as_view()),
    path('add/', PostAddView.as_view(), name='news_add'),  # Ссылка на создание товара
    path('<int:pk>/edit', PostEditView.as_view(), name='news_edit'),  # Ссылка на создание товара
    path('<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),

    # path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
    # path('unsubscribe/<int:pk>/', unsubscribe_to_category, name='unsubscribe'),

]
