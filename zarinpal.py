# -*- coding: utf-8 -*-

# Sample Flask ZarinPal WebGate with SOAP
# Zarinpal addon for flask Using Client (zeep)

from flask import Flask, url_for, redirect, request
from zeep.client import Client


app = Flask(__name__)
app.secret_key = 'SeCRet120!!'

MMERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  # Required - Merchant code
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 2000  # Amount will be based on Toman  Required
description = u'your description'  # Required
email = 'your email'  # Optional
mobile = 'your number'  # Optional


@app.route('/request/')
def send_request():
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           amount,
                                           description,
                                           email,
                                           mobile,
                                           str(url_for('verify', _external=True)))
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return 'خطا در پرداخت'


@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    client = Client(ZARINPAL_WEBSERVICE)
    if request.args.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.args['Authority'],
                                                    amount)
        if result.Status == 100:
            return 'پرداخت با موفقیت انجام شد , کد پیگیری شما : ' + str(result.RefID)
        elif result.Status == 101:
            return 'سفارش شما ثبت شد : ' + str(result.Status)
        else:
            return 'پرداخت با خطا رو برو شد , کد خطا : ' + str(result.Status)
    else:
        return 'پرداخت توسط کاربر لغو شد'


if __name__ == '__main__':
    app.run(debug=True)
