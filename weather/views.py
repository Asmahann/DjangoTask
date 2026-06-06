from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from .models import PredictionQuery
from .services import WeatherService
from datetime import datetime
import json
import base64

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Renders the weather dashboard displaying the user's search form
    and their complete prediction query log history.
    """
    template_name = 'weather/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Load all history queries for this specific user
        context['history'] = PredictionQuery.objects.filter(user=self.request.user)
        return context

@method_decorator(csrf_exempt, name='dispatch')
class PredictionAPIView(View):
    """
    Class-based view API endpoint for fetching rain forecasts.
    Supports HTTP Basic Auth so it can be called directly from Postman.
    Validates input parameters, queries Open-Meteo, saves records in database,
    and returns a formatted JSON response.
    """

    def _authenticate(self, request):
        """Authenticate via session (browser) or HTTP Basic Auth (Postman/API)."""
        # Already authenticated via session
        if request.user.is_authenticated:
            return request.user
        # Try HTTP Basic Auth
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Basic '):
            try:
                decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
                username, password = decoded.split(':', 1)
                user = authenticate(request, username=username, password=password)
                return user
            except Exception:
                return None
        return None

    def post(self, request, *args, **kwargs):
        # Authenticate the request
        user = self._authenticate(request)
        if not user:
            return JsonResponse(
                {'success': False, 'error': 'Authentication required. Provide valid Basic Auth credentials.'},
                status=401,
                headers={'WWW-Authenticate': 'Basic realm="RainCast API"'}
            )
        try:
            # Handle both JSON payloads and standard POST form data
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({'success': False, 'error': 'Invalid JSON body.'}, status=400)
            else:
                data = request.POST

            location = data.get('location', '').strip()
            start_date_str = data.get('start_date', '').strip()
            end_date_str = data.get('end_date', '').strip()

            # Input validation
            if not location or not start_date_str or not end_date_str:
                return JsonResponse({
                    'success': False, 
                    'error': 'Missing required fields. Provide location, start_date, and end_date.'
                }, status=400)

            # Date format validation
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid date format. Use YYYY-MM-DD.'
                }, status=400)

            if start_date > end_date:
                return JsonResponse({
                    'success': False, 
                    'error': 'Start date cannot be after end date.'
                }, status=400)

            # 1. Fetch location coordinates
            coords = WeatherService.get_coordinates(location)
            if not coords:
                return JsonResponse({
                    'success': False, 
                    'error': f"Unable to find coordinates for location '{location}'."
                }, status=400)

            lat = coords['latitude']
            lon = coords['longitude']
            resolved_name = coords['name']

            # 2. Fetch rain prediction forecast
            prediction = WeatherService.get_rain_prediction(lat, lon, start_date_str, end_date_str)
            if not prediction.get('success', False):
                return JsonResponse({
                    'success': False, 
                    'error': prediction.get('error', 'Error contacting weather service.')
                }, status=400)

            # 3. Persist prediction log to the database
            query_record = PredictionQuery.objects.create(
                user=user,
                location=resolved_name,
                start_date=start_date,
                end_date=end_date,
                latitude=lat,
                longitude=lon,
                rain_sum=prediction['total_rain'],
                precipitation_probability=prediction['max_probability'],
                is_rainy=prediction['is_rainy']
            )

            # 4. Return results as JSON
            return JsonResponse({
                'success': True,
                'data': {
                    'id': query_record.id,
                    'location': query_record.location,
                    'start_date': start_date_str,
                    'end_date': end_date_str,
                    'latitude': lat,
                    'longitude': lon,
                    'rain_sum': query_record.rain_sum,
                    'precipitation_probability': query_record.precipitation_probability,
                    'is_rainy': query_record.is_rainy,
                    'created_at': query_record.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })

        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f"An unexpected error occurred: {str(e)}"
            }, status=500)
