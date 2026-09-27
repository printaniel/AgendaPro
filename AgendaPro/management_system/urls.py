from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from management_system.views import user_views, professional_views


urlpatterns = [
    path('token/',TokenObtainPairView.as_view(), name = 'token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'refresh'),
    # User
    path('user/list/', user_views.UserListView.as_view(), name = 'user-list'),
    # Professional
    path('user/professional-create/', professional_views.ProfessionalCreateView.as_view(), name = 'professional-create'),
    path('user/professional-list/', professional_views.ProfessionalListView.as_view(), name = 'professional-list'),
    path('user/<int:pk>/professional-retrieve/', professional_views.ProfessionalRetrieveView.as_view(), name = 'professional-retrieve'),
    path('user/<int:pk>/professional-update/', professional_views.ProfessionalUpdateView.as_view(), name = 'professional-update'),
    path('user/<int:pk>/professional-destroy/', professional_views.ProfessionalDestroyView.as_view(), name = 'professional-destroy')

]