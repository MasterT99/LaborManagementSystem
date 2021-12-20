from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from CustomerHome import views as cust_views
from Workers import views as wor_views
from . import views

urlpatterns = [
    path('', views.index, name="Owner"),
    path('signin/', cust_views.signin, name="SignIn"),
    path('Logout/', cust_views.Logout, name="Logout"),
    path('Profile/', views.Profile, name="Profile"),
    path('AddWork/', views.add_Worker, name="AddWork"),
    # path('RegisterManager/', views.register_manager, name="RegisterManager"),
    path('ManagerRegistration/', views.ManagerRegistration, name="ManagerRegistration"),
    # path('AllManagers/', views.AllManagers, name="AllManagers"),
    path('AllCustomers/', views.AllCustomers, name="AllCustomers"),
    path('AllWork/', views.AllWork, name="AllWork"),
    path('WorkerDetails/<str:Worker_work_profile_id>/', views.showdetails, name="OwnerWorkerDetails"),
    path('CheckAvailability/<str:Worker_work_profile_id>/', views.CheckAvailability, name="OwnerCheckAvailability"),
    path('BookRequest/', views.BookRequest, name="BookRequest"),
    path('SentRequests/', views.SentRequests, name="SentRequests"),
    # path('DeleteManager/', views.DeleteManager, name="DeleteManager"),
    path('DeleteWorkProfile/', views.DeleteWorkProfile, name="DeleteWorkProfile"),
    # path('ManagerProfile/<str:Manager_email>/', views.Manager_Profile,name="ManagerProfile"),
    path('CustomerProfile/<str:customer_email>/', views.Customer_Profile, name="CustomerProfile"),
    path('WorkProfile/AddWork', wor_views.add_worker, name="AddWork")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
