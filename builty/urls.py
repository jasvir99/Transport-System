from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from BuiltyMaker.builty.models import *
urlpatterns = patterns('BuiltyMaker.builty.views',
	#	(r'^$', 'index'),
        (r'^newconsignmet','new_consignment'),
        (r'^addpayment', 'add_payment'),
        (r'^addfreight', 'add_freight'),
        (r'^genbuilty', 'generate_builty'),
        (r'^cons_register', 'consignment_register'),
		(r'^prev_cons', 'prev_cons'),
		(r'^dispatch', 'dispatch'),
)
