from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.template.loader import render_to_string

class FlightSearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.search_url = reverse('flight_tracker:flights_search')

    def test_index_page_loads(self):
        """Test that index page loads successfully"""
        response = self.client.get(reverse('flight_tracker:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_tracker/index.html')

    def test_empty_airport_code(self):
        """Test search with empty airport code"""
        response = self.client.post(self.search_url, {'airport_code': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_tracker/partials/flight_results.html')
        self.assertEqual(response.context['error'], "Airport code is required")

    def test_invalid_airport_code_length(self):
        """Test search with invalid airport code length"""
        response = self.client.post(self.search_url, {'airport_code': 'AB'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_tracker/partials/flight_results.html')
        self.assertEqual(response.context['error'], "Airport code must be exactly 3 letters")

    @patch('flight_tracker.services.flightapi_service.requests.get')
    def test_successful_flight_search(self, mock_get):
        """Test successful flight search"""
        # Mock response data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'airport': {
                'pluginData': {
                    'schedule': {
                        'arrivals': {
                            'data': [
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'Philippines'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'Philippines'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'South Korea'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'South Korea'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'Japan'}}}}}}
                            ]
                        }
                    },
                    'details': {
                        'name': 'Test Airport'
                    }
                }
            }
        }]
        mock_get.return_value = mock_response

        # Make the request
        response = self.client.post(self.search_url, {'airport_code': 'LAX'})
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_tracker/partials/flight_results.html')
        
        # Check context data
        self.assertIn('flights', response.context)
        self.assertIn('airport_code', response.context)
        self.assertIn('airport_name', response.context)
        
        # Verify the flights are sorted correctly
        flights = response.context['flights']
        self.assertEqual(flights[0], ('Philippines', 2))
        self.assertEqual(flights[1], ('South Korea', 2))
        self.assertEqual(flights[2], ('Japan', 1))
        
        # Verify airport information
        self.assertEqual(response.context['airport_code'], 'LAX')
        self.assertEqual(response.context['airport_name'], 'Test Airport')

    @patch('flight_tracker.services.flightapi_service.requests.get')
    def test_no_flights_found(self, mock_get):
        """Test when no flights are found"""
        # Mock empty response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'airport': {
                'pluginData': {
                    'schedule': {
                        'arrivals': {
                            'data': []
                        }
                    },
                    'details': {
                        'name': 'Test Airport'
                    }
                }
            }
        }]
        mock_get.return_value = mock_response
        
        response = self.client.post(self.search_url, {'airport_code': 'XYZ'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_tracker/partials/flight_results.html')
        self.assertEqual(response.context['flights'], [])
        self.assertEqual(response.context['airport_name'], 'Test Airport')

    @patch('flight_tracker.services.flightapi_service.requests.get')
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        response = self.client.post(self.search_url, {'airport_code': 'LAX'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_tracker/partials/flight_results.html')
        self.assertEqual(response.context['error'], "An error occurred: API Error")
