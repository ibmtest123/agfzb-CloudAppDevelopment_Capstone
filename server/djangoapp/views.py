from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,get_dealer_by_id_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request, "djangoapp/about.html" )

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request,"djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)
    
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://benjaminli20-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        
        # Get dealers from the URL
        dealers = get_dealers_from_cf(url)
        
        # Create a context dictionary to pass data to the template
        context = {'dealers': dealers}
        # Render the template using the context
        return render(request, 'djangoapp/index.html', context)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        durl = f"https://benjaminli20-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={id}"
        dealers = get_dealers_from_cf(durl)
        context["dealers"] = dealers

        rurl = 'https://benjaminli20-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review'
        reviews = get_dealer_reviews_from_cf(rurl, id=id)
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

#def get_dealer_details(request, id):
    #if request.method == "GET":
        #context = {}
        #dealer_url = "https://benjaminli20-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        #dealer = get_dealers_from_cf(dealer_url, id=id)
        #context["dealer"] = dealer
    
        #review_url = "https://benjaminli20-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review"
        #reviews = get_dealer_reviews_from_cf(review_url, id=id)   
        #context["reviews"] = reviews
        #print("Dealer:", dealer)
        #print("Reviews:", reviews)
        #return render(request, 'djangoapp/dealer_details.html', context)
        #return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, id):
    print(id)
    context = {}
    dealer_url = f"https://benjaminli20-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={id}"
    dealer = get_dealers_from_cf(dealer_url)
    context["dealer"] = dealer
    print(dealer)
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            new_payload = {}
            new_payload["review"] = payload
            review_post_url =  "https://benjaminli20-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)


