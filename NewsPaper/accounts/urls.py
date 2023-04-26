from django.urls import path
from .views import ProfileView
from .views import upgrade_me


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('upgrade/', upgrade_me, name='upgrade'),
]


# urlpatterns = [
#     url(r'^accounts/login', MyLoginView.as_view(), name='account_login'),
#     url(r'^accounts/signup', MySignupView.as_view(), name='account_signup'),
#     url(r'^accounts/password_reset', MyPasswordResetView.as_view(), name='account_reset_password'),
# ]
