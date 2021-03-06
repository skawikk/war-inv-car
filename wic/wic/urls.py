"""wic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from wesol import views

urlpatterns = [
    url(r'^$', views.HomeSiteView.as_view(), name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^invoice-add/$', views.InvoicesAddNewView.as_view(), name="invoice-add"),
    url(r'^contractor-add/$', views.ContractorsNewAddView.as_view(), name="contractor-add"),
    url(r'^payment-add/$', views.PaymentAddNewView.as_view(), name="payment-add"),
    url(r'^dailyreport/$', views.DailyReportAddNewView.as_view(), name="dailyreport"),
    url(r'^product-add/$', views.ProductNewAddView.as_view(), name="product-add"),
    url(r'^products-invoice-add/$', views.ProductsInvoiceAddView.as_view(), name="products-invoice-add"),
    url(r'^stocktaking/$', views.StocktakingView.as_view(), name="stocktaking"),
]
