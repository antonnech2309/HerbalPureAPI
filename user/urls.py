from django.urls import path

from user.views import (
    CreateUserView,
    ManageUserView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView, ContactUsView
)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path(
        "token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("contact-us/", ContactUsView.as_view(), name="contact_us")
]