from management_system.models import ProfessionalService

class ProfessionalServiceServices:

    @staticmethod
    def get_professionalservice(id):
        return ProfessionalService.objects.get(id = id)