# Django-weatheranalysis

# Weather Analysis System using Django

## Description
The Weather Analysis System is a web application developed using Django, designed to provide real-time weather information and perform temperature analysis. The system integrates with the OpenWeatherMap API to fetch weather data for any city, displaying detailed information such as temperature, humidity, pressure, and weather descriptions. Additionally, the application stores 24-hour weather data in a PostgreSQL database and calculates daily minimum, maximum, and average temperatures.

## Key Features
- **Real-Time Weather Data:** Integrated with the OpenWeatherMap API to provide up-to-date weather conditions for any city.
- **Historical Data Storage:** The application stores 24-hour weather data in a PostgreSQL database, allowing for historical data analysis.
- **Temperature Analysis:** Displays daily minimum, maximum, and average temperatures based on the stored data.
- **Responsive Design:** The user interface is designed to be responsive, providing an optimal experience across different devices.
- **Custom Icon Integration:** The application includes custom weather icons to enhance the visual presentation.
- **Deployment:** Deployed on Render, addressing challenges related to static file management and database configuration.

## Technologies Used
- **Backend:** Django, Python, PostgreSQL
- **Frontend:** HTML, CSS
- **API Integration:** OpenWeatherMap API
- **Deployment:** Render
- **Version Control:** Git

## How to Run the Project
**Clone the Repository:**
   git clone https://github.com/yourusername/weather-analysis.git
   cd weather-analysis
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

