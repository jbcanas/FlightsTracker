from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, MagicMock
from flight_tracker.services.flightapi_service import get_flights_by_airport

class FlightAPIServiceTests(TestCase):
    def setUp(self):
        # Ensure we have an API key for testing
        settings.FLIGHT_API_KEY = 'test_api_key'

    @patch('flight_tracker.services.flightapi_service.requests.get')
    def test_successful_api_call(self, mock_get):
        """Test successful API call with mock response"""
        # Mock response data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'airport': {
                'pluginData': {
                    'schedule': {
                        'arrivals': {
                            'data': [
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'United States'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'United States'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'Japan'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'South Korea'}}}}}},
                                {'flight': {'airport': {'origin': {'position': {'country': {'name': 'Japan'}}}}}}
                            ]
                        }
                    },
                    'details': {
                        'name': 'Los Angeles International Airport'
                    }
                }
            }
        }]
        mock_get.return_value = mock_response

        # Call the service
        flights, airport_name = get_flights_by_airport('LAX')

        # Verify the API was called correctly
        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args[1]['params']['mode'], 'arrivals')
        self.assertEqual(mock_get.call_args[1]['params']['iata'], 'LAX')

        # Verify the response processing
        expected_flights = {
            'United States': 2,
            'Japan': 2,
            'South Korea': 1
        }
        self.assertEqual(flights, expected_flights)
        self.assertEqual(airport_name, 'Los Angeles International Airport')

    @patch('flight_tracker.services.flightapi_service.requests.get')
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        # Mock API error
        mock_get.side_effect = Exception("API Error")

        # Verify error handling
        with self.assertRaises(Exception) as context:
            get_flights_by_airport('LAX')
        
        self.assertEqual(str(context.exception), "An error occurred: API Error")

    @patch('flight_tracker.services.flightapi_service.requests.get')
    def test_empty_response_handling(self, mock_get):
        """Test handling of empty API response"""
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

        # Call the service
        flights, airport_name = get_flights_by_airport('XYZ')

        # Verify empty response handling
        self.assertEqual(flights, {})
        self.assertEqual(airport_name, 'Test Airport')

    @patch('flight_tracker.services.flightapi_service.requests.get')
    def test_invalid_response_format(self, mock_get):
        """Test handling of invalid API response format"""
        # Mock invalid response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'invalid': 'format'}]
        mock_get.return_value = mock_response

        # Verify error handling for invalid format
        with self.assertRaises(Exception) as context:
            get_flights_by_airport('LAX')
        
        self.assertTrue(isinstance(context.exception, Exception))

    def test_missing_api_key(self):
        """Test handling of missing API key"""
        # Remove API key
        settings.FLIGHT_API_KEY = None

        # Verify error handling for missing API key
        with self.assertRaises(ValueError) as context:
            get_flights_by_airport('LAX')
        
        self.assertEqual(str(context.exception), "Flight API key not found in Django settings")
