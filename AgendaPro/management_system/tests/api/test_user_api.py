import pytest
from management_system.tests.conftest import (
    admin_client, admin,
    customer_client, customer,
    professional_client, professional,
    api_client)
from django.urls import reverse
from management_system.tests.factories import ProfessionalFactory, CustomerFactory
# py -m pytest

@pytest.mark.django_db
class TestUserList():
   
    def test_admin_can_list_users(self, admin_client, admin):
                
        customer_db = CustomerFactory()
        profesisonal_db = ProfessionalFactory()
        url = reverse('user-list')
        
        response = admin_client.get(url)
        
        assert response.status_code == 200     
        assert response.wsgi_request.user == admin
        assert response.wsgi_request.user.is_staff
        assert len(response.data) == 3
        
    def test_customer_cannot_list_users(self,customer, customer_client):        
  
        url = reverse('user_list')       
        response = customer_client.get(url)
        
        assert response.status_code == 403
        assert response.wsgi_request.user == customer
        
    
    def test_professional_cannot_list_users(self, professional, professional_client):
        
        url = reverse('user_list')       
        response = professional_client.get(url)
        
        assert response.status_code == 403
        assert response.wsgi_request.user == professional
        
           
    def test_annonymus_user_cannot_list_users(self, api_client):
        
        url = reverse('user_list')       
        response = api_client.get(url) 
        
        assert response.status_code == 401
        

    

