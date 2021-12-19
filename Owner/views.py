from django.shortcuts import render, redirect
from django.http import HttpResponse
from Owner.models import Owner
from Manager.models import Manager
from CustomerHome.models import Customer
from Workers.models import Worker
from BookWorker.models import BookWorker

from datetime import datetime
from datetime import date
import os
from LaborManagementSystem.settings import MEDIA_ROOT

# Create your views here.
def index(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    worker = Worker.objects.all()
    Message="Welcome Aboard!!"
    no_of_pending_request=count_pending_book_request()
    return render(request,'Owner_index.html',{'worker':worker,'Message':Message,'owner':owner,'no_of_pending_request':no_of_pending_request})

def Profile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    no_of_pending_request=count_pending_book_request()
    return render(request,'Owner_Profile.html',{'owner':owner,'no_of_pending_request':no_of_pending_request})

def register_manager(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    no_of_pending_request=count_pending_book_request()
    return render(request,'register_manager.html',{'owner':owner,'no_of_pending_request':no_of_pending_request})

def ManagerRegistration(request):
    Manager_firstname=request.POST.get('Manager_firstname','')
    Manager_lastname=request.POST.get('Manager_lastname','')
    Manager_dob=request.POST.get('Manager_dob','')
    Manager_gender=request.POST.get('Manager_gender','')
    Manager_mobileno=request.POST.get('Manager_mobileno','')
    Manager_email=request.POST.get('Manager_email','')
    Manager_password=request.POST.get('Manager_password','')
    Manager_address=request.POST.get('Manager_address','')
    Manager_city=request.POST.get('Manager_city','')
    Manager_state=request.POST.get('Manager_state','')
    Manager_country=request.POST.get('Manager_country','')
    Manager_pincode=request.POST.get('Manager_pincode','')
    Manager_id=request.FILES['Manager_id']

    result_customer = Customer.objects.filter(customer_email=Manager_email)
    result_owner = Owner.objects.filter(Owner_email=Manager_email)
    result_manager = Manager.objects.filter(Manager_email=Manager_email)
    if result_customer.exists() or result_owner.exists() or result_manager.exists():
        Message = "This Email address already exist!!"
        return render(request,'register_manager.html',{'Message':Message})
    else:
        manager=Manager(Manager_firstname=Manager_firstname,Manager_lastname=Manager_lastname,
        Manager_dob=Manager_dob,Manager_gender=Manager_gender,Manager_mobileno=Manager_mobileno,
        Manager_email=Manager_email,Manager_password=Manager_password,Manager_address=Manager_address,
        Manager_city=Manager_city,Manager_state=Manager_state,Manager_country=Manager_country,
        Manager_pincode=Manager_pincode,Manager_id=Manager_id)
        
        manager.save()
        return redirect('/Owner/AllManagers')

def AllManagers(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    manager = Manager.objects.all()
    no_of_pending_request=count_pending_book_request()
    return render(request,"All_Managers.html",{'manager':manager,'owner':owner,'no_of_pending_request':no_of_pending_request})

def AllCustomers(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    customer = Customer.objects.all()
    no_of_pending_request=count_pending_book_request()
    return render(request,"All_Customers.html",{'customer':customer,'owner':owner,'no_of_pending_request':no_of_pending_request})

def Manager_Profile(request,Manager_email):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    manager = Manager.objects.get(Manager_email=Manager_email)
    no_of_pending_request=count_pending_book_request()
    return render(request,'Owner_Manager_Profile.html',{'owner':owner,'manager':manager,'no_of_pending_request':no_of_pending_request})

def Customer_Profile(request,customer_email):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    customer = Customer.objects.get(customer_email=customer_email)
    no_of_pending_request=count_pending_book_request()
    return render(request,'Owner_Customer_Profile.html',{'owner':owner,'customer':customer,'no_of_pending_request':no_of_pending_request})

def add_Worker(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    no_of_pending_request=count_pending_book_request()
    return render(request,"Owner_Add_Worker.html",{'owner':owner,'no_of_pending_request':no_of_pending_request})

def AllWork(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    # worker = Worker.objects.filter(Worker_added_by=owner_email)
    worker = Worker.objects.all()
    no_of_pending_request=count_pending_book_request()
    return render(request,"Owner_all_workers.html",{'worker':worker,'owner':owner,'no_of_pending_request':no_of_pending_request})

def showdetails(request,Worker_work_profile_id):
    if('user_email' not in request.session):
        return redirect('/signin/')
    worker = Worker.objects.get(Worker_work_profile_id=Worker_work_profile_id)
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    no_of_pending_request=count_pending_book_request()
    return render(request,'Owner_showdetails.html',{'worker':worker,'owner':owner,'no_of_pending_request':no_of_pending_request})

def CheckAvailability(request,Worker_work_profile_id):
    if('user_email' not in request.session):
        return redirect('/signin/')

    BookWorker_Date_of_Booking=request.POST.get('BookWorker_Date_of_Booking','')
    BookWorker_Date_of_Return=request.POST.get('BookWorker_Date_of_Return','')

    BookWorker_Date_of_Booking = datetime.strptime(BookWorker_Date_of_Booking, '%Y-%m-%d').date()
    BookWorker_Date_of_Return = datetime.strptime(BookWorker_Date_of_Return, '%Y-%m-%d').date()

    bookworker = BookWorker.objects.filter(Worker_work_profile_id=Worker_work_profile_id)
    worker = Worker.objects.get(Worker_work_profile_id=Worker_work_profile_id)

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    no_of_pending_request=count_pending_book_request()

    if BookWorker_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'worker':worker,'owner':owner,'no_of_pending_request':no_of_pending_request})

    if BookWorker_Date_of_Return < BookWorker_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'worker':worker,'owner':owner,'no_of_pending_request':no_of_pending_request})
    
    days=(BookWorker_Date_of_Return-BookWorker_Date_of_Booking).days+1
    total=days*worker.Worker_price
    
    book_data = {"BookWorker_Date_of_Booking":BookWorker_Date_of_Booking, "BookWorker_Date_of_Return":BookWorker_Date_of_Return,"days":days, "total":total}
    
    for rv in bookworker:

        # if (BookWorker_Date_of_Booking < rv.BookWorker_Date_of_Booking and BookWorker_Date_of_Return < rv.BookWorker_Date_of_Booking) or (BookWorker_Date_of_Booking > rv.BookWorker_Date_of_Return and BookWorker_Date_of_Return > rv.BookWorker_Date_of_Return):
        #     Available = True
        #     return render(request,'Owner_showdetails.html',{'Available':Available,'worker':worker,'owner':owner,'book_data':book_data,'no_of_pending_request':no_of_pending_request})

        if (rv.BookWorker_Date_of_Booking >= BookWorker_Date_of_Booking and BookWorker_Date_of_Return >= rv.BookWorker_Date_of_Booking) or (BookWorker_Date_of_Booking >= rv.BookWorker_Date_of_Booking and BookWorker_Date_of_Return <= rv.BookWorker_Date_of_Return) or (BookWorker_Date_of_Booking <= rv.BookWorker_Date_of_Return and BookWorker_Date_of_Return >= rv.BookWorker_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this worker from " + str(rv.BookWorker_Date_of_Booking) + " to " + str(rv.BookWorker_Date_of_Return)
                return render(request,'Owner_showdetails.html',{'Message':Message,'Available':Available,'worker':worker,'owner':owner,'book_data':book_data,'no_of_pending_request':no_of_pending_request})

            NotAvailable = True
            return render(request,'Owner_showdetails.html',{'NotAvailable':NotAvailable,'dates':rv,'worker':worker,'owner':owner,'no_of_pending_request':no_of_pending_request})
    
    Available = True
    return render(request,'Owner_showdetails.html',{'Available':Available,'worker':worker,'owner':owner,'book_data':book_data,'no_of_pending_request':no_of_pending_request})

def BookRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    bookworker = BookWorker.objects.all()
    no_of_pending_request=count_pending_book_request()
    return render(request,'Owner_BookRequest.html',{'owner':owner,'bookworker':bookworker,'no_of_pending_request':no_of_pending_request})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    no_of_pending_request=count_pending_book_request()

    bookworker = BookWorker.objects.filter(customer_email=owner_email)
    if bookworker.exists():
        worker = Worker.objects.all()
        return render(request,'Owner_SentRequests.html',{'owner':owner,'bookworker':bookworker,'worker':worker,'no_of_pending_request':no_of_pending_request})
    else:
        Message = "You haven't made any worker request yet!!"
        return render(request,'Owner_SentRequests.html',{'owner':owner,'bookworker':bookworker,'Message':Message,'no_of_pending_request':no_of_pending_request})

def DeleteManager(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    Manager_email = request.GET.get('Manager_email','')
    manager = Manager.objects.get(Manager_email=Manager_email)
    manager.delete()

    return redirect('/Owner/AllManagers/')

def DeleteWorkProfile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    Worker_work_profile_id = request.GET.get('Worker_work_profile_id','')
    worker = Worker.objects.get(Worker_work_profile_id=Worker_work_profile_id)

    # path1 = MEDIA_ROOT + str(worker.Worker_image1)
    # path2 = MEDIA_ROOT + str(worker.Worker_image2)
    # path3 = MEDIA_ROOT + str(worker.Worker_image3)
    #
    # os.remove(path1)
    # os.remove(path2)
    # os.remove(path3)

    worker.delete()
    

    return redirect('/Owner/AllWork/')

def count_pending_book_request():
    no_of_pending_request=0
    bookworker = BookWorker.objects.all()
    for rv in bookworker:
        if rv.request_status == "Pending":
            no_of_pending_request+=1
    return no_of_pending_request