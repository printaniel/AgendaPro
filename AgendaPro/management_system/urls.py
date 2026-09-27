from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from management_system.views import (
    user_views,
    professional_views,
    customer_views,
    service_views,
    professionalservice_views
)


urlpatterns = [
    path('token/',TokenObtainPairView.as_view(), name = 'token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'refresh'),
    # User
    path('user/list/', user_views.UserListView.as_view(), name = 'user-list'),
    path('user/role-list/', user_views.RoleSeparetedUserListView.as_view(), name = 'user-role-list'),
    # Professional
    path('user/professional-create/', professional_views.ProfessionalCreateView.as_view(), name = 'professional-create'),
    path('user/professional-list/', professional_views.ProfessionalListView.as_view(), name = 'professional-list'),
    path('user/<int:pk>/professional-retrieve/', professional_views.ProfessionalRetrieveView.as_view(), name = 'professional-retrieve'),
    path('user/<int:pk>/professional-update/', professional_views.ProfessionalUpdateView.as_view(), name = 'professional-update'),
    path('user/<int:pk>/professional-destroy/', professional_views.ProfessionalDestroyView.as_view(), name = 'professional-destroy'),
    # Customer
    path('user/customer-create/', customer_views.CustomerCreateView.as_view(), name = 'customer-create'),
    path('user/customer-list/', customer_views.CustomerListView.as_view(), name = 'customer-list'),
    path('user/<int:pk>/customer-retrieve/', customer_views.CustomerRetrieveView.as_view(), name = 'customer-retrieve'),
    path('user/<int:pk>/customer-update/', customer_views.CustomerUpdateView.as_view(), name = 'customer-update'),
    path('user/<int:pk>/customer-destroy/', customer_views.CustomerDestroyView.as_view(), name = 'customer-destroy'),
    # Service
    path('service/service-list/', service_views.ServiceListView.as_view(),name = 'services-list'),
    path('service/<int:pk>/service-retrieve/',service_views.ServiceRetrieveView.as_view(),name = 'service-retrieve'),
    path('service/service-create/', service_views.ServiceCreateView.as_view(),name = 'service-create'),
    path('service/<int:pk>/service-update/',service_views.ServiceUpdateView.as_view(), name = 'service-update'),
    path('service/<int:pk>/service-destroy/',service_views.ServiceDestroyView.as_view(), name = 'service-destroy'), 
    # ProfessionalService
    path('service/<int:pk>/professionalservices-create/', professionalservice_views.ProfessionalServiceCreateView.as_view(),name = 'create-professional-service'),
    path('service/professionalservices-list/',professionalservice_views.ProfessionalServiceListView.as_view(),name = 'professionalservices-list'),
    path('service/<int:pk>/professionalservices-retrieve/',professionalservice_views.ProfessionalServiceRetrieveView.as_view(), name = 'professionalservice-retrieve'),  
    path('professional-services/<int:professional_service_id>/edit/', professionalservice_views.ProfessionalServiceUpdateView.as_view(),name = 'professionalservice-update'),
    path('professional-services/<int:professional_service_id>/delete/', professionalservice_views.ProfessionalServiceDestroyView.as_view(),name = 'professionalservice-destroy'),
]