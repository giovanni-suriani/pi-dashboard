from django.test.client import Client
from django.test import TestCase
from .views.views import *
from pi_data.models import *

# Create your tests here.

class Test_tests(TestCase):
    def setUp(self):
        # Set up any initial data for the tests
        self.tipo_participacao = TipoParticipacao.objects.create(nome="INVENTOR")
        self.pessoa = Pessoa.objects.create(nome="John Doe")
        self.pi = PropriedadeIntelectual.objects.create(titulo="Sample PI")
        
        
    def test_create_participacao(self):
        # Create a Participacao object
        participacao = Participacao.objects.create(
            tipo=self.tipo_participacao,
            pessoa=self.pessoa,
            pi=self.pi
        )
        
        # Verify that the object was created successfully
        self.assertIsNotNone(participacao.id)
        self.assertEqual(participacao.tipo, self.tipo_participacao)
        self.assertEqual(participacao.pessoa, self.pessoa)
        self.assertEqual(participacao.pi, self.pi)