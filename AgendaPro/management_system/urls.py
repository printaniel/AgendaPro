from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from management_system.views import user_views


urlpatterns = [
    path('token/',TokenObtainPairView.as_view(), name = 'token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'refresh'),
    # User
    path('user/list/', user_views.UserListView.as_view(), name = 'user-list')
    
]