import pytest
from management_system.tests.conftest import (
    admin_client, admin,
    customer_client, customer,
    professional_client, professional,
    api_client)
from django.urls import reverse
from management_system.tests.factories import ProfessionalFactory, CustomerFactory

@pytest.mark.django_db
class TestUserListView():
   
    def test_admin_can_list_users(self, admin_client, admin):
                
        customer_db = CustomerFactory()
        profesisonal_db = ProfessionalFactory()
        url = reverse('user_list')
        
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


@pytest.mark.django_db
class TestRoleSeparetedUserListView():
    
    def test_admin_can_list_users(self, admin, admin_client):
        
        customer_db = CustomerFactory()
        professional_db = ProfessionalFactory()
        
        url = reverse('user_role_list')
        response = admin_client.get(url)
        
        print(response.data)
        
        assert response.status_code == 200
        assert response.wsgi_request.user == admin
        assert 'professionals' in response.data.keys()
        assert 'customers' in response.data.keys()
        assert len(response.data['professionals']) == 1
        assert len(response.data['customers']) == 2
           
    def test_customer_cannot_list_users(self, customer, customer_client):
        
        url = reverse('user_role_list')
        response = customer_client.get(url)
        
        assert response.status_code == 403
    
    def test_professional_cannot_list_users(self, professional, professional_client):
        
        url = reverse('user_role_list')
        response = professional_client.get(url)
                
        assert response.status_code == 403
    
    def test_annoymus_user_cannot_list_users(self, api_client):
        
        url = reverse('user_role_list')
        response = api_client.get(url)
                        
        assert response.status_code == 401