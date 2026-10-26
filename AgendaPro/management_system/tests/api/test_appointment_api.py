import pytest
from django.urls import reverse
from datetime import timedelta, datetime
from management_system.models import Appointment
from management_system.tests.factories import ProfessionalFactory, CustomerFactory, AppointmentFactory
from django.utils import timezone
import threading
from concurrent.futures import ThreadPoolExecutor
from django.db import OperationalError, connection, IntegrityError
from management_system.services.appointments_services import AppointmentService
from django.utils.dateparse import parse_datetime


@pytest.mark.django_db
class TestAppointmentCreateView:
    
    @pytest.fixture(autouse= True)
    def setup(self, professionalservice, customer, professional, service):
        self.correct_data = {
            "professional": professional.id,
            "customer": customer.id,
            "service": service.id,
            "appointment_date":datetime.now() + timedelta(days = 1)
            }
        self.url = reverse('appointment_create')
    
    def test_not_authenticated_user_cannot_access(self, api_client):
        response = api_client.post(self.url)
        assert response.status_code == 401
    
    def test_create_with_past_date_not_allowed(self, customer_client):
        past_date = datetime.now() - timedelta(days = 1)
        self.correct_data['appointment_date'] = past_date
        data_with_past_date = self.correct_data.copy()
        
        response = customer_client.post(self.url, data = data_with_past_date)
                
        assert response.status_code == 400
        assert response.data['error']['appointment_date'][0] == 'The appointment date must be in the future'
        
    
    def test_customer_doesnt_send_professional(self, customer_client):
        self.correct_data.pop('professional')
        data_without_professional = self.correct_data
        
        response = customer_client.post(self.url, data = data_without_professional)
        assert response.status_code == 400
        assert 'professional' in response.data['error'].keys()
        
    
    def test_professional_doesnt_send_customer(self, professional_client):
        self.correct_data.pop('customer')
        data_without_customer = self.correct_data
    
        response = professional_client.post(self.url, data = data_without_customer)
        assert response.status_code == 400
        assert 'customer' in response.data['error'].keys()
    
    def test_non_existing_service(self, customer_client):
        self.correct_data['service'] = 99999999
        data_with_non_existing_service = self.correct_data.copy()
        
        response = customer_client.post(self.url, data = data_with_non_existing_service)

        assert response.status_code == 400
        assert 'service' in response.data['error'].keys()

    def test_professional_already_have_this_date_ocupated(self,appointment_maker, professional, customer, service, customer_client ):
        tomorrow_date = timezone.now() + timedelta(days = 1)
        appointment = appointment_maker(professional, customer, service, appointment_date = tomorrow_date)
        appointment.save()
        self.correct_data['appointment_date'] = tomorrow_date
        
        response = customer_client.post(self.url, data = self.correct_data)
        
        assert response.status_code == 400
    
    def test_professional_doesnt_have_service(self, customer_client):
        another_professional = ProfessionalFactory()
        self.correct_data['professional'] = another_professional.id
        response = customer_client.post(self.url, data = self.correct_data)
        
        assert response.status_code == 400
        assert response.data['error'] == 'The professional doesnot offer the service'
   
    @pytest.mark.concurrency
    @pytest.mark.django_db(transaction=True)
    def test_two_simultaneous_bookings_only_one_wins(self,
        service, professional, professionalservice, 
    ):
        customer = CustomerFactory()
        another_customer = CustomerFactory()
        """
        Dos clientes intentan reservar el mismo slot exactamente al mismo tiempo.
        Debe ganar uno y solo uno.
        """
        N = 2
        barrier = threading.Barrier(2, timeout=30)
        date = timezone.now() + timedelta(days = 1)
        def book(user):
            """Worker que ejecuta UN intento de reserva en su propio hilo."""
            try:
                barrier.wait()    #sincronizar
                AppointmentService.create_appointment(user, data = {
                    "professional": professional,
                    "service": service,
                    "appointment_date": date
                    }    
                )
                return "ok"                                 
            except IntegrityError:
                return "conflict"                          
            except OperationalError as exc:
                if "locked" in str(exc).lower():
                    return "locked"
                raise                                           
            finally:
                connection.close() 

        # Ejecutar los dos intentos concurrentemente
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(book, [customer, another_customer]))

        assert results.count("ok") == 1, (
            f"Debe ganar exactamente uno, resultados obtenidos: {results}"
        )
        assert results.count("conflict") + results.count("locked") == 1, (
            f"Debe fallar exactamente uno, resultados obtenidos: {results}"
        )

        # aserción sobre persistencia 
        persisted = Appointment.objects.filter(
            professional = professional,
            service = service,
            appointment_date = date
        ).count()
        assert persisted == 1, (
            f"Debe existir exactamente UNA cita en BD, encontradas: {persisted}"
        )

