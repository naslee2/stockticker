from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
      url(r'^', include('apps.stock_ticker.urls')) # And now we use the include function to pull in our first_app.urls...
  ]
