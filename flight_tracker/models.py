from django.db import models

# Create your models here.

class FlightSearch(models.Model):
    airport_code = models.CharField(max_length=3)
    search_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-search_date']
    
    def __str__(self):
        return f"{self.airport_code} - {self.search_date}"
