from django.shortcuts import render, redirect, reverse

from django.core.mail import BadHeaderError, send_mail

from django.http import HttpResponse,HttpResponseRedirect

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.forms import UserCreationForm

from django.core.mail import EmailMessage

from django.conf import settings

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

from .models import *

from .forms import *

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required

from django.utils.html import strip_tags

import datetime

import json

import requests

import uuid

import os

from decouple import config

# Create your views here.


def stocksandetfs(request):
	return render(request, 'investmentbankapp/stocksandetfs.html')

def smartbaskets(request):
	return render(request, 'investmentbankapp/smartbaskets.html')

def novaterrareits(request):
	return render(request, 'investmentbankapp/novaterrareits.html')

def renewableenergyprojects(request):
	return render(request, 'investmentbankapp/renewableenergyprojects.html')

def socialresponsibility(request):
	return render(request, 'investmentbankapp/socialresponsibility.html')

def ourstory(request):
	return render(request, 'investmentbankapp/ourstory.html')

def security(request):
	return render(request, 'investmentbankapp/security.html')

def retirementandiras(request):
	return render(request, 'investmentbankapp/retirementandiras.html')

def novaterraloans(request):
	return render(request, 'investmentbankapp/novaterraloans.html')

def kidscustodialportfolio(request):
	return render(request, 'investmentbankapp/kidscustodialportfolio.html')



def faq(request):
	return render(request, 'investmentbankapp/faq.html')

def portfolio(request):
	return render(request, 'investmentbankapp/portfolio.html')

def fund(request):
	return render(request, 'investmentbankapp/fund.html')

def home(request):
	return render(request, 'investmentbankapp/index.html')

def card(request):
	return render(request, 'investmentbankapp/card.html')

def stats(request):
	return render(request, 'investmentbankapp/stats.html')

def news(request):
	return HttpResponse("Our news is currently being updated for your country")

def legal(request):
	return render(request, 'investmentbankapp/legal.html')

def affiliates(request):
	return render(request, 'investmentbankapp/affiliates.html')

def oilandgas(request):
	return render(request, 'investmentbankapp/oilandgas.html')

def plan(request):
	return render(request, 'investmentbankapp/plan.html')

def otherpayment(request):
    return render(request, 'investmentbankapp/otherpayment.html')


def about(request):
	return render(request, 'investmentbankapp/about.html')


def career(request):
	return render(request, 'investmentbankapp/career.html')


def signin(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	else:
		if request.method == "POST":
			username= request.POST.get('username')
			password= request.POST.get('password')

			user= authenticate(request, username=username, password=password)

			if user is not None:
				email= User.objects.get(username=username).email
				print(email)
				template= render_to_string('investmentbankapp/loginAlert.html', {'name':username})
				plain_message= strip_tags(template)
				email_message= EmailMultiAlternatives(
					'Login alert on your account!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[email]

					)
				email_message.attach_alternative(template, 'text/html')
				email_message.send()
				login(request, user)
				return redirect('dashboard')

			else:
				messages.error(request, "username or password is incorrect")

	context={}
	return render(request, 'investmentbankapp/signin.html')


def privacy(request):
	return render(request, 'investmentbankapp/portfolio2.html')

def main_view(request, *args, **kwargs):
	code= str(kwargs.get('ref_code'))

	try:
		client = Client.objects.get(code=code)
		request.session['ref_client'] = client.id
		print('id', client.id)
	except:
		pass
	print(request.session.get_expiry_age())

	return render(request, 'investmentbankapp/main.html')


def signup(request):
	user_check = request.user.is_authenticated
	if user_check:
		return redirect('dashboard')
	client_id= request.session.get('ref_client')
	print('client_id', client_id)
	form = CreateUserForm(request.POST or None)
	if form.is_valid():
		if client_id is not None:
			recommended_by_client= Client.objects.get(id=client_id)
			recommended_by_client_email= recommended_by_client.email_address
			recommended_by_client_name= recommended_by_client.first_name
			username=form.cleaned_data.get('username')

			instance= form.save()
			registered_user= User.objects.get(id=instance.id)
			registered_client= Client.objects.get(user=registered_user)
			registered_client.recommended_by= recommended_by_client.user
			referral_template= render_to_string('investmentbankapp/referalsignupmail.html', {'name':recommended_by_client_name, 'refereed':username})
			plain_message= strip_tags(referral_template)
			email_message= EmailMultiAlternatives(
				'You refered a user using your referral link',
				plain_message,
				settings.EMAIL_HOST_USER,
				[recommended_by_client_email],
				)
			email_message.attach_alternative(referral_template, 'text/html')
			email_message.send()
			registered_client.save()

		else:
			form.save()

		username=form.cleaned_data.get('username')
		password= form.cleaned_data.get('password1')
		password_reminder= password[:1]
		password_reminder_two= password[-1:]
		email= form.cleaned_data.get('email')
		template= render_to_string('investmentbankapp/welcomeEmail.html', {'name':username,'password':password})
		plain_message= strip_tags(template)
		email_message= EmailMultiAlternatives(
			'Welcome to investmentbankapp',
			plain_message,
			settings.EMAIL_HOST_USER,
			[email],

			)
		email_message.attach_alternative(template, 'text/html')
		email_message.send()

		second_template= render_to_string('investmentbankapp/securityEmail.html', {'name': username, 'password_reminder':password_reminder, 'password_reminder_two':password_reminder_two})
		second_plain_message= strip_tags(second_template)
		second_email_message= EmailMultiAlternatives(
			"Stay updated and discover more with investmentbankapp!",
			second_plain_message,
			settings.EMAIL_HOST_USER,
			[email]
			)
		second_email_message.attach_alternative(second_template, 'text/html')
		second_email_message.send()

		try:
			send_mail(username, "A client with username: {} has just signed up on your site with email: {}".format(username, email),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
		except BadHeaderError:
			return HttpResponse("Your account has been created but you can't login at this time. please, try to login later")
		user= authenticate(username=username, password=password)
		login(request, user)
		return redirect('dashboard')
	context={'form':form}
	return render(request, 'investmentbankapp/signup.html', context)

@login_required(login_url='signin')
def dashboard(request):
	if request.user.is_staff:
		return redirect('admindashboard')
	else:
		client= request.user.client
		client_firstname= request.user.username
		client_email= request.user.email
		client_pk= client.pk
		client_deposit= client.deposit
		client_profit= client.profit
		client_bal= client.balance
		client_withdrawal= client.withdrawal
		client_date_joined= client.created
		client_code= client.code
		client_investment_plan_name= client.investment_plan_name
		client_contract= client.running_days
		time_left= float(28) - float(client_contract)
		client.save()
		client_notifications= Notification.objects.filter(client=client)
		number_of_notifications= client_notifications.count()
	context={'client': client, 'client_deposit':client_deposit, 'client_bal':client_bal,'client_profit':client_profit, 'client_date_joined':client_date_joined, 'time_left':time_left,
	'client_withdrawal':client_withdrawal, 'client_code':client_code, 'number_of_notifications':number_of_notifications, 'client_investment_plan_name':client_investment_plan_name}
	return render(request, 'investmentbankapp/dashboard.html', context)

@login_required(login_url='signin')
@staff_member_required
def admindashboard(request):
	clients= Client.objects.all()
	withdrawal_requests= Withdrawal_request.objects.all()
	transactions= Transaction.objects.all()
	clients_total= clients.count()
	withdrawal_requests_total= withdrawal_requests.count()
	transactions_total= transactions.count()
	payment= Payment_id.objects.all()
	context={'clients_total':clients_total, 'withdrawal_requests_total':withdrawal_requests_total, 'transactions_total':transactions_total,
	"clients":clients, 'payment':payment  }
	return render(request, 'investmentbankapp/adminpage.html', context)


def terms(request):
	return render(request, 'investmentbankapp/about.html')


def realestate(request):
	return render(request, 'investmentbankapp/realestate.html')


def crypto(request):
	return render(request, 'investmentbankapp/crypto.html')


def forex(request):
	return render(request, 'investmentbankapp/forex.html')


def nft(request):
	return render(request, 'investmentbankapp/nft.html')


def contact(request):
	return render(request, 'investmentbankapp/contact.html')


def stocks(request):
	return render(request, 'investmentbankapp/stocks.html')


def agriculture(request):
	return render(request, 'investmentbankapp/agriculture.html')


def gold(request):
	return render(request, 'investmentbankapp/gold.html')


def retirement(request):
	return render(request, 'investmentbankapp/retirement.html')

@login_required(login_url='signin')
def investmentPlans(request):
	return render(request, 'investmentbankapp/plan.html')

@login_required(login_url='signin')
def packageOptions(request):
	return render(request, 'investmentbankapp/deposit.html')

@login_required(login_url='signin')
def agriculturalDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/agriculturalDeposit.html', context)

@login_required(login_url='signin')
def stocksDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/StocksDepositForm.html', context)

@login_required(login_url='signin')
def cryptoDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/cryptoDepositForm.html', context)

@login_required(login_url='signin')
def oilandgasDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/oilandgasDeposit.html')

@login_required(login_url='signin')
def goldDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/goldDeposit.html', context)


@login_required(login_url='signin')
def forexDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/forexDeposit.html', context)

@login_required(login_url='signin')
def retirementDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/retirementdepositForm.html', context)

@login_required(login_url='signin')
def realestateDeposit(request):
	if request.method == 'POST':
		investment_info= request.POST.get('investment_plan')
		price_amount= request.POST.get('amount')
		pay_currency= request.POST.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {}
	return render(request, 'investmentbankapp/realestateDepositForm.html', context)

@login_required(login_url='signin')
def portfolioDeposit(request):
	form = PortfolioDepositForm(request.POST or None)
	if form.is_valid():
		investment_info= form.cleaned_data.get('investment_plan')
		price_amount= form.cleaned_data.get('amount')
		pay_currency= form.cleaned_data.get('pay_currency')
		#print(investment_info)
		#print(price_amount)
		#print(pay_currency)
		request.session['investment_info'] = investment_info
		request.session['price_amount'] = price_amount
		request.session['pay_currency'] = pay_currency
		print(request.session['investment_info'])
		print(request.session['price_amount'])
		print(request.session['pay_currency'])
		return redirect('deposit')
	context= {'form':form}
	return render(request, 'investmentbankapp/PortfolioDepositForm.html', context)

'''
@login_required(login_url='signin')
def deposit(request):
	if request.method=='GET':
		client= request.user.client
		client_name= client.first_name
		client_email= client.email_address
		#post data to create invoice for payment
		price_amount= request.session.get('price_amount')
		price_currency= "usd"
		investment_info= request.session.get('investment_info')
		investment_info_split= investment_info.split('#')
		investment_plan= investment_info_split[0]
		investment_plan_name= investment_info_split[1]
		investment_contract_duration= investment_info_split[2]
		print(investment_plan)
		print(investment_plan_name)
		pay_currency= request.session.get('pay_currency')
		generated_payment_id= '568-8534-xxx-25674'
		order_id= 'investmentbankapp Invest'
		order_description= "This is a plan subscription"
		if price_amount and pay_currency:
			#Now get the user and add the payment ID to the database as we will be using it to know their payment status
			Payment_id.objects.create(
				client=client,
				payment_id= generated_payment_id,
				price_amount= price_amount,
				investment_plan=investment_plan,
				investment_plan_name=investment_plan_name,
				contract_duration= investment_contract_duration,
				)
			template= render_to_string('investmentbankapp/pendingDepositEmail.html', {'name': client_name, 'amount':price_amount, 'transaction_id':generated_payment_id})
			plain_message= strip_tags(template)
			emailmessage= EmailMultiAlternatives(
				'Pending Deposit Order',
				plain_message,
				settings.EMAIL_HOST_USER,
				[client_email],
				)
			emailmessage.attach_alternative(template, 'text/html')
			emailmessage.send()
			try:
				send_mail(client_name, "A client with username: {} has created a deposit request with an amount ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
			except BadHeaderError:
				pass
			if str(pay_currency) == 'btc':
				return redirect(btc_deposit)

			if str(pay_currency) == 'USDTTRC20':
				return redirect(usdt_deposit)

			if str(pay_currency) == 'ltc':
				return redirect(ltc_deposit)

			if str(pay_currency) == 'doge':
				return redirect(doge_deposit)

			if str(pay_currency) == 'eth':
				return redirect(eth_deposit)

			if str(pay_currency) == 'trx':
				return redirect(trx_deposit)
	return HttpResponse('Something went wrong, please try again.')

@login_required(login_url='signin')
def btc_deposit(request):
	client= request.user.client
	client_name= request.user.username
	pay_wallet= 'btc'
	try:
		payment_info= Payment_id.objects.filter(client=client)
		last_payment_info= payment_info.last()
		price_amount= last_payment_info.price_amount
		wallet_address_query= Wallet.objects.all()
		for i in wallet_address_query:
			wallet_address = i.btc
	except:
		return HttpResponse('Bitcoin wallet address not available at the moment. Try again later.')
	if request.method == 'POST':
		try:
			send_mail(client_name, "A client with username: {} has made a deposit of ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
		except:
			pass
		return HttpResponse('Deposit Awaiting Confirmation')
	context= {'client':client, 'pay_wallet':pay_wallet, 'last_payment_info':last_payment_info, 'wallet_address':wallet_address}
	return render(request, 'investmentbankapp/btc_deposit.html', context)

@login_required(login_url='signin')
def usdt_deposit(request):
	client= request.user.client
	client_name= request.user.username
	pay_wallet= 'usdttrc20'
	try:
		payment_info= Payment_id.objects.filter(client=client)
		last_payment_info= payment_info.last()
		price_amount= last_payment_info.price_amount
		wallet_address_query= Wallet.objects.all()
		for i in wallet_address_query:
			wallet_address = i.usdttrc20
	except:
		return HttpResponse('USDT TRC20 wallet address not available at the moment. Try again later.')
	if request.method == 'POST':
		try:
			send_mail(client_name, "A client with username: {} has made a deposit of ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
		except:
			pass
		return HttpResponse('Deposit Awaiting Confirmation')
	context= {'client':client, 'pay_wallet':pay_wallet, 'last_payment_info':last_payment_info, 'wallet_address':wallet_address}
	return render(request, 'investmentbankapp/usdt_deposit.html', context)

@login_required(login_url='signin')
def ltc_deposit(request):
	client= request.user.client
	client_name= request.user.username
	pay_wallet= 'ltc'
	try:
		payment_info= Payment_id.objects.filter(client=client)
		last_payment_info= payment_info.last()
		price_amount= last_payment_info.price_amount
		wallet_address_query= Wallet.objects.all()
		for i in wallet_address_query:
			wallet_address = i.ltc
	except:
		return HttpResponse('Litecoin wallet address not available at the moment. Try again later.')
	if request.method == 'POST':
		try:
			send_mail(client_name, "A client with username: {} has made a deposit of ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
		except:
			pass
		return HttpResponse('Deposit Awaiting Confirmation')
	context= {'client':client, 'pay_wallet':pay_wallet, 'last_payment_info':last_payment_info, 'wallet_address':wallet_address}
	return render(request, 'investmentbankapp/ltc_deposit.html', context)

@login_required(login_url='signin')
def doge_deposit(request):
	client= request.user.client
	client_name= request.user.username
	pay_wallet= 'doge'
	try:
		payment_info= Payment_id.objects.filter(client=client)
		last_payment_info= payment_info.last()
		price_amount= last_payment_info.price_amount
		wallet_address_query= Wallet.objects.all()
		for i in wallet_address_query:
			wallet_address = i.doge
	except:
		return HttpResponse('Dogecoin wallet address not available at the moment. Try again later.')
	if request.method == 'POST':
		try:
			send_mail(client_name, "A client with username: {} has made a deposit of ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
		except:
			pass
		return HttpResponse('Deposit Awaiting Confirmation')
	context= {'client':client, 'pay_wallet':pay_wallet, 'last_payment_info':last_payment_info, 'wallet_address':wallet_address}
	return render(request, 'investmentbankapp/doge_deposit.html', context)

@login_required(login_url='signin')
def eth_deposit(request):
	client= request.user.client
	client_name= request.user.username
	pay_wallet= 'eth'
	try:
		payment_info= Payment_id.objects.filter(client=client)
		last_payment_info= payment_info.last()
		price_amount= last_payment_info.price_amount
		wallet_address_query= Wallet.objects.all()
		for i in wallet_address_query:
			wallet_address = i.eth
	except:
		return HttpResponse('Ethereum wallet address not available at the moment. Try again later.')
	if request.method == 'POST':
		try:
			send_mail(client_name, "A client with username: {} has made a deposit of ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
		except:
			pass
		return HttpResponse('Deposit Awaiting Confirmation')
	context= {'client':client, 'pay_wallet':pay_wallet, 'last_payment_info':last_payment_info, 'wallet_address':wallet_address}
	return render(request, 'investmentbankapp/eth_deposit.html', context)

@login_required(login_url='signin')
def trx_deposit(request):
	client= request.user.client
	client_name= request.user.username
	pay_wallet= 'trx'
	try:
		payment_info= Payment_id.objects.filter(client=client)
		last_payment_info= payment_info.last()
		price_amount= last_payment_info.price_amount
		wallet_address_query= Wallet.objects.all()
		for i in wallet_address_query:
			wallet_address = i.trx
	except:
		return HttpResponse('Tron wallet address not available at the moment. Try again later.')
	if request.method == 'POST':
		try:
			send_mail(client_name, "A client with username: {} has made a deposit of ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
		except:
			pass
		return HttpResponse('Deposit Awaiting Confirmation')
	context= {'client':client, 'pay_wallet':pay_wallet, 'last_payment_info':last_payment_info, 'wallet_address':wallet_address}
	return render(request, 'investmentbankapp/trx_deposit.html', context)
'''

@login_required(login_url='signin')
def deposit(request):
	if request.method == 'GET':
		client= request.user.client
		client_name= request.user.username
		client_email= client.email_address
		#post data to create invoice for payment
		price_amount= request.session.get('price_amount')
		price_currency= "usd"
		investment_info= request.session.get('investment_info')
		investment_info_split= investment_info.split('#')
		investment_plan= investment_info_split[0]
		investment_plan_name= investment_info_split[1]
		investment_contract_duration= investment_info_split[2]
		print(investment_plan)
		print(investment_plan_name)
		pay_currency= request.session.get('pay_currency')
		order_id= 'investmentbankapp'
		order_description= "This is a plan subscription"
		if price_amount and pay_currency:
			# Api's url link
			url= 'https://api.nowpayments.io/v1/invoice'
			payload=json.dumps({
				"price_amount": price_amount,
				"price_currency": price_currency,
				"pay_currency": pay_currency,
				"order_id": order_id,
				"order_description": order_description,
				"ipn_callback_url": "https://nowpayments.io",
				"success_url": "https://www.investmentbankapp.com.com/dashboard",
				#our success url will direct us to the get_payment_status view for balance top ups
				"cancel_url": "https://www.investmentbankapp.com.com/dashboard"
			})
			headers={'x-api-key': config('Nowpayment_key'), 'Content-Type': 'application/json'}
			response= requests.request('POST', url, headers=headers, data=payload)
			res= response.json()
			print(res)
			generated_link= res["invoice_url"]
			generated_payment_id= res["id"]
			#Now get the user and add the payment ID to the database as we will be using it to know their payment status
			Payment_id.objects.create(
				client=client,
				payment_id= generated_payment_id,
				price_amount= price_amount,
				investment_plan=investment_plan,
				investment_plan_name=investment_plan_name,
				contract_duration= investment_contract_duration,
				)
			template= render_to_string('investmentbankapp/pendingDepositEmail.html', {'name': client_name, 'amount':price_amount, 'transaction_id':generated_payment_id})
			plain_message= strip_tags(template)
			emailmessage= EmailMultiAlternatives(
				'Pending Deposit Order',
				plain_message,
				settings.EMAIL_HOST_USER,
				[client_email],
				)
			emailmessage.attach_alternative(template, 'text/html')
			emailmessage.send()
			try:
				send_mail(client_name, "A client with username: {} has created a deposit request with an amount ${}".format(client_name, price_amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
			except BadHeaderError:
				pass
			return redirect(generated_link)
	context={}
	return HttpResponse('Deposit')

@login_required(login_url='signin')
def withdrawal(request):
	client= request.user.client
	client_id= client.id
	client_username= request.user.username
	client_email= client.email_address
	client_deposit= client.deposit
	client_withdrawal= client.withdrawal
	minimum_withdrawal= Minimum_withdrawal.objects.all()
	maximum_withdrawal= Maximum_withdrawal.objects.all()
	for i in minimum_withdrawal:
		minimum_withdrawal_amount= i.minimum_withdrawal
	for i in maximum_withdrawal:
		maximum_withdrawal_amount= i.maximum_withdrawal
	print(client_deposit)
	client_profit= client.profit
	client_balance= client.balance
	client_info= Client.objects.filter(id=client_id)
	if request.method =='POST':
		withdrawal_option = request.POST.get('withdrawal_category')
		amount= request.POST.get('amount')
		withdrawal_address= request.POST.get('withdrawal_address')
		crypto= request.POST.get('crypto')
		if withdrawal_option == 'balance' and float(client_balance) > float(minimum_withdrawal_amount):
			client_current_balance= float(client_balance) - float(amount)
			client_withdrawal_balance= float(client_withdrawal) + float(amount)
			if float(client_current_balance) < 0 or float(client_balance) > float(maximum_withdrawal_amount):
				messages.error(request, "The amount requested is greater than your balance or you are exceeding the maximum withdrawal amount")
			else:
				client_update= client_info.update(balance=client_current_balance, withdrawal=client_withdrawal_balance)
				Withdrawal_request.objects.create(
					client= client,
					client_username= client_username,
					client_email= client_email,
					crypto_used_for_requesting_withdrawal= crypto,
					withdrawal_address= withdrawal_address,
					amount= amount
					)
				try:
					send_mail(client_username, "A client with username: {} has requested a withdrawal of {}".format(client_username, amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])

				except BadHeaderError:
					return HttpResponse('Something went wrong, please try again later')

				return HttpResponse('Withdrawal submitted successfully')


		if withdrawal_option == 'balance' and float(client_balance)<= 10:
			messages.error(request, "Your balance is too low for this withdrawal or your request is less than the minimum withdrawal amount")

		if withdrawal_option == 'profit' and float(client_profit) > 10:
			client_profit_balance= float(client_profit) - float(amount)
			client_withdrawal_balance= float(client_withdrawal) + float(amount)
			if client_profit_balance < 0:
				messages.error(request, "Amount requested is greater than profit")
			else:
				client_update= client_info.update(profit= client_profit_balance, withdrawal=client_withdrawal_balance)
				Withdrawal_request.objects.create(
					client= client,
					client_username= client_username,
					client_email= client_email,
					crypto_used_for_requesting_withdrawal= crypto,
					withdrawal_address= withdrawal_address,
					amount= amount
					)
				try:
					send_mail(client_username, "A client with username: {} has requested a withdrawal of {}".format(client_username, amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
				except BadHeaderError:
					return HttpResponse('Something went wrong, please try again later')
				messages.success(request, "Your withdrawal was successfully completed")

		if withdrawal_option == 'profit' and float(client_profit) <=10:
			messages.error(request, "Your profit is too low for this withdrawal" )
	context={}
	return render(request, 'investmentbankapp/withdrawal2.html', context)

@login_required(login_url='signin')
def history(request):
	client= request.user.client
	transaction= ''
	bonus= ''
	payment_id= ''
	withdrawal= ''
	total_transaction=''
	try:
		withdrawal= Withdrawal_request.objects.filter(client=client)
		total_withdrawal= withdrawal.count()
		last_five_withdrawal= withdrawal.order_by('-id')[:5][::-1]
		transaction= Transaction.objects.filter(client=client)
		total_completed_transaction= transaction.count()
		last_five_transaction= transaction.order_by('-id')[:5][::-1]
		bonus= Bonus.objects.filter(client=client)
		total_bonus= bonus.count()
		last_five_bonus= bonus.order_by('-id')[:5][::-1]
		payment_id= Payment_id.objects.filter(client=client)
		total_payment_id= payment_id.count()
		last_five_payment_id= payment_id.order_by('-id')[:5][::-1]
		total_transaction= float(transaction.count()) + float(bonus.count()) + float(payment_id.count() + float(withdrawal.count()))
	except:
		pass
	context={'withdrawal':withdrawal, 'bonus':bonus, 'payment_id':payment_id,'transaction':transaction, 'total_transaction':total_transaction,
	'total_withdrawal':total_withdrawal, 'total_bonus':total_bonus, 'total_payment_id':total_payment_id,
	'last_five_payment_id':last_five_payment_id, 'last_five_withdrawal':last_five_withdrawal, 'last_five_bonus':last_five_bonus,
	'total_completed_transaction':total_completed_transaction,'last_five_transaction':last_five_transaction }
	return render(request, 'investmentbankapp/history.html', context)

@login_required(login_url='signin')
def pending_deposit(request):
	client= request.user.client
	payment_id=''
	try:
		payment_id= Payment_id.objects.filter(client=client)
	except:
		pass
	context={'payment_id':payment_id}
	return render(request, 'investmentbankapp/pending_deposit.html', context)

@login_required(login_url='signin')
def pending_withdrawal(request):
	client= request.user.client
	withdrawal_req= ""
	try:
		withdrawal_req= Withdrawal_request.objects.filter(client=client)
	except:
		pass
	context={'withdrawal_req':withdrawal_req}
	return render(request, 'investmentbankapp/pending_withdrawal.html', context)

@login_required(login_url='signin')
def pending_bonus(request):
	client= request.user.client
	pending_bonus=''
	try:
		pending_bonus= Bonus.objects.filter(client=client)
	except:
		pass
	context={'pending_bonus':pending_bonus}
	return render(request, 'investmentbankapp/pending_bonus.html', context)

@login_required(login_url='signin')
def completed_transaction(request):
	client= request.user.client
	completed_transaction= ''
	try:
		completed_transaction= Transaction.objects.filter(client=client)
	except:
		pass
	context={'completed_transaction':completed_transaction}
	return render(request, 'investmentbankapp/completed_transaction.html', context)

@login_required(login_url='signin')
def myreferals(request):
    info= request.user
    client= Client.objects.get(user=info)
    ref_info= client.get_recommended_profiles()
    client_code= client.code
    context={'ref_info': ref_info, 'client_code':client_code}
    return render(request, 'investmentbankapp/referralprofiles.html', context)

@login_required(login_url='signin')
@staff_member_required
def confirm_withdrawal(request):
	withdrawalInfo= Withdrawal_request.objects.all()
	context={'withdrawalInfo': withdrawalInfo}
	return render(request, 'investmentbankapp/confirmwithdrawal.html', context)

@login_required(login_url='signin')
@staff_member_required
def update_withdrawal(request, pk):
	withdrawalInfo= Withdrawal_request.objects.get(id=pk)
	withdrawalInfo_id= withdrawalInfo.id
	withdrawalInfo_amount= withdrawalInfo.amount
	withdrawal_address= withdrawalInfo.withdrawal_address
	client_id= withdrawalInfo.client.id
	client= Client.objects.get(id=client_id)
	client_bal= client.deposit
	client_name= client.first_name
	client_email= client.email_address
	client_withdrawal= client.withdrawal
	template= render_to_string('investmentbankapp/withdrawalEmail.html', {'name': client_name, 'amount':withdrawalInfo_amount, 'wallet_address':withdrawal_address})
	plain_message= strip_tags(template)
	emailmessage= EmailMultiAlternatives(
		'Congratulations, Your withdrawal request has been approved!',
		plain_message,
		settings.EMAIL_HOST_USER,
		[client_email],
		)
	Transaction.objects.create(
		client=client,
		transaction_type='Withdrawal',
		amount= withdrawalInfo_amount,
		status= 'Approved',
		)
	emailmessage.attach_alternative(template, 'text/html')
	emailmessage.send()
	delete_withdrawal= withdrawalInfo.delete()
	return HttpResponse('Update withdrawal')

@login_required(login_url='signin')
@staff_member_required
def decline_wihdrawal(request, pk):
	withdrawalInfo= Withdrawal_request.objects.get(id=pk)
	withdrawalInfo_id= withdrawalInfo.id
	withdrawalInfo_amount= withdrawalInfo.amount
	withdrawal_address= withdrawalInfo.withdrawal_address
	client_id= withdrawalInfo.client.id
	client= Client.objects.get(id=client_id)
	client_info= Client.objects.filter(id=client_id)
	client_bal= client.balance
	client_name= client.first_name
	client_email= client.email_address
	client_withdrawal= client.withdrawal
	client_balance_reup= float(client_bal) + float(withdrawalInfo_amount)
	client_withdrawal_reup= float(client_withdrawal) - float(withdrawalInfo_amount)
	client_info_update= client_info.update(balance=client_balance_reup, withdrawal=client_withdrawal_reup)
	template= render_to_string('investmentbankapp/declineWithdrawalEmail.html', {'name': client_name, 'amount':withdrawalInfo_amount, 'wallet_address':withdrawal_address})
	plain_message= strip_tags(template)
	emailmessage= EmailMultiAlternatives(
		'Withdrawal request declined!',
		plain_message,
		settings.EMAIL_HOST_USER,
		[client_email],
		)
	emailmessage.attach_alternative(template, 'text/html')
	emailmessage.send()
	Transaction.objects.create(
		client=client,
		transaction_type='Withdrawal',
		amount= withdrawalInfo_amount,
		status= 'Declined'
		)
	delete_withdrawal= withdrawalInfo.delete()
	return HttpResponse('Withdrawal request declined')


@login_required(login_url='signin')
@staff_member_required
def confirm_deposit(request):
	paymentInfo= Payment_id.objects.all()
	context={'paymentInfo': paymentInfo}
	return render(request, 'investmentbankapp/confirmdeposit.html', context)


@login_required(login_url='signin')
@staff_member_required
def update_payment(request, pk):
	payment_info= Payment_id.objects.get(id=pk)
	payment_info_id= payment_info.id
	payment_info_amount= payment_info.price_amount
	payment_info_investment_plan= payment_info.investment_plan
	payment_info_investment_plan_name= payment_info.investment_plan_name
	payment_info_contract_duration= payment_info.contract_duration
	payment_info_transactionID= payment_info.payment_id
	currentDate= datetime.date.today()
	expected_return= float(payment_info_investment_plan) * float(payment_info_amount)
	packageName=''
	client_id= payment_info.client.id
	client= Client.objects.get(id=client_id)
	client_deposit= client.deposit
	client_pk= client.id
	client_name= client.first_name
	client_email= client.email_address
	print(client_deposit)
	client_info= Client.objects.filter(id=client_pk)
	newClientbal= float(payment_info_amount) + float(client_deposit)
	update_payment= client_info.update(deposit=newClientbal, running_days=0, roi=payment_info_investment_plan, investment_plan_name=payment_info_investment_plan_name, contract_duration=payment_info_contract_duration)

	template= render_to_string('investmentbankapp/confirmDepositEmail.html', {'name':client_name, 'amount':payment_info_amount, 'TransactionID':payment_info_transactionID,
		'package':payment_info_investment_plan_name, 'roi':expected_return, 'approvedDate':currentDate})
	plain_message= strip_tags(template)
	emailmessage= EmailMultiAlternatives(
		'Contract Approved',
		plain_message,
		settings.EMAIL_HOST_USER,
		[client_email],

		)
	emailmessage.attach_alternative(template, 'text/html')
	emailmessage.send()

	Transaction.objects.create(
		client=client,
		transaction_type='Deposit',
		transaction_id=payment_info_transactionID,
		investment_plan=payment_info_investment_plan_name,
		amount= payment_info_amount,
		status= 'Approved'
		)
	delete_payment_info= payment_info.delete()
	if update_payment:
		return redirect('confirm_deposit')
	return HttpResponse('Update payment')

@login_required(login_url='signin')
def account_settings(request):

	client= request.user.client

	form=ClientForm(instance=client)

	if request.method=='POST':
		form= ClientForm(request.POST, request.FILES, instance=client)
		if form.is_valid():
			form.save()

	context= {"form":form}
	return render(request, 'investmentbankapp/account_settings.html', context)

@login_required(login_url='signin')
@staff_member_required
def create_bonus(request):
	return HttpResponse('Not Yet Available')

@login_required(login_url='signin')
def use_bonus(request):
	return HttpResponse('Bonus not yet available...')

@login_required(login_url='signin')
def notifications(request):
	client= request.user.client
	try:
		client_notifications= Notification.objects.filter(client=client)
	except ObjectDoesNotExist:
		return HttpResponse('You do not have any notifications at the moment.')
	context= {'client_notifications':client_notifications}
	return render(request, 'investmentbankapp/notifications.html', context)


@login_required(login_url='signin')
def transfer_funds(request):
	if request.method=='POST':
		client= request.user.client
		client_username= request.user.username
		client_pk= client.id
		client_balance= client.balance
		client_email= client.email_address
		destination_client_account= request.POST.get('account_id')
		amount= request.POST.get('amount')
		if float(client_balance) > float(amount):
			try:
				destination_client_account_info= User.objects.get(username=destination_client_account)
				if destination_client_account_info.username != client_username:
					print(destination_client_account_info.username)
					print(destination_client_account_info.client.balance)
					newClientbal= float(client_balance) - float(amount)
					new_destination_client_account_bal= float(destination_client_account_info.client.balance) + float(amount)
					client_info= Client.objects.filter(id=client_pk)
					destination_client_account_info_query= Client.objects.filter(id=destination_client_account_info.client.id)
					updateSender= client_info.update(balance=newClientbal)
					updateReciever= destination_client_account_info_query.update(balance=new_destination_client_account_bal)
					template= render_to_string('investmentbankapp/creditMail.html', {'name':destination_client_account_info.username,
						'amount':amount, 'balance': new_destination_client_account_bal, 'sender':client_username})
					plain_message= strip_tags(template)
					emailmessage= EmailMultiAlternatives(
						'Credit Notification',
						plain_message,
						settings.EMAIL_HOST_USER,
						[destination_client_account_info.client.email_address],
						)
					emailmessage.attach_alternative(template, 'text/html')
					emailmessage.send()
					debit_template= render_to_string('investmentbankapp/debitMail.html', {'name':client_username,
						'amount':amount, 'balance': newClientbal, 'recieverName': destination_client_account_info.username})
					debit_plain_message= strip_tags(debit_template)
					debit_emailmessage= EmailMultiAlternatives(
						'Debit Notification',
						debit_plain_message,
						settings.EMAIL_HOST_USER,
						[client_email],
						)
					debit_emailmessage.attach_alternative(debit_template, 'text/html')
					debit_emailmessage.send()
					Transaction.objects.create(
						client=client,
						transaction_type= 'Debit',
						transaction_id= f'DEBIT {destination_client_account_info.username}',
						investment_plan='None',
						amount=amount,
						status='Successful',
						)
					Transaction.objects.create(
						client=destination_client_account_info.client,
						transaction_type= 'Credit',
						transaction_id= f'CREDIT {client_username}',
						investment_plan='None',
						amount=amount,
						status='Successful',
						)
					try:
						send_mail(client_username, "A client with username: {} has made a transfer of {} to another client with username {}".format(client_username, amount, destination_client_account_info.username),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
					except BadHeaderError:
						pass
						return HttpResponse('Something went wrong, please try again later')
					return HttpResponse('Transaction successfully completed')
				else:
					return HttpResponse("Quit trying to transfer funds to yourself. Otherwise we would have to block your account permanently!")
			except ObjectDoesNotExist:
				return HttpResponse('Account Does not exist')
		else:
			return HttpResponse('Sorry but you do not have sufficent account balance to carry out this transaction')
	context= {}
	return render(request, 'investmentbankapp/transferFunds.html', context)

@login_required(login_url='signin')
def video_page(request):
	try:
		videos= Video.objects.all()
	except ObjectDoesNotExist:
		return HttpResponse('There are no confrence to watch at the moment')
	context={'videos': videos}
	return render(request, 'investmentbankapp/videoPage.html', context)

@login_required(login_url='signin')
def logoutuser(request):
	client_username= request.user.username
	client_email= request.user.email
	template= render_to_string('investmentbankapp/logoutMail.html', {'name':client_username})
	plain_message= strip_tags(template)
	emailmessage= EmailMultiAlternatives(
		'Logout Notification',
		plain_message,
		settings.EMAIL_HOST_USER,
		[client_email],

		)
	emailmessage.attach_alternative(template, 'text/html')
	#emailmessage.send()
	logout(request)
	return redirect('signin')

@login_required(login_url='signin')
def reinvest(request):
	try:
		packages= Package.objects.all()
	except ObjectDoesNotExist:
		return HttpResponse('Please try depositing when our packegs are available')
	if request.method == 'POST':
		client= request.user.client
		client_id= client.id
		client_bal = client.balance
		client_email= client.email_address
		client_username= request.user.username
		client_info= Client.objects.filter(id=client_id)
		investment_plan= float(0.025)
		amount= request.POST.get('amount')
		investment_plan_name= request.POST.get('investmentPlanName')
		if (float(client_bal) > float(amount)):
			Payment_id.objects.create(
				client= client,
				payment_id= 'xxx-REINVESTMENT-xxx',
				price_amount= amount,
				investment_plan= float(investment_plan),
				investment_plan_name= investment_plan_name,
				)
			update_client= client_info.update(balance=float(client_bal) - float(amount))
			template= render_to_string('investmentbankapp/reinvestmail.html', {'name': client_username})
			plain_message= strip_tags(template)
			emailmessage= EmailMultiAlternatives(
				'Reinvestment Notification',
				 plain_message,
				 settings.EMAIL_HOST_USER,
				 [client_email]
				)
			emailmessage.attach_alternative(template, 'text/html')
			emailmessage.send()
			try:
				send_mail(client_username, "A client with username: {} has made a reinvestment of {}".format(client_username, amount),settings.EMAIL_HOST_USER, ['info@investmentbankapp.com'])
			except BadHeaderError:
				pass
			return HttpResponse('Your reinvestment was submitted successfully. Please wait...')

		else:
			messages.error(request, 'You do not have sufficent balance to make this transaction.')
	context= {'packages': packages}
	return render(request, 'investmentbankapp/reinvest.html', context)

@login_required(login_url='signin')
def loan(request):
	if request.method =='POST':
		name= request.POST.get('name')
		email= request.POST.get('email')
		phone= request.POST.get('phone')
		amount= request.POST.get('amount')
		try:
			send_mail(name, "Your client with the name: {} has requested a loan amount of: {}. Their email is {} and phone number is {}".format(name, amount,email, phone),email, ['info@investmentbankapp.com'])
			return HttpResponse('Thank you for reaching out to us, Your loan request has been sent successfully')

		except BadHeaderError:
			return HttpResponse('Bad Header Error. Please try again later.')
	return render(request, 'investmentbankapp/loan.html')

@login_required(login_url='signin')
def portfolio2(request):
	client= request.user.client
	client_firstname= request.user.username
	client_email= request.user.email
	client_pk= client.pk
	client_deposit= client.deposit
	client_profit= client.profit
	client_bal= client.balance
	client_withdrawal= client.withdrawal
	client_date_joined= client.created
	client_code= client.code
	client_investment_plan_name= client.investment_plan_name
	client_contract= client.running_days
	time_left= float(28) - float(client_contract)
	client= request.user.client
	portfolio=''
	portfolioDeposit=''
	try:
		portfolioDeposit= Transaction.objects.filter(client=client, transaction_type='Deposit')
		print(portfolioDeposit)
	except:
		pass
	context={'portfolio':portfolio, 'client_deposit':client_deposit, 'client_profit':client_profit, 'client_bal':client_bal, 'client_withdrawal':client_withdrawal,
	 'client_date_joined':client_date_joined, 'client_investment_plan_name':client_investment_plan_name, 'client_contract':client_contract, 'portfolioDeposit':portfolioDeposit }
	return render(request, 'investmentbankapp/portfoliodash.html', context)