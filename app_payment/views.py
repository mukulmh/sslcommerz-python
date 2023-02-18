from django.shortcuts import render, redirect
from sslcommerz_python.payment import SSLCSession
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import secrets
import string
from .models import Transactions
from django.core.serializers import serialize


@csrf_exempt
def Card(request):
    # objs = serialize('json', Transactions.objects.filter(status='SUCCESS'))
    # print(objs)
    return render(request, 'card.html')


def Checkout(request):
    transaction_id = ''.join(secrets.choice(
        string.ascii_uppercase + string.digits) for i in range(18))
    amount = 100

    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='devel634786da0d226',
                            sslc_store_pass='devel634786da0d226@ssl')

    mypayment.set_urls(success_url='http://127.0.0.1:8000/status', fail_url='http://127.0.0.1:8000/status',
                       cancel_url='http://127.0.0.1:8000/status', ipn_url='http://127.0.0.1:8000/status')

    mypayment.set_product_integration(tran_id=transaction_id, total_amount=amount, currency='BDT', product_category='clothing',
                                      product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')

    mypayment.set_customer_info(name='John Doe', email='johndoe@email.com', address1='demo address',
                                address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01711111111')

    mypayment.set_shipping_info(shipping_to='demo customer', address='demo address',
                                city='Dhaka', postcode='1209', country='Bangladesh')

    # If you want to post some additional values
    mypayment.set_additional_values(
        value_a='cusotmer@email.com', value_b='portalcustomerid', value_c='1234', value_d='uuid')

    response_data = mypayment.init_payment()
    print(response_data)
    if (response_data['status'] == 'SUCCESS'):
        Transactions.objects.create(
            tran_id=transaction_id, amount=amount, status='PENDING')
        return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def Status(request):
    request_obj = request.POST
    print(request_obj)
    try:
        pay_obj = Transactions.objects.get(tran_id=request_obj['tran_id'])
    except:
        messages.error(request, 'Transaction ID Not matched! ')
        return redirect('index')

    if request_obj['status'] == 'FAILED':
        pay_obj.status = 'FAILED'
        pay_obj.card_type = request_obj['card_type']
        pay_obj.currency = request_obj['currency']
        pay_obj.card_no = request_obj['card_no']
        pay_obj.card_issuer = request_obj['card_issuer']
        pay_obj.card_brand = request_obj['card_brand']
        pay_obj.card_sub_brand = request_obj['card_sub_brand']
        pay_obj.card_issuer_country = request_obj['card_issuer_country']
        pay_obj.card_issuer_country_code = request_obj['card_issuer_country_code']
        pay_obj.currency_rate = request_obj['currency_rate']
        pay_obj.base_fair = request_obj['base_fair']
        pay_obj.bank_tran_id = request_obj['bank_tran_id']
        pay_obj.save()
        messages.error(request, 'Your payment has Failed!')

    if request_obj['status'] == 'VALID':
        pay_obj.status = 'SUCCESS'
        pay_obj.card_type = request_obj['card_type']
        pay_obj.val_id = request_obj['val_id']
        pay_obj.currency = request_obj['currency']
        pay_obj.store_amount = request_obj['store_amount']
        pay_obj.card_no = request_obj['card_no']
        pay_obj.card_issuer = request_obj['card_issuer']
        pay_obj.card_brand = request_obj['card_brand']
        pay_obj.card_sub_brand = request_obj['card_sub_brand']
        pay_obj.card_issuer_country = request_obj['card_issuer_country']
        pay_obj.card_issuer_country_code = request_obj['card_issuer_country_code']
        pay_obj.currency_rate = request_obj['currency_rate']
        pay_obj.base_fair = request_obj['base_fair']
        pay_obj.bank_tran_id = request_obj['bank_tran_id']
        pay_obj.risk_title = request_obj['risk_title']
        pay_obj.save()
        messages.success(request, 'Your Payment is Successfull.')
    return redirect('index')
