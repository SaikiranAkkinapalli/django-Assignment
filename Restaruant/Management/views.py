from django.db.models.aggregates import Avg
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest,JsonResponse
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import Additem,AddFoodtype,AddTable,CustomerForm,LoginForm,SignUpForm
from django.contrib.auth import authenticate,login
from .models import UserModel, foodtype,item,table,Bill
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import logout
from django.db.models import Sum
def home(request):
    if request.user.is_authenticated: 
        return render(request,'index.html')
    if request.method=="POST":
        user = authenticate(username=request.POST.get('UserSign'), password=request.POST.get('password'))
        if user is not None:
            login(request,user)
            if user.is_admin==True:
                request.session['Admin']=True
            if user.is_admin==False and user.is_staff==True:
                request.session['Manager']=True
            if user.customer==True:
                request.session['customer']=True
                return redirect('/customer')
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
@login_required(login_url='/')
def tableAvailability(request):
    if request.method=="POST":
        number=request.POST['No_Of_People']
        entry = table.objects.filter(Seating_Capacity__gte=number).exclude(Available=False)
        if entry.exists():
            entry=entry.order_by('Seating_Capacity').first()
            tablenum=entry.id
            entry.Available=False
            entry.save()
            request.session['tablenum']=tablenum
            return redirect('/customer')
    response = JsonResponse({"error": "No Vacancy"})
    response.status_code = 503
    return response
@login_required(login_url='/')
def addItem(request):
    if request.method=="GET":
        if 'Admin' in request.session or 'Manager' in request.session:
            form=Additem()
            submission="addItem"
            return render(request,'form.html',{'form':form,'submission':submission}) 
        else:
            return render(request,'error.html',{'error':"No View"})
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
@login_required(login_url='/')
def addFoodType(request):
    boolinsert=False
    if request.method=="GET":
        if 'Admin' not in request.session and 'Manager' not in request.session:
            return render(request,'error.html',{'error':"No View"})
    if request.method=="POST" :
        if 'Admin' in request.session or 'Manager' in request.session:
            form=AddFoodtype(request.POST)
            if form.is_valid():
                form.save()
                boolinsert=True
            else:
                context={
                    "form":form,
                    "boolinsert":False,
                    "submission":"addType"
                }
                return render(request,'form.html',context)
    form=AddFoodtype()
    submission="addType"
    return render(request,'form.html',{'form':form,'submission':submission,'boolinsert':boolinsert})
@login_required(login_url='/')
def addTable(request):
    boolinsert=False
    if request.method=="GET":
        if 'Admin' not in request.session and 'Manager' not in request.session:
            return render(request,'error.html',{'error':"No View"})
    if request.method=="POST":
        if 'Admin' in request.session or 'Manager' in request.session:
            form=AddTable(request.POST)
            if form.is_valid():
                form.save()
                boolinsert=True
        else:
            return render(request,'error.html',{'error':"No View"})
    form=AddTable()
    submission="addTable"
    return render(request,'form.html',{'form':form,'submission':submission,'boolinsert':boolinsert})
@login_required(login_url='/')
def addManager(request):
    if 'Admin' in request.session:
        boolinsert=False
        submission="addmanager"
        if request.method=="POST":
            form=SignUpForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                user = UserModel.objects.create_user(request.POST.get('first_name'),request.POST.get('last_name'),request.POST.get("Email"), request.POST.get("phonenumber"), request.POST.get("password"))
                user.save()
                boolinsert=True
            else :
                context={
                "form":form,
                "boolinsert":False
                }
                return render(request,'form.html',context)
        form=SignUpForm()
        return render(request,'form.html',{'form':form,'submission':submission,'boolinsert':boolinsert})
@login_required(login_url='/')
def orderrecieve(request):
    if request.method=="POST":
        tablenum=request.session['tablenum']
        current_table=table.objects.get(id=tablenum)
        items_qset=item.objects.all()
        if 'ordered_items' in request.session:
            ordered_items=request.session['ordered_items']
        else:
            ordered_items={}
        for items in items_qset:
            if request.POST.get(items.Name) is not None and int(request.POST.get(str(items.id)))<=items.Remaining:
                x=ordered_items.get(items.Name)
                if x:
                    ordered_items[items.Name]=int(request.POST.get(str(items.id)))+int(ordered_items[items.Name])
                else:
                    ordered_items[items.Name]=request.POST.get(str(items.id))
                    current_table.presentbill=current_table.presentbill+(int(request.POST.get(str(items.id)))*items.price)
                    items.Remaining=items.Remaining-int(request.POST.get(str(items.id)))
                    current_table.save()
                    items.save()
        print(ordered_items)
        request.session['ordered_items']=ordered_items
        return HttpResponse("Ordered Succesfully", content_type="text/plain")
def checkout(request):
    tablenum=request.session['tablenum']
    ordered_items=request.session['ordered_items']
    current_table=table.objects.get(id=tablenum)
    bill=current_table.presentbill
    newBill=Bill(amount=bill,table_num=tablenum,items_ordered=str(ordered_items))
    newBill.save()
    current_table.totalbill+=current_table.presentbill
    current_table.presentbill=0
    current_table.Available=1
    current_table.save()
    return render(request,'customerbill.html',{'ordered_items':request.session['ordered_items'],'bill':bill})
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
def ShowBill(request):
    total_amount=table.objects.all().aggregate(Sum('totalbill'))
    bill_list=Bill.objects.all()
    return render(request,'bill.html',{'bill_list':bill_list,'total_amount':total_amount['totalbill__sum']})
def error_404(request, exception):
    return render(request,'error.html',{'error':"No View"})