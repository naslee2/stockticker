from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from .models import *
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
import bcrypt, requests, json, math


def index(request): #Index Page
  return render(request, "index.html")

def dashboard(request):
  if 'id' not in request.session:
    return redirect('/index')
  else:
    return render(request, 'dashboard.html')

def result(request):
  date = []
  open_data = []
  high = []
  low = []
  close = []
  volume = []

  if 'id' not in request.session:
    return redirect('/index')
  elif 'meta_data' not in request.session:
    return redirect('/dashboard')
  else:
    data = request.session['stock_data']
    meta = request.session['meta_data']
    for key, value in sorted(data.items()):
      date.append(key)
      for key2, value2 in sorted(value.items()):
        if key2 == '1. open':
          open_data.append(value2)
        if key2 == '2. high':
          high.append(value2)
        if key2 == '3. low':
          low.append(value2)
        if key2 == '4. close':
          close.append(value2)
        if key2 == '5. volume':
          volume.append(value2)

    plot = figure()
    plot.circle([1,2], [3,4])

    script, div = components(plot, CDN)



    return render(request, 'result.html', {"the_script": script, "the_div": div})


def update(request):
  if request.method == "POST":
    stock_options = {}
    stock_options['function'] = request.POST['time_series']
    stock_options['symbol'] = request.POST['symbol']
    stock_options['key'] = "67ZBM9BPG298O6TL"

    stock_object = requests.get("https://www.alphavantage.co/query?function="+stock_options['function']+"&symbol="+stock_options['symbol']+"&apikey="+stock_options['key'])

    obj = stock_object.json()

    if 'Meta Data' not in obj:
      return redirect('/dashboard')
    else:
      for x in obj:
        if x == 'Meta Data':
          request.session['meta_data'] = obj[x]
        elif x == 'Time Series (Daily)':
          request.session['stock_data'] = obj[x]
        elif x == 'Weekly Time Series':
          request.session['stock_data'] = obj[x]
        elif x == 'Monthly Time Series':
          request.session['stock_data'] = obj[x]
      return redirect('/result')
  else:
    return redirect('/dashboard')




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

  #################

    # stock_options = {}
    # crypto_options = {}
    # fx_options = {}

    # stock_options['function'] = "TIME_SERIES_DAILY_ADJUSTED"
    # stock_options['symbol'] = "RTN"

    # crypto_options['function'] = "DIGITAL_CURRENCY_INTRADAY"
    # crypto_options['market'] = "EUR"
    # crypto_options['symbol'] = "BTC"

    # fx_options['function'] = "CURRENCY_EXCHANGE_RATE"
    # fx_options['from_currency'] = "USD"
    # fx_options['to_currency'] = "JPY"

    # stock_object = requests.get("https://www.alphavantage.co/query?function="+stock_options['function']+"&symbol="+stock_options['symbol']+"&apikey=67ZBM9BPG298O6TL")
    # obj = stock_object.json()

    # daily_data = obj['Time Series (Daily)']
    # for x in daily_data:
    #   print "Daily Close", daily_data[x]['4. close']

    # crypto_response = serializers.serialize('json',requests.get("https://www.alphavantage.co/query?function="+crypto_data['function']+"&symbol="+crypto_options['symbol']+"&market="+crypto_options['market']+"&apikey=67ZBM9BPG298O6TL"))

    # fx_response = serializers.serialize('json',requests.get("https://www.alphavantage.co/query?function="+fx_options['function']+"&from_currency="+fx_options['from_currency']+"&to_currency="+fx_options['to_currency']+"&apikey=67ZBM9BPG298O6TL"))