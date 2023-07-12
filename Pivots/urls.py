from django.urls import path
from . import views


urlpatterns = [    
    path('', views.index.as_view(), name='index'),
    path('login', views.authentication.login.as_view(), name='Login'),
    path('logout', views.authentication.logout.as_view(), name='Logout'),


    #Pivot
    #path('pivot', views.pivot.dashboard.as_view(), name='pivot'),
    path('pivot/farmers', views.pivot.Farmers.as_view(), name='Farmers'),
    path('pivot/farmers/add', views.pivot.FarmersForm.as_view(), name='FarmerForm'),

    path('pivot/harvests', views.pivot.Harvests.as_view(), name='Harvests'),
    path('pivot/farmers/<int:farmer_id>/harvests/add', views.pivot.HarvestForm.as_view(), name='HarvestForm'),

    #add input paths
    path('pivot/inputs', views.pivot.Inputs.as_view(), name='Inputs'),
    path('pivot/farmers/<int:farmer_id>/inputs/add', views.pivot.InputForm.as_view(), name='InputForm'),

    #add report paths
    path('pivot/farmers/<int:farmer_id>/report', views.pivot.FarmerReport.as_view(), name='FarmerReport'),
    path('pivot/report', views.pivot.FarmerReport.as_view(), name='PivotReport'),
    



    ]