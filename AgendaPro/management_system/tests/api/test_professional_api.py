import pytest
from django.urls import reverse
from  management_system.tests.factories import ProfessionalFactory

CORRECT_DATA = {
    "username": "Aniel",
    "password": "hesoyam",
    "email":"anielvarela64@gmail.com"
    
}

@pytest.mark.django_db
class TestProfessionalCreateView:
    
    def test_create_with_correct_data(self, api_client):
        
        url = reverse('professional_create')
        response = api_client.post(url, data = CORRECT_DATA)
        
        assert response.status_code == 201
        assert 'username' in response.data
        assert 'email' in response.data
        assert 'password' not in  response.data
        
    
    @pytest.mark.parametrize("payload", [
        ({"username": " ", "password": "hesoyam2", "email": "anielvarela64@gmail.com"}), # username vacio
        ({"username": "Aniel", "password": "", "email": "anielvarela64@gmail.com"}), # password vacia 
        ({"username": "Aniel", "password": "hesoyam2", "email": "anielgmail.com"}), # email sin @ 
    ])
    def test_create_with_incorrect_data(self, payload, api_client):
        url = reverse('professional_create')
        response = api_client.post(url, data = payload)
        
        assert response.status_code == 400
        

@pytest.mark.django_db
class TestProfessionalListView:
    
    def test_professional_list(self, api_client):
        
        professional0 = ProfessionalFactory()
        professional1 = ProfessionalFactory()
        
        url = reverse('professional_list')
        response = api_client.get(url)
                
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['username'] == professional0.username
        assert 'services' in response.data[0]
        assert 'password' not in response.data[0]
        assert response.data[1]['username'] == professional1.username
        assert 'services' in response.data[1]
        assert 'password' not in response.data[1]
        

