"""Temporary reproduction script - DELETE AFTER USE."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgendaPro.settings')
django.setup()

from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.runner import DiscoverRunner

setup_test_environment()
runner = DiscoverRunner(verbosity=0, interactive=False)
old_config = runner.setup_databases()

from django.contrib.auth import get_user_model
from management_system.models import Service, Appointment, ProfessionalService
from rest_framework.test import APIClient
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

cust = User.objects.create_user(username='c1', password='Str0ngPass!x', email='c@e.com', role='customer')
prof = User.objects.create_user(username='p1', password='Str0ngPass!x', email='p@e.com', role='professional')
svc = Service.objects.create(service_name='cut')
ProfessionalService.objects.create(professional=prof, service=svc, price='10.00', duration=timedelta(minutes=30), description='d')

client = APIClient()
client.force_authenticate(user=cust)

print('\n--- CASE 1: customer creates appointment WITHOUT "professional" in body ---')
try:
    r = client.post('/appointment/appointment-create/', {'service': svc.id, 'appointment_date': '2030-01-01T10:00:00Z'}, format='json')
    print('status:', r.status_code)
    print('body:', r.content[:400])
except Exception as e:
    print('RAISED:', type(e).__name__, e)

print('\n--- CASE 2: professional creates appointment WITHOUT "customer" in body ---')
client2 = APIClient()
client2.force_authenticate(user=prof)
try:
    r = client2.post('/appointment/appointment-create/', {'service': svc.id, 'appointment_date': '2030-01-01T10:00:00Z'}, format='json')
    print('status:', r.status_code)
    print('body:', r.content[:400])
except Exception as e:
    print('RAISED:', type(e).__name__, e)

print('\n--- CASE 3: user update (PATCH/PUT) without password ---')
try:
    r = client.patch(f'/user/{cust.id}/customer-update/', {'email': 'new@e.com'}, format='json')
    print('PATCH status:', r.status_code, r.content[:200])
except Exception as e:
    print('RAISED:', type(e).__name__, e)
try:
    r = client.put(f'/user/{cust.id}/customer-update/', {'email': 'new@e.com'}, format='json')
    print('PUT status:', r.status_code, r.content[:300])
except Exception as e:
    print('RAISED:', type(e).__name__, e)

runner.teardown_databases(old_config)
teardown_test_environment()