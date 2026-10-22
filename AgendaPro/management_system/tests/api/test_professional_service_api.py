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

@pytest.mark.django_db
class TestProfessionalServiceListView:
    
    def test_list_professional_services(self, professionalservice_maker, user_client_maker):
        # Arrange
        professional0 = ProfessionalFactory()
        professional_client = user_client_maker(professional0)
        service0 = ServiceFactory()
        service1 = ServiceFactory()
        professionalservice0 = professionalservice_maker(professional0, service0, price = 1, duration = timedelta(minutes = 1))
        professionalservice1 = professionalservice_maker(professional0, service1, price = 1, duration = timedelta(minutes = 1))
        # Act
        response = professional_client.get(reverse('professionalservice_list'))
        # Assert
        assert response.status_code == 200
        assert len(response.data) == 2
        

@pytest.mark.django_db
class TestProfessionalServiceRetrieveView:
    
    @pytest.fixture(autouse = True)
    def setUpt(self, professionalservice):
        self.professionalservice = professionalservice
        self.url = reverse('professionalservice_retrieve', args = [professionalservice.id])
    
    def test_get_professional_service(self, customer_client):
        response = customer_client.get(self.url)
        
        assert response.status_code == 200
        assert response.json()['service_name'] == self.professionalservice.service.service_name
        assert response.data['professional'] == self.professionalservice.professional.username
        assert response.data['price'] == f'{self.professionalservice.price}.00'
        assert response.data['description'] == self.professionalservice.description
        
            
    def test_non_existing_professional_service(self, customer_client):
        response = customer_client.get(reverse('professionalservice_retrieve', args = [99999999]))
        
        assert response.status_code == 404
        
class TestProfessionalServiceUpdateView:
    pass

class TestProfessionalServiceDestroyView:
    pass