import pytest
from management_system.tests.factories import (
    ProfessionalFactory,
    CustomerFactory,
    AdminFactory,
    ServiceFactory)
from management_system.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def professional(db):
    return ProfessionalFactory()

@pytest.fixture
def customer(db):
    return CustomerFactory()

@pytest.fixture
def admin(db):
    return AdminFactory()

@pytest.fixture
def admin_client(admin):
    client = APIClient()
    refresh = RefreshToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION = f"Bearer {refresh.access_token}")
    return client 

@pytest.fixture
def customer_client(customer):
    client = APIClient()
    refresh = RefreshToken.for_user(customer)
    client.credentials(HTTP_AUTHORIZATION = f"Bearer {refresh.access_token}")
    return client 

@pytest.fixture
def professional_client(professional):
    client = APIClient()
    refresh = RefreshToken.for_user(professional)
    client.credentials(HTTP_AUTHORIZATION = f"Bearer {refresh.access_token}")
    return client 

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_client_maker():
    def _make(user):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION = f"Bearer {refresh.access_token}")
        return client
    return _make

@pytest.fixture
def service():
    return ServiceFactory()


        
            