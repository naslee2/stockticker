from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from .models import *
import bcrypt, requests, json

def index(request): #Index Page
  return render(request, "index.html")

def dashboard(request):
  if 'id' not in request.session:
    return redirect('/index')
  else:
    stock_options = {}
    crypto_options = {}
    fx_options = {}

    stock_options['function'] = "TIME_SERIES_DAILY_ADJUSTED"
    stock_options['symbol'] = "RTN"

    crypto_options['function'] = "DIGITAL_CURRENCY_INTRADAY"
    crypto_options['market'] = "EUR"
    crypto_options['symbol'] = "BTC"

    fx_options['function'] = "CURRENCY_EXCHANGE_RATE"
    fx_options['from_currency'] = "USD"
    fx_options['to_currency'] = "JPY"

    stock_object = requests.get("https://www.alphavantage.co/query?function="+stock_options['function']+"&symbol="+stock_options['symbol']+"&apikey=67ZBM9BPG298O6TL")
    obj = stock_object.json()

    print obj

    # crypto_response = serializers.serialize('json',requests.get("https://www.alphavantage.co/query?function="+crypto_data['function']+"&symbol="+crypto_options['symbol']+"&market="+crypto_options['market']+"&apikey=67ZBM9BPG298O6TL"))

    # fx_response = serializers.serialize('json',requests.get("https://www.alphavantage.co/query?function="+fx_options['function']+"&from_currency="+fx_options['from_currency']+"&to_currency="+fx_options['to_currency']+"&apikey=67ZBM9BPG298O6TL"))

    # context = {
    #   'stocks': stock_response,
    #   'cryptos': crypto_response,
    #   'fxs': crypto_response,
    # }
    return render(request, 'dashboard.html')

def register(request):
  if request.method == "POST":
    errors = User.objects.validator(request.POST)
    if 'valid_user' in errors:
      request.session['register_email'] = errors['valid_user'].email
      request.session['name'] = errors['valid_user'].username
      request.session['id'] = errors['valid_user'].id
      return redirect('/dashboard')
    else:
      for tag, error in errors.iteritems():
        messages.error(request, error, extra_tags=tag)
      return redirect('/index')
  else:
    return redirect('/index')

def login(request):
  if request.method == "POST":
    errors2 = User.objects.validator2(request.POST)
    if 'success' in errors2:
      request.session['username'] = errors2['success'].username
      request.session['email'] = errors2['success'].email
      request.session['id'] = errors2['success'].id
      return redirect('/dashboard')
    else:
      for tag, error in errors2.iteritems():
        messages.error(request, error, extra_tags=tag)
      return redirect('/index')
  else: 
    return redirect('/index')


def logout(request):
  request.session.clear()
  return redirect('/index')




    #   stock_data = {}
    #   crypto_data = {}
    #   fx_data = {}

    #   stock_data['function'] = "TIME_SERIES_DAILY_ADJUSTED"
    #   stock_data['symbol'] = "RTN"

    #   crypto_data['function'] = "DIGITAL_CURRENCY_INTRADAY"
    #   crypto_data['market'] = "EUR"
    #   crypto_data['symbol'] = "BTC"

    #   fx_data['function'] = "CURRENCY_EXCHANGE_RATE"
    #   fx_data['from_currency'] = "USD"
    #   fx_data['to_currency'] = "JPY"

    #   stock_response = requests.get("https://www.alphavantage.co/query?function="+stock_data['function']+"&symbol="+stock_data['symbol']+"&apikey=67ZBM9BPG298O6TL")

    #   crypto_response = requests.get("https://www.alphavantage.co/query?function="+crypto_data['function']+"&symbol="+crypto_data['symbol']+"&market="+crypto_data['market']+"&apikey=67ZBM9BPG298O6TL")

    #   fx_response = requests.get("https://www.alphavantage.co/query?function="+fx_data['function']+"&from_currency="+fx_data['from_currency']+"&to_currency="+fx_data['to_currency']+"&apikey=67ZBM9BPG298O6TL")

    #   request.session['stocks'] = stock_response
    #   request.session['cryptos'] = crypto_response
    #   request.session['fxs'] = fx_response
    #   context = {
    #     'stocks': request.session['stocks'],
    #     'cryptos': request.session['cryptos'],
    #     'fxs': request.session['fxs'],
    #   }