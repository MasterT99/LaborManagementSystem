from datetime import datetime

from Manager.models import Manager
from django.shortcuts import render, redirect

from BookWorker.models import BookWorker
from CustomerHome.models import Customer
from Owner.models import Owner


# Create your views here.
def index(request):
    return render(request, 'BookWorker/index.html')


def SendRequest_toOwner(request):
    if ('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')

    BookWorker_Date_of_Booking = request.POST.get('BookWorker_Date_of_Booking', '')
    BookWorker_Date_of_Return = request.POST.get('BookWorker_Date_of_Return', '')
    Total_days = request.POST.get('Total_days', '')
    BookWorker_Total_amount = request.POST.get('BookWorker_Total_amount', '')
    Worker_work_profile_id = request.POST.get('Worker_work_profile_id', '')
    BookWorker_Date_of_Booking = request.POST.get('BookWorker_Date_of_Booking', '')

    BookWorker_Date_of_Booking = datetime.strptime(BookWorker_Date_of_Booking, '%b. %d, %Y').date()
    BookWorker_Date_of_Return = datetime.strptime(BookWorker_Date_of_Return, '%b. %d, %Y').date()

    bookworker = BookWorker(BookWorker_Date_of_Booking=BookWorker_Date_of_Booking,
                            BookWorker_Date_of_Return=BookWorker_Date_of_Return,
                            Total_days=Total_days, BookWorker_Total_amount=BookWorker_Total_amount,
                            Worker_work_profile_id=Worker_work_profile_id, customer_email=user_email)

    bookworker.save()

    customer = Customer.objects.filter(customer_email=user_email)
    if customer.exists():
        return redirect("/SentRequests/")

    manager = Manager.objects.filter(Manager_email=user_email)
    if manager.exists():
        return redirect("/Manager/SentRequests/")

    owner = Owner.objects.filter(Owner_email=user_email)
    if owner.exists():
        return redirect("/Owner/SentRequests/")


def AcceptRequest(request):
    if ('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')
    id = request.GET.get('id', '')
    bookworker = BookWorker.objects.get(id=id)
    bookworker.isAvailable = False
    bookworker.request_responded_by = user_email
    bookworker.request_status = "Accepted"
    bookworker.save()

    manager = Manager.objects.filter(Manager_email=user_email)
    if manager.exists():
        return redirect("/Manager/BookRequest/")

    owner = Owner.objects.filter(Owner_email=user_email)
    if owner.exists():
        return redirect("/Owner/BookRequest/")


def DeclineRequest(request):
    if ('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')
    id = request.GET.get('id', '')
    bookworker = BookWorker.objects.get(id=id)
    bookworker.isAvailable = True
    bookworker.request_responded_by = user_email
    bookworker.request_status = "Declined"
    bookworker.save()

    manager = Manager.objects.filter(Manager_email=user_email)
    if manager.exists():
        return redirect("/Manager/BookRequest/")

    owner = Owner.objects.filter(Owner_email=user_email)
    if owner.exists():
        return redirect("/Owner/BookRequest/")


def CancelRequest(request):
    if ('user_email' not in request.session):
        return redirect('/signin/')

    user_email = request.session.get('user_email')
    id = request.GET.get('id', '')
    bookworker = BookWorker.objects.get(id=id)
    bookworker.delete()

    customer = Customer.objects.filter(customer_email=user_email)
    if customer.exists():
        return redirect("/SentRequests/")

    manager = Manager.objects.filter(Manager_email=user_email)
    if manager.exists():
        return redirect("/Manager/SentRequests/")

    owner = Owner.objects.filter(Owner_email=user_email)
    if owner.exists():
        return redirect("/Owner/SentRequests/")
