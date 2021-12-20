from Manager.models import Manager
from django.shortcuts import render, redirect

from Owner.models import Owner
from Workers.models import Worker


# Create your views here.
def add_worker(request):
    Worker_name = request.POST.get('Worker_name', '')
    Worker_company = request.POST.get('Worker_company', '')
    Worker_model = request.POST.get('Worker_model', '')
    Worker_type = request.POST.get('Worker_type', '')
    Worker_skilllevel = request.POST.get('Worker_skilllevel', '')
    Worker_No_of_skills = request.POST.get('Worker_No_of_skills', 0)
    Worker_ptype = request.POST.get('Worker_ptype', '')
    Worker_work_profile_id = request.POST.get('Worker_work_profile_id', 'test')

    Worker_added_by = request.session.get('user_email')

    isWorkProfileTemped = request.POST.get('isWorkProfileTemped', True)
    Worker_description = request.POST.get('Worker_description', '')
    Worker_price = request.POST.get('Worker_price', '')
    # Worker_image1=request.FILES['Worker_image1']
    # Worker_image2=request.FILES['Worker_image2']
    # Worker_image3=request.FILES['Worker_image3']

    result_worker = Worker.objects.filter(Worker_work_profile_id=Worker_work_profile_id)
    result_owner = Owner.objects.filter(Owner_email=Worker_added_by)
    result_manager = Manager.objects.filter(Manager_email=Worker_added_by)

    if result_worker.exists():
        if result_owner.exists():
            Message = "This Work already exist!!"
            return render(request, 'Owner_Add_Worker.html', {'Message': Message})
        if result_manager.exists():
            Message = "This Work already exist!!"
            return render(request, 'Manager_Add_Worker.html', {'Message': Message})
    else:
        worker = Worker(Worker_name=Worker_name, Worker_company=Worker_company,
                        Worker_model=Worker_model,
                        Worker_type=Worker_type,
                        # Worker_skilllevel=Worker_skilllevel,
                        Worker_No_of_skills=Worker_No_of_skills, Worker_ptype=Worker_ptype,
                        Worker_work_profile_id=Worker_work_profile_id,
                        Worker_added_by=Worker_added_by, isWorkProfileTemped=isWorkProfileTemped,
                        Worker_description=Worker_description,
                        Worker_price=Worker_price
                        # ,Worker_image1=Worker_image1,Worker_image2=Worker_image2,Worker_image3=Worker_image3
                        )

        worker.save()
        if result_owner.exists():
            return redirect('/Owner/AllWork')
        if result_manager.exists():
            return redirect('/Manager/AllWork')
