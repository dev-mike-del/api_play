import os
import requests

from django.shortcuts import render


def ip_map(request):
    is_cached = ('geodata' in request.session)
    google_key = os.getenv('GOOGLE_KEY')

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        ipstack_key = os.getenv('IPSTACK_KEY')
        response = requests.get(
            f'http://api.ipstack.com/134.201.250.155?access_key={ipstack_key}'
            ).json()
        request.session['geodata'] = response

    geodata = request.session['geodata']

    return render(request, 'ip_map.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': google_key,
        'is_cached': is_cached
    })
