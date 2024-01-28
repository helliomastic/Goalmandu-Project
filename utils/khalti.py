import requests

class Khalti:
    base_url = "https://a.khalti.com/api/v2/"
    key = "e80334d432a64b38909b698935a63b42"
    return_url = "http://127.0.0.1:5000/payment-complete"
    website_url = "http://localhost"

    @classmethod
    def construct_url(cls, path):
        return cls.base_url + path

    @classmethod
    def initiate_payment(cls, amt, purchase_ord_id, purchase_ord_name):
        path = "epayment/initiate/"
        url = cls.construct_url(path)
        return_url = cls.return_url
        payload = {
            "return_url": return_url,
            "website_url": cls.website_url,
            "amount": amt,
            "purchase_order_id": purchase_ord_id,
            "purchase_order_name": purchase_ord_name,
        }
        headers = {"Authorization": f"Key {cls.key}"}
        resp = requests.post(url,payload,headers=headers)
        resp = resp.json()
        print(resp)
        return resp['pidx'], resp['payment_url']

    @classmethod
    def verify_payment(cls, pidx):
        path = "epayment/lookup/"
        url = cls.construct_url(path)
        payload = {
            "pidx": pidx
        }
        headers = {"Authorization": f"Key {cls.key}"}
        resp = requests.post(url,payload,headers=headers)
        resp = resp.json()
        response = {}
        if resp.get('status') == 'Completed':
            response['success'] = True
            response['data'] = resp
        else:
            response['success'] = False
            response['data'] = resp
        return response
