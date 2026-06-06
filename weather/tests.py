from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from weather.models import PredictionQuery

User = get_user_model()

class RainPredictionTests(TestCase):
    """
    Test suite for user registration, authentication flow, 
    dashboard access control, and the AJAX prediction API.
    """
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')
        self.predict_url = reverse('predict_api')
        
        self.username = 'testengineer'
        self.password = 'SecurePass123!'
        self.email = 'engineer@example.com'

    def test_signup_and_authentication(self):
        # 1. Signup user
        signup_response = self.client.post(self.signup_url, {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        # Verify redirect to login
        self.assertEqual(signup_response.status_code, 302)
        
        # Verify database record exists
        self.assertTrue(User.objects.filter(username=self.username).exists())

        # 2. Login user
        login_response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        # Verify redirect to dashboard
        self.assertEqual(login_response.status_code, 302)
        self.assertRedirects(login_response, self.dashboard_url)

    def test_dashboard_access_protection(self):
        # Unauthenticated GET requests should redirect to login
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

        # Authenticated GET requests should return 200 OK
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)

    @patch('weather.services.WeatherService.get_coordinates')
    @patch('weather.services.WeatherService.get_rain_prediction')
    def test_prediction_api_saves_and_returns_data(self, mock_predict, mock_coords):
        # Set up mocks for external APIs
        mock_coords.return_value = {
            'latitude': 48.8566,
            'longitude': 2.3522,
            'name': 'Paris, FR'
        }
        mock_predict.return_value = {
            'success': True,
            'total_rain': 1.25,
            'max_probability': 40.0,
            'is_rainy': True
        }

        # Setup user and log in
        user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

        # Call the API
        response = self.client.post(self.predict_url, {
            'location': 'Paris',
            'start_date': '2026-06-06',
            'end_date': '2026-06-08'
        })

        # Verify response structure
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        
        data = json_data['data']
        self.assertEqual(data['location'], 'Paris, FR')
        self.assertEqual(data['rain_sum'], 1.25)
        self.assertEqual(data['precipitation_probability'], 40.0)
        self.assertTrue(data['is_rainy'])

        # Verify prediction query is logged in DB
        self.assertEqual(PredictionQuery.objects.count(), 1)
        db_log = PredictionQuery.objects.first()
        self.assertEqual(db_log.user, user)
        self.assertEqual(db_log.location, 'Paris, FR')
        self.assertEqual(db_log.rain_sum, 1.25)
