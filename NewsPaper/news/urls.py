from django.urls import path
from .views import PostList, PostDetail, PostSearchList, PostAddView, PostEditView, PostDeleteView, CategoryDetailView, \
    email_success, subscribe_to_category, unsubscribe_to_category
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(100)(PostList.as_view()), name='news'),
    path('<int:pk>/', cache_page(50*10)(PostDetail.as_view()), name='newsdetail'),
    path('search', PostSearchList.as_view()),
    path('add/', PostAddView.as_view(), name='news_add'),
    path('<int:pk>/edit', PostEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('email_success/', email_success, name='email_success'),
    path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_to_category, name='unsubscribe'),

]
