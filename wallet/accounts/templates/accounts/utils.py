import requests

def get_fx_rates():
    url = 'https://68976304250b078c2041c7fc.mockapi.io/api/wiremit/InterviewAPIS'
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return {
            'GBP': data['rates']['GBP'], 'ZAR': data['rates']['ZAR']
        }
    except:
        return {'GBP': 0.0, 'ZAR': 0.0}