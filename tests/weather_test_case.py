import os
from unittest import TestCase
from app import create_app


class WeatherTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ['CACHE_TYPE'] = 'null'
        app = create_app()
        cls.client = app.test_client()

    def test_not_found_city_response(self):
        query_string = {'city': 'Gotham City', 'country': 'US'}
        response = self.client.get('/weather', query_string=query_string)
        self.assertEqual(404, response.status_code)
        self.assertDictEqual({'message': 'city not found'}, response.json)

    def test_response_object_structure(self):
        query_string = {'city': 'Medellin', 'country': 'CO'}
        response = self.client.get('/weather', query_string=query_string)
        self.assertEqual(200, response.status_code)
        keys = 'location_name', 'temperature', 'wind', 'cloudiness', \
               'pressure', 'humidity', 'sunrise', 'sunset', 'geo_coordinates', \
               'requested_time'
        for key in keys:
            self.assertIn(key, response.json)

    def test_location_name_matches_query_params(self):
        query_string = {'city': 'Bogota', 'country': 'CO'}
        response = self.client.get('/weather', query_string=query_string)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Bogotá, CO', response.json['location_name'])
