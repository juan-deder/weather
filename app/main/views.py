import requests
from datetime import datetime
from flask import request, make_response
from . import main
from .. import cache, config


@main.route('/weather')
@cache.cached(query_string=True)
def weather():
    params = {'q': ','.join(request.args.values()), 'appid': config['api_id']}
    r = requests.get(config['api_url'], params=params).json()

    if (code := r.pop('cod')) == 200:
        r = {
            'location_name': f"{r['name']}, {r['sys']['country']}",
            'temperature': f"{round((r['main']['temp'] - 32) * 5 / 9)} °C",
            'wind': f"{r['wind']['speed']} m/s",
            'cloudiness': r['weather'][0]['description'].capitalize(),
            'pressure': f"{r['main']['pressure']} hpa",
            'humidity': f"{r['main']['humidity']}%",
            'sunrise': datetime.fromtimestamp(
                r['sys']['sunrise']).strftime('%H:%m'),
            'sunset': datetime.fromtimestamp(
                r['sys']['sunset']).strftime('%H:%m'),
            'geo_coordinates': '[%.2f, %.2f]' % tuple([*r['coord'].values()]),
            'requested_time': str(datetime.fromtimestamp(
                r['dt']).strftime('%Y-%m-%d %H:%M:%S'))
        }
    return make_response(r, code, {'Content-Type': 'application/json'})
