from django.urls import path
from users.views import RegisterAccount, verification, ActivateAccount

app_name = "users"

urlpatterns = [
    path('register/', RegisterAccount.as_view(), name="signup"),
    path('verification/', verification, name="verification-account"),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccount.as_view(), name='activate-account'),
]
