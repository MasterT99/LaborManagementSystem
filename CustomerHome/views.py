from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from CustomerHome.models import Customer
from Owner.models import Owner
from Manager.models import Manager
from Workers.models import Worker
from BookWorker.models import BookWorker

from datetime import datetime
from datetime import date

isLogin = False
isLogout = False

# Create your views here.
def index(request):
    global isLogin
    global isLogout

    if('user_email' in request.session):
        email = request.session.get('user_email')

        result_customer = Customer.objects.filter(customer_email=email)
        result_owner = Owner.objects.filter(Owner_email=email)
        result_manager = Manager.objects.filter(Manager_email=email)

        if result_customer.exists():
            request.session['user_email'] = email
            isLogin = True
            return redirect('/Home/')
        elif result_owner.exists():
            request.session['user_email'] = email
            isLogin = True
            return redirect('/Owner/')
        elif result_manager.exists():
            request.session['user_email'] = email
            isLogin = True
            return redirect('/Manager/')
        return redirect('/Home/')

    worker = Worker.objects.all()
    if('user_email' not in request.session and isLogout):
        isLogin = False
        isLogout = False
        Message = "Successfully Logged Out!!"
        return render(request,'index.html',{'Message':Message,'worker':worker})
    return render(request,'index.html',{'worker':worker})

def signin(request):
    return render(request,'SignIn.html')

def register(request):
    return render(request,'register.html')

def LoginAuthentication(request):
    global isLogin
    login_email=request.POST.get('login_email','')
    login_password=request.POST.get('login_password','')
    # customer = Customer.objects.all()

    result_customer = Customer.objects.filter(customer_email=login_email,customer_password=login_password)
    result_owner = Owner.objects.filter(Owner_email=login_email,Owner_password=login_password)
    result_manager = Manager.objects.filter(Manager_email=login_email,Manager_password=login_password)

    if result_customer.exists():
        request.session['user_email'] = login_email
        isLogin = True
        return redirect('/Home/')
    elif result_owner.exists():
        request.session['user_email'] = login_email
        isLogin = True
        return redirect('/Owner/')
    elif result_manager.exists():
        request.session['user_email'] = login_email
        isLogin = True
        return redirect('/Manager/')
    else:
        Message = "Invalid Email or password!!"
        return render(request,'SignIn.html',{'Message':Message})

def RegisterCustomer(request):
    global isLogin

    customer_firstname=request.POST.get('customer_firstname','')
    customer_lastname=request.POST.get('customer_lastname','')
    customer_dob=request.POST.get('customer_dob','')
    customer_gender=request.POST.get('customer_gender','')
    customer_mobileno=request.POST.get('customer_mobileno','')
    customer_email=request.POST.get('customer_email','')
    customer_password=request.POST.get('customer_password','')
    customer_address=request.POST.get('customer_address','')
    customer_city=request.POST.get('customer_city','')
    customer_state=request.POST.get('customer_state','')
    customer_country=request.POST.get('customer_country','')
    customer_pincode=request.POST.get('customer_pincode','')
    # customer_id=request.FILES['customer_id']

    result_customer = Customer.objects.filter(customer_email=customer_email)
    result_owner = Owner.objects.filter(Owner_email=customer_email)
    result_manager = Manager.objects.filter(Manager_email=customer_email)

    if result_customer.exists() or result_owner.exists() or result_manager.exists():
        Message = "This Email address already exist!!"
        return render(request,'register.html',{'Message':Message})
    else:
        customer=Customer(customer_firstname=customer_firstname,customer_lastname=customer_lastname,
        customer_dob=customer_dob,customer_gender=customer_gender,customer_mobileno=customer_mobileno,
        customer_email=customer_email,customer_password=customer_password,customer_address=customer_address,
        customer_city=customer_city,customer_state=customer_state,customer_country=customer_country,
        customer_pincode=customer_pincode)
        
        customer.save()
        request.session['user_email'] = customer_email
        isLogin = True
        return redirect('/Home/')

def Logout(request):
    global isLogout
    del request.session['user_email']
    isLogout = True
    Message = "Successfully Logged Out!!"
    return redirect('/')

def Home(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)
    worker = Worker.objects.all()
    Message="Welcome Aboard!!"
    return render(request,'Home.html',{'worker':worker,'Message':Message,'customer':customer})

def Profile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)
    return render(request,'Profile.html',{'customer':customer})

def showdetails(request,Worker_work_profile_id):
    worker = Worker.objects.get(Worker_work_profile_id=Worker_work_profile_id)
    if('user_email' not in request.session):
        return render(request,'showdetails_not_login.html',{'worker':worker})
    else:
        customer_email = request.session.get('user_email')
        customer = Customer.objects.get(customer_email=customer_email)
        return render(request,'showdetails_loggedin.html',{'worker':worker,'customer':customer})

def CheckAvailability(request,Worker_work_profile_id):
    if('user_email' not in request.session):
        return redirect('/signin/')

    BookWorker_Date_of_Booking=request.POST.get('BookWorker_Date_of_Booking','')
    BookWorker_Date_of_Return=request.POST.get('BookWorker_Date_of_Return','')
    
    BookWorker_Date_of_Booking = datetime.strptime(BookWorker_Date_of_Booking, '%Y-%m-%d').date()
    BookWorker_Date_of_Return = datetime.strptime(BookWorker_Date_of_Return, '%Y-%m-%d').date()

    bookworker = BookWorker.objects.filter(Worker_work_profile_id=Worker_work_profile_id)
    worker = Worker.objects.get(Worker_work_profile_id=Worker_work_profile_id)

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)

    if BookWorker_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'worker':worker,'customer':customer})

    if BookWorker_Date_of_Return < BookWorker_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'worker':worker,'customer':customer})
    
    days=(BookWorker_Date_of_Return-BookWorker_Date_of_Booking).days+1
    total=days*worker.Worker_price
    
    book_data = {"BookWorker_Date_of_Booking":BookWorker_Date_of_Booking, "BookWorker_Date_of_Return":BookWorker_Date_of_Return,"days":days, "total":total}
    
    for rv in bookworker:

        if (rv.BookWorker_Date_of_Booking >= BookWorker_Date_of_Booking and BookWorker_Date_of_Return >= rv.BookWorker_Date_of_Booking) or (BookWorker_Date_of_Booking >= rv.BookWorker_Date_of_Booking and BookWorker_Date_of_Return <= rv.BookWorker_Date_of_Return) or (BookWorker_Date_of_Booking <= rv.BookWorker_Date_of_Return and BookWorker_Date_of_Return >= rv.BookWorker_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this worker from " + str(rv.BookWorker_Date_of_Booking) + " to " + str(rv.BookWorker_Date_of_Return)
                return render(request,'showdetails_loggedin.html',{'Message':Message,'Available':Available,'worker':worker,'customer':customer,'book_data':book_data})

            NotAvailable = True
            return render(request,'showdetails_loggedin.html',{'NotAvailable':NotAvailable,'dates':rv,'worker':worker,'customer':customer})

        # if (BookWorker_Date_of_Booking < rv.BookWorker_Date_of_Booking and BookWorker_Date_of_Return < rv.BookWorker_Date_of_Booking) or (BookWorker_Date_of_Booking > rv.BookWorker_Date_of_Return and BookWorker_Date_of_Return > rv.BookWorker_Date_of_Return):
        #     Available = True
        #     return render(request,'showdetails_loggedin.html',{'Available':Available,'worker':worker,'customer':customer,'book_data':book_data})


    Available = True
    return render(request,'showdetails_loggedin.html',{'Available':Available,'worker':worker,'customer':customer,'book_data':book_data})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)

    bookworker = BookWorker.objects.filter(customer_email=customer_email)
    if bookworker.exists():
        worker = Worker.objects.all()
        return render(request,'SentRequests.html',{'customer':customer,'bookworker':bookworker,'worker':worker})
    else:
        Message = "You haven't made any worker request yet!!"
        return render(request,'SentRequests.html',{'customer':customer,'bookworker':bookworker,'Message':Message})

def about_us(request):
    return render(request, 'aboutus.html')
    
def contact_us(request):
    return render(request, 'contactus.html')

def sitemap(request):
    return render(request, 'sitemap.html')

def search(request):
    return HttpResponse('search')