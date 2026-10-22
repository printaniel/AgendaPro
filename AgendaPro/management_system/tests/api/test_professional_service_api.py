import pytest
from django.urls import reverse
from management_system.models import ProfessionalService
from management_system.tests.factories import ServiceFactory, ProfessionalFactory
from datetime import timedelta

@pytest.mark.django_db
class TestProfessionalServiceCreateView:
    
    @pytest.fixture(autouse = True)
    def setup(self, professional, service):
        self.correct_data = {
            "professional": professional.id,
            "service": service.id,
            "price": 1,
            "duration": timedelta(hours = 1),
            "description": 'default description'
        }
        self.url = reverse('professionalservice_create')
          
    def test_professional_can_create(self, professional_client):
        response = professional_client.post(self.url, data = self.correct_data)
        assert response.status_code == 201
        assert ProfessionalService.objects.all().count() == 1
        
    def test_customer_cannot_access(self, customer_client):
        response = customer_client.post(self.url, data = self.correct_data)
        
        assert response.status_code == 403
    
    def test_annonymus_user_cannot_access(self, api_client):
        response = api_client.post(self.url, data = self.correct_data)
        
        assert response.status_code == 401
    
    def test_non_existing_service(self, professional_client):
        self.correct_data['service'] = 999999
        data_with_non_existing_service = self.correct_data.copy()
        response = professional_client.post(self.url, data = data_with_non_existing_service)
        
        assert response.status_code == 400
    
    def test_with_incorrect_price(self, professional_client):
        self.correct_data['price'] = -10
        data_with_negative_price = self.correct_data.copy()
        response = professional_client.post(self.url, data = data_with_negative_price)
        
        assert response.status_code == 400
    
    def test_professional_already_have_service(self, professionalservice, professional_client):   
        response = professional_client.post(self.url, data = self.correct_data)
        
        assert response.status_code == 409

class TestProfessionalServiceListView:
    pass

class TestProfessionalServiceRetrieveView:
    pass

class TestProfessionalServiceUpdateView:
    pass

class TestProfessionalServiceDestroyView:
    pass