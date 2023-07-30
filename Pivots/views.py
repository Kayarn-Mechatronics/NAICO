from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Sum, Max, Min

from django.contrib import auth
from django.contrib.auth.models import User


from .forms import *

# Create your views here.


class index(View):
    def get(self, request):
        return redirect(reverse("Login"))


class authentication:
    class login(View):
        template = "Authentication/login.html"
        context = {"LoginForm": LoginForm()}

        def get(self, request):
            return render(request, self.template, context=self.context)

        def post(self, request):
            #process the login
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                #check if user exists
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect(reverse('Farmers'))
                else:
                    self.context['LoginForm'] = form
                    self.context['errors'] = "Invalid username or password"
                    return render(request, self.template, context=self.context)

    class logout(View):
        def get(self, request):
            auth.logout(request)
            return redirect(reverse('Login'))


class pivot:
    # class dashboard(View):
    #     template = "Pivot/dashboard.html"
    #     context = {}

    #     def get(self, request):
    #         return render(request, self.template, context=self.context)

    #requires login
    class Farmers( View):
        template = "Pivot/Farmers.html"
        #create context dictionary with all the farmers
        context = {}

        def get(self, request):
            self.context["Farmers"] = Farmer.objects.all()
            return render(request, self.template, context=self.context)

    class FarmersForm(View):
        template = "Pivot/FarmerForm.html"
        context = {"FarmerForm": FarmerForm()}

        def get(self, request):
            return render(request, self.template, context=self.context)

        def post(self, request):
            form = FarmerForm(request.POST)
            if form.is_valid():
                form.save(1)
                return redirect(reverse("Farmers"))
            else:
                self.context["FarmerForm"] = form
                self.context["errors"] = form.errors.get_json_data()["__all__"]
                return render(request, self.template, context=self.context)

    class Harvests(View):
        template = "Pivot/Harvests.html"
        context = {}

        def get(self, request):
            self.context["Harvests"]= Harvest.objects.all()
            return render(request, self.template, context=self.context)

    class HarvestForm(View):
        template = "Pivot/HarvestForm.html"
        context = {}

        def get(self, request, farmer_id):
            farmer_id = Farmer.objects.filter(farmer_id=farmer_id).first()
            form = HarvestForm()  # Renamed the variable to 'form' instead of 'HarvestForm'
            self.context["HarvestForm"] = form  # Updated the variable name to 'form'
            self.context['Farmer'] = Farmer.objects.filter(farmer_id=farmer_id.farmer_id).first()

            return render(request, self.template, context=self.context)
        
        def post(self, request, farmer_id):
            farmer_id = Farmer.objects.filter(farmer_id=farmer_id).first()
            form = HarvestForm(request.POST)
            if form.is_valid():
                pivot_id = Pivot.objects.filter(pivot_id=1).first()
                form.save(farmer_id.farmer_id)
                return redirect(reverse("Harvests"))
            else:
                self.context["HarvestForm"] = form
                #self.context["errors"] = form.errors.get_json_data()["__all__"]
                return render(request, self.template, context=self.context)
            
    class Inputs( View):
        template = "Pivot/Inputs.html"
        context = {"Inputs": Input.objects.all()}

        def get(self, request):
            return render(request, self.template, context=self.context)
        

             
    class InputForm( View):
        template = "Pivot/InputForm.html"
        context = {"InputForm": InputForm()}

        def get(self, request, farmer_id: int):
            self.context['Farmer'] = Farmer.objects.filter(farmer_id=farmer_id).first()
            return render(request, self.template, context=self.context)
        
        def post(self, request, farmer_id: int):
            farmer_id = Farmer.objects.filter(farmer_id=farmer_id).first()
            form = InputForm(request.POST)
            if form.is_valid():
                form.save(farmer_id.farmer_id)
                return redirect(reverse("Inputs"))
            else:
                self.context["InputForm"] = form
                #self.context["errors"] = form.errors.get_json_data()["__all__"]
                return render(request, self.template, context=self.context)
            

    class FarmerReport( View):
        template = "Pivot/FarmerReport.html"
        context = {}

        def get(self, request, farmer_id):
            farmer = Farmer.objects.filter(farmer_id=farmer_id).first()
            self.context["Farmer"] = farmer

            #Pull all the harvest by the farmer
            self.context['Harvests'] = Harvest.objects.filter(farmer_id=farmer.farmer_id)
            HarvestTotalValue = self.context['Harvests'].aggregate(Sum('total_value'))['total_value__sum']
            if HarvestTotalValue:
                self.context['HarvestTotalValue'] = HarvestTotalValue
            if HarvestTotalValue is None:
                self.context['HarvestTotalValue'] = 0

            #Pull al the Input by the farmer
            self.context['Inputs'] = Input.objects.filter(farmer_id=farmer.farmer_id)
            self.context['TotalInputs'] = self.context['Inputs'].aggregate(Sum('total_value'))['total_value__sum']
            self.context['TotalPaidInputs'] = Input.objects.filter(farmer_id=farmer.farmer_id, payment_mode="Cash").aggregate(Sum('total_value'))['total_value__sum']
            self.context['TotalCreditInputs'] = Input.objects.filter(farmer_id=farmer.farmer_id, payment_mode="Credit").aggregate(Sum('total_value'))['total_value__sum']
            
            #Balance

            self.context['Balance'] = self.context['HarvestTotalValue'] - self.context['TotalCreditInputs']


            return render(request, self.template, context=self.context)

