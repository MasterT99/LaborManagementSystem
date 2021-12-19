from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name="Home"),
    path('Home/', views.Home, name="LoggedinHome"),
    path('signin/', views.signin, name="SignIn"),
    path('Logout/', views.Logout, name="Logout"),
    path('register/', views.register, name="Register"),
    path('Profile/', views.Profile, name="Profile"),
    path('about/', views.about_us, name="AboutUs"),
    path('contact/', views.contact_us, name="ContactUs"),
    path('sitemap/', views.sitemap, name="SiteMap"),
    path('search/', views.search, name="Search"),
    path('LoginAuthentication/', views.LoginAuthentication, name="LoginAuthentication"),
    path('RegisterCustomer/', views.RegisterCustomer, name="RegisterCustomer"),
    path('WorkerDetails/<str:Worker_work_profile_id>/', views.showdetails, name="WorkerDetails"),
    path('CheckAvailability/<str:Worker_work_profile_id>/', views.CheckAvailability, name="CheckAvailability"),
    path('SentRequests/', views.SentRequests, name="SentRequests"),
    path('BookWorker', include("BookWorker.urls")),
    path('Owner/', include("Owner.urls")),
    # path('Manager/',include("Manager.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
