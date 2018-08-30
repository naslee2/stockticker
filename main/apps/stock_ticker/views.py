from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from .models import *
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.layouts import gridplot, column
from bokeh.models import ColumnDataSource, HoverTool,DatetimeTickFormatter, Slider, CustomJS
import bcrypt, requests, json
import pandas as pd
import numpy as np

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
    return HttpResponse("Invalid Request!")
  else:
    data = request.session['stock_data']
    meta = request.session['meta_data']
    for key, value in sorted(data.items()):
      date.append(str(key))
      for key2, value2 in sorted(value.items()):
        if key2 == '1. open':
          open_data.append(float(value2))
        if key2 == '2. high':
          high.append(float(value2))
        if key2 == '3. low':
          low.append(float(value2))
        if key2 == '4. close':
          close.append(float(value2))
        if key2 == '5. volume':
          volume.append(int(value2))

    np_date = np.array(date, dtype=np.datetime64)
    source = ColumnDataSource(data=dict(
      date=np_date,
      close=close,
      volume=volume
    ))

    plot = figure(plot_height=600, plot_width=1000, x_axis_type="datetime",toolbar_location="above", title="Closing Prices for "+meta['2. Symbol']+" at "+meta['3. Last Refreshed'])
    plot.grid.grid_line_alpha=0.3
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Price'
    plot.add_tools(HoverTool(
    tooltips=[
        ('date','@date{%F}'),
        ("Close","@close"),
        ("Volume", "@volume"),
    ],

    formatters={
        'date':'datetime', # use 'datetime' formatter for 'date' field
    },
    mode='vline'
    ));

    plot.line(x='date', y='close', color='#A6CEE3', source=source)
   
    script, div = components(plot, CDN)
    return render(request, 'stock_result.html', {'the_script': script, 'the_div': div})


def update(request):
  if request.method == "POST":
    stock_options = {}
    stock_options['function'] = request.POST['time_series']
    stock_options['symbol'] = request.POST['symbol']
    stock_options['key'] = "67ZBM9BPG298O6TL"

    stock_object = requests.get("https://www.alphavantage.co/query?function="+stock_options['function']+"&symbol="+stock_options['symbol']+"&apikey="+stock_options['key'])

    obj = stock_object.json()

    if 'Meta Data' not in obj:
      return HttpResponse("Invalid Request!")
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
      print "@@@@@@@@@@@@ /result"
      return redirect('/result')
  else:
    print "@@@@@@@@@@@@ /dashboard"
    return HttpResponse("Invalid Request!")
    # return redirect('/dashboard')



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
