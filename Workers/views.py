from django.shortcuts import render, redirect
from django.http import HttpResponse
from Workers.models import Worker
from Owner.models import Owner
from Manager.models import Manager
from django.shortcuts import get_object_or_404

# Create your views here.
def add_worker(request):
    Worker_name=request.POST.get('Worker_name','')
    Worker_company=request.POST.get('Worker_company','')
    Worker_model=request.POST.get('Worker_model','')
    Worker_type=request.POST.get('Worker_type','')
    Worker_fuel=request.POST.get('Worker_fuel','')
    Worker_No_of_Seats=request.POST.get('Worker_No_of_Seats',0)
    Worker_color=request.POST.get('Worker_color','')
    Worker_work_profile_id=request.POST.get('Worker_work_profile_id','test')
    
    Worker_added_by=request.session.get('user_email')

    isWorkProfileTemped=request.POST.get('isWorkProfileTemped',True)
    Worker_description=request.POST.get('Worker_description','')
    Worker_price=request.POST.get('Worker_price','')
    # Worker_image1=request.FILES['Worker_image1']
    # Worker_image2=request.FILES['Worker_image2']
    # Worker_image3=request.FILES['Worker_image3']

    result_worker = Worker.objects.filter(Worker_work_profile_id=Worker_work_profile_id)
    result_owner = Owner.objects.filter(Owner_email=Worker_added_by)
    result_manager = Manager.objects.filter(Manager_email=Worker_added_by)

    if result_worker.exists():
        if result_owner.exists():
            Message = "This Work already exist!!"
            return render(request,'Owner_Add_Worker.html',{'Message':Message})
        if result_manager.exists():
            Message = "This Work already exist!!"
            return render(request,'Manager_Add_Worker.html',{'Message':Message})
    else:
        worker=Worker(Worker_name=Worker_name,Worker_company=Worker_company,
        Worker_model=Worker_model,
                        Worker_type=Worker_type,
                        # Worker_fuel=Worker_fuel,
        Worker_No_of_Seats=Worker_No_of_Seats,Worker_color=Worker_color,
        Worker_work_profile_id=Worker_work_profile_id,
        Worker_added_by=Worker_added_by,isWorkProfileTemped=isWorkProfileTemped,Worker_description=Worker_description,
        Worker_price=Worker_price
                        # ,Worker_image1=Worker_image1,Worker_image2=Worker_image2,Worker_image3=Worker_image3
                        )
        
        worker.save()
        if result_owner.exists():
            return redirect('/Owner/AllWork')
        if result_manager.exists():
            return redirect('/Manager/AllWork')