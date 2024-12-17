from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.flightapi_service import get_flights_by_airport
from ..models import FlightSearch
from .serializers import AirportCodeSerializer, FlightResultSerializer

class FlightsByCountryView(APIView):
    def post(self, request):
        """Get flights by country for a given airport code."""
        serializer = AirportCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        airport_code = serializer.validated_data['airport_code']
        
        try:
            # Save the search
            FlightSearch.objects.create(airport_code=airport_code)
            
            # Get flight data
            country_flights = get_flights_by_airport(airport_code)
            
            # Format the response
            results = [
                {'country': country, 'num_flights': count}
                for country, count in country_flights.items()
            ]
            
            # Sort by number of flights in descending order
            results.sort(key=lambda x: x['num_flights'], reverse=True)
            
            response_serializer = FlightResultSerializer(data=results, many=True)
            response_serializer.is_valid()
            
            return Response(response_serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
