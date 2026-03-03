from django.urls import reverse
from rest_framework.test import APITestCase
from homepage.models import City

# Create your tests here.

class CitiesTestCase(APITestCase):
    def setUp(self):
        self.city_get = City.objects.create(
            name='TestCity',
            latitude = 50,
            longitude = 50,
            temperature = 50.0,
            wind_speed = 50.0,
            surface_pressure = 50.0,
            )
        self.city_post = City.objects.create(
            name='TestCity',
            latitude = 50,
            longitude = 50,
            temperature = None,
            wind_speed = None,
            surface_pressure = None,
            )
        self.url = reverse('homepage:citys')
    
    def test_get_cities(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'],self.city_get.name)

    def test_post_cities(self):
        data={
            "name":'TestCity',
            "latitude": 50,
            "longitude": 50,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data,{'name':self.city_post.name,'latitude':self.city_post.latitude,'longitude':self.city_post.longitude})
        data={
            "name":'TestCity',
            "latitude": 50,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
