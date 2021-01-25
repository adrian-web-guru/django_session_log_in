from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import AirplaneCollector

import json
class TestAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        AirplaneCollector.objects.create(username="test_user",password="test12345")
        User.objects.create(username="test_admin",password="admin12345")

    ############################### MODELS ##############################
    def test_fields_airplane_collector(self):
        airplane_collector = AirplaneCollector.objects.get(id=1)
        field_label = airplane_collector._meta.get_field('username').verbose_name
        second_label = airplane_collector._meta.get_field('password').verbose_name

        self.assertEquals(field_label,'username')
        self.assertEquals(second_label,'password')

    def test_model_fields_values(self):
        airplane_collector=AirplaneCollector.objects.get(id=1)

        max_length_first = airplane_collector._meta.get_field('username').max_length
        max_length_second = airplane_collector._meta.get_field('password').max_length

        self.assertEquals(max_length_first,50)
        self.assertEquals(max_length_second,250)

    def test_str_airplane_collector(self):
        airplane_collector = AirplaneCollector.objects.get(id=1)
        initials_username = airplane_collector.username[:3]
        expected_username = f"Airplane Collector|{initials_username}"
        
        self.assertEquals(expected_username,str(airplane_collector))


    ############################## END POINTS ##############################

    # test GET /airplan-collector 
    def test_get_all_airplane_collector(self):
        client = Client()
        response = client.get('/token-endpoint/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.status_code), 'list')