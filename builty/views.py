# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from BuiltyMaker.builty.models import *
from django.template import *
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Max ,Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.db.models import F
from django import template
from tagging.models import Tag, TaggedItem
from django.core.mail import send_mail
import datetime

def index(request):
	if request.user.is_active == 1:
		return render_to_response('builty/index.html')
	else:
		return render_to_response('builty/index1.html')

def new_consignment(request):
	if request.method == 'POST':
		if request.user.is_active == 1:
			form = consignmentForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				consigner = cd['consigner']
				consigner_tin = cd['consigner_tin']
				consignee = cd['consignee']
				consignee_tin = cd['consignee_tin']
				source = cd['source']
				destination = cd['destination']
				number_of_pkgs = cd['number_of_pkgs']
				item_description = cd['item_description']
				private_mark = cd['private_mark']
				invoice_no = cd['invoice_no']
				date = cd['date']
				invoice_value = cd['invoice_value']
				actual_weight_in_kg = cd['actual_weight_in_kg']
				charged_weight_in_kg = cd['charged_weight_in_kg']
				mode = cd['mode_of_transfer']
				account = cd['account_of']
				dispatch = dispatch_status()
				dispatch.save()
				id = dispatch_status.objects.aggregate(Max('id'))
				status_id = id['id__max']
				status = dispatch_status.objects.get(id = status_id)
				save = consignment_details(account_of = account, mode_of_transfer = mode, 
				consigner = consigner ,consigner_tin = consigner_tin, 
				consignee =  consignee, consignee_tin = consignee_tin, 
				source = source, destination = destination, number_of_pkgs 
				= number_of_pkgs, item_description = item_description, 
				private_mark = private_mark, invoice_no = invoice_no, 
				date = date, invoice_value = invoice_value, 
				actual_weight_in_kg = actual_weight_in_kg, status = status,
				charged_weight_in_kg = 	charged_weight_in_kg)
				save.save()
				return render_to_response('builty/cons_ok.html')
		else :
			return render_to_response('builty/index1.html')
	else:
		form = consignmentForm()
		temp = {'form':form}
		return render_to_response('builty/new_consignment.html', 
		dict(temp.items()), context_instance=RequestContext(request))

def add_payment(request):
	if request.user.is_active == 1:
		if request.method == 'POST':
			form = paymentDetailsForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				billing_station = cd['billing_station']
				amount_paid = cd['amount_paid']
				cheque_or_dd_no = cd['cheque_or_dd_no']
				save = payment_details( billing_station = billing_station, 
				amount_paid = amount_paid, cheque_or_dd_no = cheque_or_dd_no)
				save.save()
				return render_to_response('builty/pay_ok.html')
		else:
			form = paymentDetailsForm()
			temp = {'form': form}
			return render_to_response('builty/add_payment.html', 
			dict(temp.items()), context_instance=RequestContext(request))
	else:
		return render_to_response('builty/index1.html')

def add_freight(request):
	if request.user.is_active == 1:
		if request.method == 'POST':
			form = freightDetailsForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				basic_freight = cd['basic_freight']
				barrier_charges = cd['barrier_charges']
				hamali_charges = cd['hamali_charges']
				stationary_charges = cd['stationary_charges']
				other_charges = cd['other_charges']
				id = fixed_values.objects.aggregate(Max('id'))
				s_tax = id['id__max']
				s_tax_value = fixed_values.objects.values_list('serviceTax').\
				filter(id=s_tax)
				for value in s_tax_value:
					for entry in value:
						fixed_tax = entry
				total = basic_freight + barrier_charges + hamali_charges + \
				stationary_charges + other_charges
				total_service_tax = (total * fixed_tax) / 100
				grand_total = total + total_service_tax
				id = consignment_details.objects.aggregate(Max('id'))
				consignment = id['id__max']
				cons = consignment_details.objects.get(id = consignment)
				id = payment_details.objects.aggregate(Max('id'))
				payment = id['id__max']
				pay = payment_details.objects.get(id = payment)
				save = freight_details(cons = cons, pay = pay, basic_freight 
				= basic_freight, barrier_charges = barrier_charges, 
				hamali_charges = hamali_charges, stationary_charges = 
				stationary_charges, other_charges = other_charges, 
				service_tax = total_service_tax, total = total, grand_total 
				= grand_total)
				save.save()
				temp = {'consignment':cons}
				return render_to_response('builty/freight_ok.html',
				dict(temp.items()),context_instance=RequestContext(request))
		else:
			form = freightDetailsForm()
			temp = {'form':form}
			return render_to_response('builty/add_freight.html', 
			dict(temp.items()),context_instance=RequestContext(request))
	else:
		return render_to_response('builty/index1.html')

def generate_builty(request):
	if request.user.is_active == 1:
		query = request.GET.get('q', '')
		cons_details = consignment_details.objects.get(id=query)
		freightDetails = freight_details.objects.get(id=query)
		temp = {'cons_details': cons_details, 'freight': freightDetails}
		return render_to_response('builty/gen_builty.html', 
		dict(temp.items()), context_instance=RequestContext(request))
	else:
		return render_to_response('builty/index1.html')

def consignment_register(request):
	if request.user.is_active == 1:
		cons = freight_details.objects.values('cons_id').all()
		pay = freight_details.objects.values('pay_id').all()
		details = freight_details.objects.values('cons__id','cons__consigner',
		'cons__consigner_tin','cons__consignee','cons__consignee_tin',
		'cons__date','cons__source','cons__destination','cons','cons__status__status',
		'cons__status__date').all()
		temp = {'consignment': details}
		return render_to_response('builty/cons_register.html', 
		dict(temp.items()),context_instance=RequestContext(request))
	else:
		return render_to_response('builty.index1.html')

def prev_cons(request):
	if request.user.is_active == 1:		
		query = request.GET.get('q', '')
		if query :
			result = consignment_details.objects.filter(id=query)
			temp = {'result': result, 'query': query}
			return render_to_response('builty/prev_cons.html', 
			dict(temp.items()), context_instance=RequestContext(request))
		else:
			result = []
			temp = {'result':result}
			return render_to_response('builty/prev_cons.html', 
			dict(temp.items()), context_instance=RequestContext(request))
	else:
		return render_to_response('builty/index1.html')

def dispatch(request):
	if request.user.is_active == 1:
		query = request.GET.get('q','')
		consignment = consignment_details.objects.filter(id = query)
		temp = {'consignment': consignment}
		return render_to_response('builty/dispatch_confirm.html', 
		dict(temp.items()),context_instance=RequestContext(request))
	else:
		return render_to_response('builty/index1.html')

def confirm_dispatch(request):
	if request.user.is_active == 1:
		query = request.GET.get('q', '')
		date = datetime.date.today()
		status = 1
		dispatch_status.objects.filter(id = query).update(status = status,
		date = date)
		return render_to_response('builty/dispatch_ok.html')
	else:
		return render_to_response('builty/index1.html')
