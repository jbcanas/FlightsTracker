from rest_framework import serializers
from ..models import FlightSearch

class AirportCodeSerializer(serializers.Serializer):
    airport_code = serializers.CharField(
        max_length=3,
        min_length=3,
        help_text="3-letter IATA airport code"
    )
    
    def validate_airport_code(self, value):
        return value.upper()

class FlightResultSerializer(serializers.Serializer):
    country = serializers.CharField()
    num_flights = serializers.IntegerField()
