import pytest
from django.urls import reverse
from management_system.tests.factories import ProfessionalFactory
from management_system.tests.conftest import admin, admin_client, user_client_maker

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
        

@pytest.mark.django_db
class TestProfessionalRetrieveView():
    
    def test_professional_retrieve(self, api_client):
        professional0 =  ProfessionalFactory()
        url = reverse('professional_retrieve', args = [professional0.id])
        
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data['username'] == professional0.username
        assert 'services' in response.data
        assert 'password' not in response.data
        assert 'email'  not in response.data
        

@pytest.mark.django_db        
class TestProfessionalUpdateView:
    
    @pytest.fixture(autouse = True)
    def setup(self, db, professional):
        self.new_username = 'Raul'
        self.new_password = 'croquetas'
        self.professional = professional
        self.url = reverse('professional_update', args = [professional.id])
    
    def test_owner_can_update(self, professional, professional_client):
        
        response = professional_client.patch(self.url, data = {"username": self.new_username, "password": self.new_password })       
        professional.refresh_from_db()
        
        assert response.status_code == 200
        assert professional.username == self.new_username
        assert professional.check_password(self.new_password)
    
    def test_admin_can_update(self, admin_client, professional):
        
        response = admin_client.patch(self.url, data = {"username": self.new_username, "password": self.new_password })       
        professional.refresh_from_db()
                
        assert response.status_code == 200
        assert professional.username == self.new_username
        assert professional.check_password(self.new_password)
    
    def test_customer_cannot_udpate(self, professional, customer_client):
        
        old_username = professional.username
        old_password = professional.raw_password
                
        response = customer_client.patch(self.url, data = {"username": self.new_username, "password": self.new_password })              
        professional.refresh_from_db()
        
        assert response.status_code == 403
        assert professional.username == old_username
        assert professional.check_password(old_password)
    
    def test_another_professional_cannot_update(self, professional_client):
        
        professional_to_update = ProfessionalFactory()
        old_username = professional_to_update.username
        old_password = professional_to_update.raw_password
        
        url = reverse('professional_update', args = [professional_to_update.id])
        response = professional_client.patch(url, data = {"username": self.new_username, "password": self.new_password })
                  
        professional_to_update.refresh_from_db()
          
        assert response.status_code == 403 
        assert professional_to_update.username == old_username
        assert professional_to_update.check_password(old_password)    
        
    @pytest.mark.parametrize("payload", [
            ({"username": " ", "password": "hesoyam2", "email": "anielvarela64@gmail.com"}), # username vacio
            ({"username": "Aniel", "password": "", "email": "anielvarela64@gmail.com"}), # password vacia 
            ({"username": "Aniel", "password": "hesoyam2", "email": "anielgmail.com"}), # email sin @ 
        ])
    def test_update_with_incorrect_data(self, payload, professional_client):
        response = professional_client.patch(self.url, data = payload)        
        assert response.status_code == 400
        
    def test_annonymus_cannot_update(self, api_client):
        response = api_client.patch(self.url, data = {"username": self.new_username, "password": self.new_password})
        
        assert response.status_code == 401
   
@pytest.mark.django_db     
class TestProfessionalDestroyView:
    
    @pytest.fixture(autouse = True)
    def setup(self, professional):
        self.professional = professional
        self.url = reverse('professional_destroy', args = [professional.id])
    
    def test_owner_can_cancel(self, professional_client):

        response = professional_client.delete(self.url)       
        self.professional.refresh_from_db()
        
        assert response.status_code == 204
        assert response.wsgi_request.user == self.professional
        assert self.professional.is_active == False
    
    def test_admin_can_cancel(self, admin_client):
        
        response = admin_client.delete(self.url)
        self.professional.refresh_from_db()
        
        assert response.status_code == 204
        assert self.professional.is_active == False
    
    def test_customer_cannot_cancel(self, customer_client):
        
        response = customer_client.delete(self.url)
        self.professional.refresh_from_db()
        
        assert response.status_code == 403
        assert self.professional.is_active == True
    
    def test_another_professional_cannot_cancel(self, user_client_maker):
        
        another_professional = ProfessionalFactory()
        another_professional_client = user_client_maker(another_professional)
        
        response = another_professional_client.delete(self.url)
        self.professional.refresh_from_db()
        assert response.status_code == 403
        assert self.professional.is_active == True