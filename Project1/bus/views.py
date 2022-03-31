from django.shortcuts import render, redirect
from . forms  import CreateUserForm
from django.contrib  import messages
from . models import Routes,Bus
from . filters import routeFilter
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required


config ={
  "apiKey": "AIzaSyBSQSEP5Z0d-w8c26Jg59LzNzRhX5IvEyU",
  "authDomain": "kyubus-f4b7c.firebaseapp.com",
  "databaseURL": "https://kyubus-f4b7c-default-rtdb.firebaseio.com",
  "projectId": "kyubus-f4b7c",
  "storageBucket": "kyubus-f4b7c.appspot.com",
  "messagingSenderId": "384761105159",
  "appId": "1:384761105159:web:b49bf926321e8a592b93a2",
  "measurementId": "G-1GTFXR44MZ"
}





def seatsRemain(route):
    seats = route.bus.no_of_seats
    rio=route.bSeats
    return seats-rio


def home(request):
    routes = Routes.objects.all()
    context = {'routes':routes}
    #print(routes)

    if request.method == 'POST':    
        date = request.POST['date']
        if Routes.objects.filter(date = date):
            return redirect('route', date)
        else:
            messages.info(request, "Sorry, but routes on that date per now\n try out another date.")
            return redirect('home')
            
    else:
        return render(request, 'home.html', context)





def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_Name')
            messages.success(request, "Account was created for "+ user)
            return redirect('login')
        else:
            messages.info(request,"The form is not filled approprietly")
            return redirect('register')

    else:
        context={'form':form}
        return render(request, 'register.html', context)
    



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid crudentials')
            return redirect('login')
        
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')





def route(request, result):
    results = Routes.objects.filter(date = result)
    myFilter = routeFilter(request.GET, queryset=results)
    results = myFilter.qs
    context = {'results': results, 'myFilter':myFilter}

    return render(request, 'route.html', context )




@login_required(login_url = 'login')
def book(request,id):
    route = Routes.objects.get(id = id)
    seats = route.bus.no_of_seats
    rio=route.bSeats
    rem =seats-rio
    #rem=seatsRemain(route)
    context={'user':request.user, 'route':route, 'rem':rem}

    if request.method=="POST":
        
        wantedSeats = int(request.POST['no_seats'])
        paymentMethod = request.POST['payment']
        if wantedSeats<=rem:
            rio = rio + wantedSeats
            route.bSeats = rio
            route.save()
            chargedfare = wantedSeats * route.fare
            context['charge'] = chargedfare
            context['method'] = paymentMethod
            messages.info(request, "Thanks for booking")
            return render(request, 'book.html',context)
        
        else:
            messages.info(request, "The number of seats requested is not available")
            return render(request, 'book.html',context)
    else:
         return render(request, 'book.html',context) 





def reciept(request):
    return render(request, 'reciept.html')