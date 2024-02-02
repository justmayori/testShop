from webshop.settings import MONOBANK_TOKEN
import requests


headers = {
    'X-Token': MONOBANK_TOKEN,
}

redirect_url = 'http://localhost:8000/orderconf'

res = requests.post('https://api.monobank.ua/api/merchant/invoice/create', headers=headers, json = {
    'amount': 10000,
    'ccy': 840,
    'redirectUrl': redirect_url,
})

print(res.text)