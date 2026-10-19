import pytest
from management_system.tests.factories import (
    ProfessionalFactory,
    CustomerFactory,
    ServiceFactory)
from management_system.models import User
from rest_framework.test import APIClient

@pytest.fixture
def professional(db):
    return ProfessionalFactory()

@pytest.fixture
def customer(db):
    return CustomerFactory()

@pytest.fixture
def auth_user(db):
    def _make(user = None):
        client = APIClient()
        if user is not None:
            client.force_authenticate(user)
        return client
    return _make


        
            