from django.shortcuts import render
import requests
from datetime import timedelta
from .models import TemperatureRecord
from django.utils import timezone
import random

def home(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            api_key = '4b4a4879a798f31615b8ed8aa1164ad1' 
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'
            response = requests.get(url)
            weather_data = response.json()

            if 'city' in weather_data and 'list' in weather_data:
                # Clear existing records for this city
                TemperatureRecord.objects.filter(city=city).delete()

                # Extract all temperature data points
                temperature_entries = [
                    {
                        'timestamp': timezone.make_aware(timezone.datetime.utcfromtimestamp(entry['dt'])),
                        'temperature': round(entry['main']['temp'] - 273.15, 2)
                    }
                    for entry in weather_data['list']
                ]

                # Randomly select 24 temperature entries # doing this bcs this is assignment
                if len(temperature_entries) > 24:
                    temperature_entries = random.sample(temperature_entries, 24)

                # Saving selected temperature records to the database
                for entry in temperature_entries:
                    TemperatureRecord.objects.create(
                        city=city,
                        temperature=entry['temperature'],
                        timestamp=entry['timestamp']
                    )

                # here i'm temperature analysis to calculate avg, min and max
                min_temp, max_temp, avg_temp = analyze_temperature(city)

                # weather description
                description = weather_data['list'][0]['weather'][0]['description']
                
                # alert message based on the description
                alert_message = generate_alert_message(description)

                data = {
                    'city': weather_data['city']['name'],
                    'description': description,
                    'icon': weather_data['list'][0]['weather'][0]['icon'],
                    'celsius_temperature': temperature_entries[0]['temperature'] if temperature_entries else None,
                    'kelvin_temperature': weather_data['list'][0]['main']['temp'] if weather_data['list'] else None,
                    'humidity': weather_data['list'][0]['main']['humidity'] if weather_data['list'] else None,
                    'pressure': weather_data['list'][0]['main']['pressure'] if weather_data['list'] else None,
                    'min_temp': min_temp,
                    'max_temp': max_temp,
                    'avg_temp': avg_temp,
                    'alert_message': alert_message,
                }
            else:
                data['error'] = f"City '{city}' does not exist or data is unavailable."

    return render(request, 'home.html', {'data': data})

def analyze_temperature(city):
    """Analyze temperature data for the last 24 hours for the given city."""
    now = timezone.now()
    past_24_hours = now - timedelta(hours=24)
    temperature_records = TemperatureRecord.objects.filter(city=city, timestamp__gte=past_24_hours)

    if temperature_records.exists():
        temperatures = temperature_records.values_list('temperature', flat=True)
        min_temp = round(min(temperatures), 2)
        max_temp = round(max(temperatures), 2)
        avg_temp = round(sum(temperatures) / len(temperatures), 2)
    else:
        min_temp = max_temp = avg_temp = None

    return min_temp, max_temp, avg_temp

def generate_alert_message(description):
    """Generate an alert message based on the weather description."""
    alert_keywords = {
        "rain": "Carry an umbrella! It looks like it's going to rain.",
        "clear": "It's a clear day. Enjoy the sunshine!",
        "snow": "It's snowing. Drive carefully!",
        "storm": "Stormy weather ahead! Stay safe indoors.",
        "cloud": "It's cloudy. Might need a light jacket."
    }

    for keyword, message in alert_keywords.items():
        if keyword in description.lower():
            return message

    return "Weather looks fine. Have a great day!"
