from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Avg
from django.shortcuts import get_object_or_404

def index(request):
    return render(request,'index.html')


def register(request):
    print('hi')
    errors = Merchant.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        request.session['username'] = first_name +" " + last_name
        request.session['status'] = 'registered'
        
        
        merchant = Merchant.objects.create(first_name = first_name, last_name = last_name, email= email, password = pw_hash)
        request.session['merchant_id'] = merchant.id
    return redirect('/main')

def login(request):
    errors2 = Merchant.objects.login_validator(request.POST)
    if len(errors2 ) > 0:
        for key,value in errors2.items():
            messages.error(request, value)
        return redirect('/')
    
    merchant= Merchant.objects.filter(email = request.POST['email2'])
    if merchant:
        logged_user = merchant[0]
        if bcrypt.checkpw(request.POST['password2'].encode(),logged_user.password.encode()):
            request.session['username'] = logged_user.first_name
            request.session['status'] = 'logged in'
            request.session['merchant_id'] = logged_user.id
            return redirect('/main')
        print('Wrong Password')

def logout(request):
    del request.session['username']
    del request.session['status']
    del request.session['merchant_id']
    request.session.flush()
    return redirect('/')

def main(request):
    the_cars = Car.objects.aggregate(Avg('rent_price'))
    this_merchant = Merchant.objects.get(id = request.session['merchant_id'])
    cars = this_merchant.cars_owned.all()
    
    context = {
        'all_cars' : the_cars,
        'my_cars':cars,
        'merchant':this_merchant
    }
    return render(request,'main.html',context)

def add_car(request):
    the_cars = Car.objects.aggregate(Avg('rent_price'))
    context = {
        'cars' : the_cars
    }
    return render(request,'add_car.html',context)

def adding_car(request):
    the_type = request.POST['the_type']
    man_year = int(request.POST['man_year'])
    rent_price = int(request.POST['rent_price'])
    insurance = int(request.POST['insurance'])
    maintenance = int(request.POST['maintenance'])
    payments = int(request.POST['payments'])
    acquiring_date = request.POST['acquiring_date']
    owned_by_id = Merchant.objects.get(id=request.session.get('merchant_id'))
    cars = Car.objects.create(the_type = the_type,man_year = man_year,rent_price=rent_price,insurance=insurance,maintenance=maintenance,payments = payments,acquiring_date = acquiring_date,owned_by = owned_by_id)
    the_cars = Car.objects.aggregate(Avg('rent_price'))
    context = {
        'all_cars' : the_cars,
        'my_cars':cars,
        
    }
    return redirect(request,'main.html',context)

def view(request,id):
    the_car = Car.objects.get(id = id)
    rental = Rental.objects.filter(car=the_car).first()
    client = rental.client if rental else None

    context = {
        'car' : the_car,
        'rental': rental,
        'client': client
    }
    return render(request,'view.html',context)

def edit(request,id):
    car = Car.objects.get(id = id)
    context= {
        'car' : car
    }
    return render(request,'edit.html',context)

def confirm(request):
    car_id = request.POST['car_id']
    the_type = request.POST['the_type']
    man_year = int(request.POST['man_year'])
    rent_price = int(request.POST['rent_price'])
    insurance = int(request.POST['insurance'])
    maintenance = int(request.POST['maintenance'])
    payments = int(request.POST['payments'])
    acquiring_date = request.POST.get('acquiring_date')

    car = Car.objects.get(id=car_id)
    car.the_type = the_type
    car.man_year = man_year
    car.rent_price = rent_price
    car.insurance = insurance
    car.maintenance = maintenance
    car.payments = payments

    # Check if acquiring_date is provided in the request
    # If not, set it to the previously set acquiring_date
    if acquiring_date:
        car.acquiring_date = acquiring_date
    car.save()
    return redirect('/main')

def rent(request,id):
    car = Car.objects.get(id = id)
    context = {
        'car' : car
    }
    return render(request,'rent.html',context)

def rent_thecar(request):
    client_firstname = request.POST['cl_fname']
    client_lastname = request.POST['cl_lname']
    nat_id = request.POST['cl_id']
    cellphone = request.POST['cellphone']
    the_client = Client.objects.create(first_name = client_firstname,last_name = client_lastname,nat_id = nat_id,cell_number=cellphone)
    
    renting_client = Client.objects.get(id = the_client.id)
    renting_car = Car.objects.get(id = request.POST['car_id'])
    returning_date = request.POST['return_date']
    renting = Rental.objects.create(client = renting_client,car =renting_car,return_date = returning_date)
    renting_car.rent_status = 0
    renting_car.save()
    renting.save()
    
    return redirect('/main')

def deliver(request,id):
    car = Car.objects.get(id = id)
    car.rent_status = 1
    
    car.save()
    Rental.objects.all().delete()
    Client.objects.all().delete()
    
    
    return redirect('/main')