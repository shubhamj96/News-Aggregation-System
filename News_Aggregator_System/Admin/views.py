from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from News.models import UserInfo, AdminInfo
import pymongo
client=pymongo.MongoClient(
    "mongodb+srv://Shubham:Shubh_012@cluster0.8ji46re.mongodb.net/?retryWrites=true&w=majority")
database = client.MongoP
news_collection = database.app1_crud
user_collection = database.app1_user


# Create your views here.
def adminHomePage(request):
    admin_id=request.POST.get('admin_id')
    admin_psw=request.POST.get('admin_psw')
    print(admin_psw,admin_id)
    obj=AdminInfo.objects.filter(admin_id=admin_id,admin_password=admin_psw).values()
    if obj:
        request.session['adminid']=admin_id
        request.session['adminpsw']=admin_psw
    if request.session.get('adminid') and request.session.get('adminpsw'):
        return render(request, 'admin_home_page.html')
    else:
        messages.error(request, 'Invalid ID/Password')
        return redirect('admin_login')


def userList(request):
    user=user_collection.find({})
    data=[]
    for d in user:
        print('user:--',d)
        print('user:--',type(d))
        data.append(d)
    if request.session.get('adminid') and request.session.get('adminpsw'):
         return render(request,'User_Data.html',{'user':data})


def userDetails(request):
    if request.session.get('adminid') and request.session.get('adminpsw'):
        today_date = datetime.today()
        one_month_ago = today_date - relativedelta(months=1)
        print(one_month_ago)
        print(UserInfo.objects.filter(last_login_date__lt =one_month_ago))

        try:
            data = []
            users=UserInfo.objects.filter().values(last_login_date__lt =one_month_ago)
            print()
            for d in users:
                print(d)
                data.append(data)
            return render(request, 'User_Record.html', {'user': users})
        except TypeError:
                return render(request, 'User_Record.html', {'user': 'No Record To Show','msg':'NO Record'})

def userDelete(request):
    if request.session.get('adminid') and request.session.get('adminpsw'):
        user = user_collection.find({},{'id':1,'user_name':1,'log_in_date':1})
        data = []
        count=0
        for x in user:
            x['id'] = x['_id']
            del x['_id']
            for k in x:
                 if k=='id':
                     dummy = {}
                     dummy[k]=x['id']
                     print('dummy_update', dummy)
                     dummy.update(x)
                     print(x)
                     data.insert(count,dummy)
                     print('data',data)
                     print('dummy2',dummy)
                     count=count+1
                     print(count)


        print(data)
        return render(request,'delete_user.html', {'user': data})


def deleteUserRecord(request,uid):
    if request.session.get('adminid') and request.session.get('adminpsw'):
        user_collection.delete_many({'user_name':uid})

        return HttpResponse('ok')


def adminLogIN(request):
    return render(request, 'admin_login.html')


def adminLogOut(request):
    del request.session['adminid']
    del request.session['adminpsw']
    return render(request, 'admin_login.html')