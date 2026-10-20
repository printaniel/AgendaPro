import pytest
from django.urls import reverse
from management_system.tests.conftest import (
    api_client,
    admin_client,
    customer_client, customer,
    professional_client,
    user_client_maker)
from management_system.tests.factories import CustomerFactory
from django.urls import reverse

CORRECT_DATA = {
    "username": "Aniel",
    "password": "hesoyam",
    "email":"anielvarela64@gmail.com"
    
}

@pytest.mark.django_db
class TestCustomerCreateView:
    
    def test_create_with_correct_data(self, api_client):         
        url = reverse('customer_create')
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
        url = reverse('customer_create')
        response = api_client.post(url, data = payload)
        
        assert response.status_code == 400
        
class TestCustomerListView:
    
    @pytest.fixture(autouse = True)
    def setup(self):
        self.url = reverse('user_list')
        
    def test_admin_access(self, admin_client):     
        customer1 = CustomerFactory()
        customer2 = CustomerFactory()
        
        response = admin_client.get(self.url)      
        assert response.status_code == 200
        assert len(response.data) == 3
    
    
    def test_customer_cannot_access(self, customer_client):      
        response = customer_client.get(self.url)
        assert response.status_code == 403
    
    def test_professional_cannot_access(self, professional_client):  
        response = professional_client.get(self.url)         
        assert response.status_code == 403
    
    def test_annonymus_user_cannot_access(self, api_client):       
        response = api_client.get(self.url)                
        assert response.status_code == 401

class TestCustomerRetrieveView:
    
    @pytest.fixture(autouse = True)
    def setup(self, customer):
        self.customer = customer
        self.url = reverse('customer_retrieve', args = [customer.id])
    
    def test_owner_access(self, customer_client):     
        response = customer_client.get(self.url)
        
        assert response.status_code == 200
        assert response.data['username'] == self.customer.username
        assert response.data['email'] == self.customer.email
        assert 'password' not in response.data 
    
    def test_admin_acess(self, admin_client):
        response = admin_client.get(self.url)
                
        assert response.status_code == 200
        assert response.data['username'] == self.customer.username
        assert response.data['email'] == self.customer.email
        assert 'password' not in response.data
    
    def test_another_customer_cannot_access(self, user_client_maker):   
        another_customer_client = user_client_maker(CustomerFactory())
        response = another_customer_client.get(self.url)
        
        assert response.status_code == 403
    
    def test_professional_cannot_access(self, professional_client):
        response = professional_client.get(self.url)
                
        assert response.status_code == 403
     
    def test_annonymus_user_cannot_access(self, api_client):
        response = api_client.get(self.url)
                        
        assert response.status_code == 401
        
    def test_non_existing_customer(self, admin_client):
        response = admin_client.get(reverse('customer_retrieve', args = [999999]))
        assert response.status_code == 404
class TestCustomerUpdateView:
    
    @pytest.fixture(autouse = True)
    def setup(self, customer):
        self.customer = customer
        self.new_username = "Raul"
        self.new_password = "croquetas"
        self.url = reverse('customer_update', args = [customer.id])
    
    def test_owner_access(self, customer_client):     
        response = customer_client.patch(self.url, data = {"username": self.new_username, "password": self.new_password})
        
        self.customer.refresh_from_db()
        assert response.status_code == 200
        assert self.customer.username == self.new_username
        assert self.customer.check_password(self.new_password)
        assert self.customer.password != self.new_password
    

    def test_admin_acess(self, admin_client):
        response = admin_client.patch(self.url, data = {"username": self.new_username, "password": self.new_password})
                
        self.customer.refresh_from_db()
        assert response.status_code == 200
        assert self.customer.username == self.new_username
        assert self.customer.check_password(self.new_password)
        assert self.customer.password != self.new_password
    
    def test_another_customer_cannot_access(self, user_client_maker):   
        another_customer_client = user_client_maker(CustomerFactory())
        response = another_customer_client.patch(self.url)
        
        assert response.status_code == 403
    
    def test_professional_cannot_access(self, professional_client):
        response = professional_client.patch(self.url)
                
        assert response.status_code == 403
     
    def test_annonymus_user_cannot_access(self, api_client):
        response = api_client.patch(self.url)
                        
        assert response.status_code == 401
        
    def test_non_existing_customer(self, admin_client):
        response = admin_client.patch(reverse('customer_update', args = [999999]))

        assert response.status_code == 404
     
    @pytest.mark.parametrize("payload", [
        ({"username": " ", "password": "hesoyam2", "email": "anielvarela64@gmail.com"}), # username vacio
        ({"username": "Aniel", "password": "", "email": "anielvarela64@gmail.com"}), # password vacia 
        ({"username": "Aniel", "password": "hesoyam2", "email": "anielgmail.com"}), # email sin @ 
        ])   
    def test_update_with_incorrect_data(self,payload ,admin_client):
        response = admin_client.patch(self.url, data = payload )
        
        assert response.status_code == 400

@pytest.mark.django_db
class TestCustomerDestroyView:
     
    @pytest.fixture(autouse = True)
    def setup(self, customer):
        self.customer = customer
        self.url = reverse('customer_cancel', args = [customer.id])
        
    def test_owner_access(self, customer_client):     
        response = customer_client.delete(self.url)
            
        self.customer.refresh_from_db()
        assert response.status_code == 204
        assert self.customer.is_active == False
        
    
    def test_admin_acess(self, admin_client):
        response = admin_client.delete(self.url)
                    
        self.customer.refresh_from_db()
        assert response.status_code == 204
        assert self.customer.is_active == False
        
    def test_another_customer_cannot_access(self, user_client_maker):   
        another_customer_client = user_client_maker(CustomerFactory())
        response = another_customer_client.delete(self.url)
        
        self.customer.refresh_from_db()  
        assert response.status_code == 403
        assert self.customer.is_active == True
        
    def test_professional_cannot_access(self, professional_client):
        response = professional_client.delete(self.url)
        
        self.customer.refresh_from_db()          
        assert response.status_code == 403
        assert self.customer.is_active == True
         
    def test_annonymus_user_cannot_access(self, api_client):
        response = api_client.delete(self.url)
        
        self.customer.refresh_from_db()                    
        assert response.status_code == 401
        assert self.customer.is_active == True
            
    def test_non_existing_customer(self, admin_client):
        response = admin_client.delete(reverse('customer_cancel', args = [999999]))
    
        assert response.status_code == 404


