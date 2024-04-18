import json
import requests

def get_average_temperature(lat, lon, start_time, end_time):
    api_key = '864c21a57f6c4e479af40e7c60666ec3'
    url = 'https://api.oikolab.com/weather'

    response = requests.get(url,
                            params={'param': ['temperature'],
                                    'lat': [lat],
                                    'lon': [lon],
                                    'start': start_time,
                                    'end': end_time},
                            headers={'api-key': api_key}
                            )

    if response.status_code == 200:
        data = response.json()
        nested_data = json.loads(data['data'])
        temperature_data = nested_data['data']
        temperatures = [entry[-1] for entry in temperature_data]
        average_temperature = sum(temperatures) / len(temperatures)
        return average_temperature
    else:
        print("Error:", response.status_code, response.text)

# Example usage:
average_temp = get_average_temperature(23.1, 114.1, "2022-01-01 00 UTC", "2022-01-01 01 UTC")
if average_temp is not None:
    print("Average Temperature:", average_temp, "°C")
