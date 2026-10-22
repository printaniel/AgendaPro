import pytest
from management_system.models import Service
from django.urls import reverse

CORRECT_SERVICE_NAME = 'name_test'

@pytest.mark.django_db
class TestServiceUpdateView:
    
    @pytest.fixture(autouse = True)
    def setup(self, service):
        self.service = service
        self.url = reverse('service_update', args = [service.id])
      
    def test_admin_access(self, admin_client):
        response = admin_client.patch(self.url, data = {"service_name": CORRECT_SERVICE_NAME})
        self.service.refresh_from_db()
        
        assert response.status_code == 200
        assert self.service.service_name == CORRECT_SERVICE_NAME
         
        
    def test_customer_cannot_access(self, customer_client):
        response = customer_client.patch(self.url, data = {"service_name": CORRECT_SERVICE_NAME})
        old_name = self.service.service_name
        
        self.service.refresh_from_db()
        assert response.status_code == 403
        assert self.service.service_name == old_name
    
    def test_professional_cannot_access(self, professional_client):
        response = professional_client.patch(self.url, data = {"service_name": CORRECT_SERVICE_NAME})
        old_name = self.service.service_name
                
        self.service.refresh_from_db()
        assert response.status_code == 403
        assert self.service.service_name == old_name
    
    def test_annonymus_user_cannot_accesss(self, api_client):
        response = api_client.patch(self.url, data = {"service_name": CORRECT_SERVICE_NAME})
        old_name = self.service.service_name
                        
        self.service.refresh_from_db()
        assert response.status_code == 401
        assert self.service.service_name == old_name
    
    def test_service_doesnt_exists(self, admin_client): 
        response = admin_client.patch(reverse('service_update', args=[99999]))
        
        assert response.status_code == 404
        
    def test_update_with_incorrect_data(self, admin_client):
        response = admin_client.patch(self.url, data = {"service_name": ""})
        self.service.refresh_from_db()
        
        assert response.status_code == 400
    
@pytest.mark.django_db
class TestServiceDestroyView:
    
    @pytest.fixture(autouse = True)
    def setup(self, service):
        self.url = reverse('service_destroy', args = [service.id])
    
    def test_admin_access(self, admin_client):    
        response = admin_client.delete(self.url)
        
        assert response.status_code == 204
        assert Service.objects.count() == 0
        
    def test_customer_cannot_access(self, customer_client):
        response = customer_client.delete(self.url)
                
        assert response.status_code == 403
        
    def test_professional_access(self, professional_client):
        response = professional_client.delete(self.url)
        
        assert response.status_code == 403
        
    def test_annonymus_user_access(self, api_client):
        response = api_client.delete(self.url)
        
        assert response.status_code == 401
     
    def test_service_doesnt_exists(self, admin_client):
        response = admin_client.delete(reverse('service_destroy', args=[99999999]))
        
        assert response.status_code == 404
        assert Service.objects.count() == 1