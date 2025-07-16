"""
from django.core.management.base import BaseCommand

from investmentbankapp.models import Client

from django.conf import settings

import requests

import json

import random

from django.db.models import Count, F, Value

class Command(BaseCommand):
	help = 'Top users balance automatically'

	def handle(self, *args, **kwargs):
		print('Script to top up clients automatically')
		for client in Client.objects.annotate(pro= F('deposit') * F('roi') + F('profit'), bal= F('deposit') + F('profit')):
			if float(client.running_days) == 28:
				client.profit= 0
				client.deposit= 0
				client.balance= float(client.balance) + client.bal
				client.save()
				print('You have reached your maximum running days')
			else:
				client.profit= client.pro or 0
				if client.deposit > 0:
					client.running_days= float(client.running_days) + 1
				client.save()
				print('Your topup was successful')
		client= Client.objects.all()
		for i in client:
			print(i.profit)
			print(i.balance)

"""
from django.core.management.base import BaseCommand

from investmentbankapp.models import Client

from django.core.mail import EmailMessage

from django.conf import settings

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

from django.core.exceptions import ObjectDoesNotExist

from django.utils.html import strip_tags

import requests

import json

import random

from django.db.models import Count, F, Value

class Command(BaseCommand):
	help = 'Top users balance automatically'

	def handle(self, *args, **kwargs):
		print('Script to top up clients automatically')
		for client in Client.objects.annotate(pro= F('deposit') * F('roi') + F('profit'), bal= F('deposit') + F('profit')):
			if client.running_days > 0 and float(client.running_days) == float(client.contract_duration):
				client.profit= 0
				client.deposit= 0
				client.running_days= 0
				client.contract_duration= 0
				client.balance= float(client.balance) + client.bal
				client.save()
				client_username= client.user.username
				client_email= client.user.email
				template= render_to_string('investmentbankapp/email_top_up_complete.html', {'name':client_username})
				plain_message= strip_tags(template)
				emailmessage= EmailMultiAlternatives(
					'Contract Notification',
					plain_message,
					settings.EMAIL_HOST_USER,
					[client_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				print('You have reached your maximum running days, and email has been sent.')

			if client.deposit > 0 and client.running_days > 0 and float(client.running_days) < float(client.contract_duration):
				client.profit= client.pro or 0
				client.running_days= float(client.running_days) + 1
				client_username= client.user.username
				client_email= client.user.email
				credit_template= render_to_string('investmentbankapp/email_top_up.html', {'name':client_username})
				credit_plain_message= strip_tags(credit_template)
				credit_emailmessage= EmailMultiAlternatives(
					'Contract Notification',
					credit_plain_message,
					settings.EMAIL_HOST_USER,
					[client_email],
					)
				credit_emailmessage.attach_alternative(credit_template, 'text/html')
				credit_emailmessage.send()
				client.save()
				print('Your topup was successful')
			else:
			    pass
		client= Client.objects.all()
		for i in client:
			print(i.profit)
			print(i.balance)
