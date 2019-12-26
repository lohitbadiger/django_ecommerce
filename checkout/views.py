import stripe
import uuid
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView
# Create your views here.
# def checkout(request):
    
# 	# Checkout view
# 	form = BillingForm
	
# 	order_qs = Order.objects.filter(user= request.user, ordered=False)
# 	order_items = order_qs[0].orderitems.all()
# 	order_total = order_qs[0].get_totals() 
# 	context = {"form": form, "order_items": order_items, "order_total": order_total}
	
# 	return render(request, 'checkout/index.html', context)

def checkout(request):
    
	# Checkout view
	form = BillingForm
	
	order_qs = Order.objects.filter(user= request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total = order_qs[0].get_totals() 
	context = {"form": form, "order_items": order_items, "order_total": order_total}
	# Getting the saved saved_address
	saved_address = BillingAddress.objects.filter(user = request.user)
	if saved_address.exists():
		savedAddress = saved_address.first()
		context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress}
	if request.method == "POST":
		saved_address = BillingAddress.objects.filter(user = request.user)
		if saved_address.exists():

			savedAddress = saved_address.first()
			form = BillingForm(request.POST, instance=savedAddress)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
		else:
			form = BillingForm(request.POST)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
				
	return render(request, 'checkout/index.html', context)


# Import Stripe
import stripe
from django.conf import settings



def payment(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    order_total = order_qs[0].get_totals()
    totalCents = float(order_total * 100)
    total = round(totalCents, 2)
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=total,
            currency='usd',
            description=order_qs,
            source=request.POST['stripeToken'])
        print(charge)
    return render(request, 'checkout/payment.html', {"key": key, "total": total})





def charge(request): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')


def oderView(request):
    
	try:
		orders = Order.objects.filter(user=request.user, ordered=True)
		context = {
			"orders": orders
		}
	except:
		messages.warning(request, "You do not have an active order")
		return redirect('/')
	return render(request, 'checkout/order.html', context)