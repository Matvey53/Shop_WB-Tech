from django.urls import path

from users.views import ProfileView, RegisterView, TopUpBalanceView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path("profile/top-up/", TopUpBalanceView.as_view(), name="top-up-balance"),
    path('profile/', ProfileView.as_view(), name='profile'),
]
