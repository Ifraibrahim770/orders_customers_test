import random
import string
#from dotenv import load_dotenv
import requests
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Customer, Order
import os


def sign_in(request):
    return render(request, 'main.html', )


class AddCustomer(APIView):
    '''Creates customer, accepts the following JSON Format, {"Name": "Example Name", "Phone":"072xxxxxxx"}'''

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        name = request.data.get('Name', False)
        phone = request.data.get('Phone', False)

        customer = Customer.objects.filter(phone__iexact=phone)
        if customer.exists():
            return Response({
                'status': False,
                'detail': 'The phone number is already registered with another user'

            })
        new_customer = Customer.objects.create(
        )
        new_customer.name = name
        new_customer.phone = phone

        new_customer.save()
        return Response({
            'status': True,
            'detail': 'The customer details were succesfully added'

        })


class AddOrder(APIView):
    '''Creates order, accepts the following JSON Format, {"Phone": "0741405186", "Items":"Eggs,7,Beans,3,Milk,4,
    Bananas,8"} '''

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        phone = request.data.get('Phone', False)
        items = request.data.get('Items', False)

        customer = Customer.objects.filter(phone__iexact=phone)
        if customer.exists():
            order_items = str(items)
            print(order_items)
            item_list = order_items.split(",")

            print(item_list)
            it = iter(item_list)
            item_dict = dict(zip(it, it))
            trans_id = get_random_string(6)

            print(item_dict)

            customer = Customer.objects.get(phone=phone)

            for key, value in item_dict.items():
                # print('The item  ' + key + ' is of  ' + str(value) + ' Amount')

                try:
                    amount = int(value)
                    new_order = Order.objects.create(
                    )
                    new_order.trans_id = trans_id
                    new_order.item = key
                    new_order.quantity = amount
                    new_order.customer = customer

                    new_order.save()
                    print('item saved ', key)

                except Exception as e:
                    return Response({
                        'status': False,
                        'Detail': "the quantity of " + key + " is badly formatted, provide a valid number"
                    })

            message = 'Your Order ' + trans_id + ' with a total of ' + str(len(
                item_dict)) + ' distinct items, has ' \
                              'been created'  # TODO SEND THIS MESSAGE TO CUSTOMERS PHONE NUMBER

            print(message)
            link = 'http://bauersms.co.ke/adminx/api.php?apikey=[API_KEY]&apitext=[Your message]&tel=[Your+Recipients]&method=sendsms'
            link = link.replace('[Your+Recipients]', customer.phone)
            link = link.replace('[Your message]', message)
            link = link.replace('[API_KEY]', os.environ.get('SMS_API_KEY'))


            print("the final link is", link)

            response = requests.post(link)
            print(response)
            return Response({
                'status': True,
                'Detail': 'Order ' + trans_id + ' for customer ' + customer.name + ' has been processed!!!'
            })
        else:
            return Response({
                'status': False,
                'Detail': 'The customer is not registered yet, '
            })


def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
