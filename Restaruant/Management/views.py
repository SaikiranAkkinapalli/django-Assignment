from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest,JsonResponse
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import Additem,AddFoodtype,AddTable,CustomerForm,LoginForm,SignUpForm
from django.contrib.auth import authenticate,login
from .models import UserModel, foodtype,item,table
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import logout
def home(request):
    if request.user.is_authenticated: 
        return render(request,'index.html')
    if request.method=="POST":
        user = authenticate(username=request.POST.get('UserSign'), password=request.POST.get('password'))
        print(request.POST.get('UserSign')+request.POST.get('password'))
        if user is not None:
            if user.is_admin==True:
                request.session['Admin']=True
            if user.customer==True:
                request.session['customer']=True
                form=CustomerForm
                return render(request,'customer.html',{"form":form})
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return render(request,'index.html')
    form1= SignUpForm()
    form2= LoginForm()
    return render(request,'login.html',{'Login':form2,'SignUp':form1})
@login_required(login_url='/')
def customer(request):
    if 'customer' in request.session:
        if 'tablenum' in request.session:
            tablenum=request.session['tablenum']
            item_list = (item.objects.values('type','Name','price','id','Remaining').annotate(dcount=Count('type')).order_by())
            return render(request,'customer.html',{"tablenum":tablenum,"item":item_list})
        form=CustomerForm
        submission="verifyTableAvailability"
        return render(request,'customer.html',{"form":form,"submission":submission})
def tableAvailability(request):
    if request.method=="GET":
        return render(request,'error.html',{'error':"No Add Manager"})
    if request.method=="POST":
        number=request.POST['No_Of_People']
        entry = table.objects.filter(Seating_Capacity__gte=number).exclude(Available=False)
        if entry.exists():
            entry=entry.order_by('Seating_Capacity').first()
            tablenum=entry.id
            entry.Available=False
            entry.save()
            request.session['tablenum']=tablenum
            return render(request,'menu.html',{"tablenum":tablenum})
    response = JsonResponse({"error": "No Vacancy"})
    response.status_code = 503
    return response
def addItem(request):
    if request.method=="GET":
        return render(request,'error.html',{'error':"No Add Manager"})
    if request.is_ajax:
        form=Additem()
        submission="addItem"
        if request.method=="POST":
            form=Additem(request.POST)
            if form.is_valid():
                form.save()
                boolinsert=True
                print("Successfully Inserted")
                return render(request,'form.html',{'form':form,'submission':submission,'boolinsert':boolinsert})
        return render(request,'form.html',{'form':form,'submission':submission})
    return HttpResponse("Page not found")
def addFoodType(request):
    boolinsert=False
    if request.method=="GET":
        return render(request,'error.html',{'error':"No Add Manager"})
    if request.method=="POST":
        form=AddFoodtype(request.POST)
        if form.is_valid():
            form.save()
            boolinsert=True
    form=AddFoodtype()
    submission="addType"
    return render(request,'form.html',{'form':form,'submission':submission,'boolinsert':boolinsert})
def addTable(request):
    boolinsert=False
    if request.method=="GET":
        return render(request,'error.html',{'error':"No Add Manager"})
    if request.method=="POST":
        form=AddTable(request.POST)
        if form.is_valid():
            form.save()
            boolinsert=True
    form=AddTable()
    submission="addTable"
    return render(request,'form.html',{'form':form,'submission':submission,'boolinsert':boolinsert})
def addManager(request):
    boolinsert=False
    if request.method=="GET":
        return render(request,'error.html',{'error':"No Add Manager"})
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            boolinsert=True
    form=SignUpForm()
    submission="addManager"
    return render(request,'form.html',{'form':form,'submission':submission,'boolinsert':boolinsert})
def orderrecieve(request):
    if request.method=="GET":
        return render(request,'error.html',{'error':"No Add Manager"})
    if request.method=="POST":
        tablenum=request.session['tablenum']
        current_table=table.objects.get(id=tablenum)
        items_qset=item.objects.all()
        for items in items_qset:
            if request.POST.get(items.id)!='' and int(request.POST.get(items.id))<=items.Remaining:
                current_table.presentbill=current_table.presentbill+(int(request.POST.get(items.id))*items.price)
                items.Remaining=items.Remaining-int(request.POST.get(items.id))
                current_table.save()
                items.save()
        return HttpResponse("Ordered Succesfully", content_type="text/plain")
def checkout(request):
    if 'tablenum' not in request:
        return render(request,'error.html',{'error':"No Add Manager"})
    tablenum=request.session['tablenum']
    current_table=table.objects.get(id=tablenum)
    bill=current_table.presentbill
    current_table.totalbill+=current_table.presentbill
    current_table.presentbill=0
    current_table.Available=1
    current_table.save()
    del request.session['tablenum']
    message="Your Bill is "+str(bill)
    return HttpResponse(message, content_type="text/plain")
def signup(request):
    form1= SignUpForm()
    form2= LoginForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            user = UserModel.objects.create_customer(request.POST.get('first_name'),request.POST.get('last_name'),request.POST.get("Email"), request.POST.get("password"), request.POST.get("phonenumber"))
            user.save()
            return render(request,'login.html',{'Login':form2,'SignUp':form1,"Success":True})
        else:
            context={
                "Login":LoginForm(),
                "SignUp":form
            }
            return render(request,'login.html',context)
    return render(request,'login.html',{'Login':form2,'SignUp':form1})
def loggingout(request):
    print(request)
    logout(request)
    return redirect(home)
def error_404(request, exception):
    return render(request,'error.html',{'error':"No View"})