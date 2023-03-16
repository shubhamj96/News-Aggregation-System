import pymongo
import datetime
import requests
from News.models import DefaulNewsCategory, WatchList, UserInfo
from django.contrib import messages
from django.http import HttpResponse


language='en'
category='world'
sort='relevancy'
country='in'




from django.shortcuts import render, redirect

client = pymongo.MongoClient(
    "mongodb+srv://Shubham:Shubh_012@cluster0.8ji46re.mongodb.net/?retryWrites=true&w=majority")
database = client.MongoP
news_collection = database.app1_crud
user_collection = database.app1_user

url = "https://newscatcher.p.rapidapi.com/v1/search_enterprise"


# Create your views here.
def userHomePage(request):

    if category:
        ref = category

    if language:
        l = language

    if sort:
            s = sort
    if country:
        c = country

    querystring = {"q":ref, "lang":l, "sort_by":s,"from":"yesterday","page": "1", "media": "True", }
    # querystring ={

    headers = {
        "X-RapidAPI-Key": "81ca2c5f72mshb0e22d5ea9f9730p12ff74jsn9cc349c3988d",
        "X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res=response.json()
    print(res)
    if request.session.get('0') and request.session.get('1'):
        try:
            for i in res['articles']:
                i['id']=i['_id']
                del i['_id']
            flag=news_collection.replace_one({},res)
            print(flag)
            res1 = news_collection.find_one({})
            print(res1)
            return render(request, 'home_page.html', {'res': res1})
        except KeyError :
            try:

                res1 = news_collection.find_one({})
                messages.error(request, res['status'])
                print(res1)
                return render(request, 'home_page.html', {'res': res1})
            except KeyError:
                res1 = news_collection.find_one({})
                messages.error(request, res['message'])
                print(res)
                return render(request, 'home_page.html', {'res': res1})
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def userLogInCheck(request):
    uname = request.POST.get('uname')
    password = request.POST.get('psw')
    print('user-input: ', uname, password)
    user_coll = database.app1_user
    flag = user_coll.find_one({'user_name': uname, 'password': password})
    print(flag)
    if flag:
        obj=UserInfo(user_name=uname, last_login_date=datetime.datetime.today())
        obj.save()
        print(datetime.datetime.today())
        request.session[0] = uname
        request.session[1] = password
        print('session', request.session.get(0))
        print(request.session.get(1))
        return redirect('homepage')
    else:
        messages.error(request, 'Invalid User Id/Password')
        return redirect('show')


def userRegistraion(request):
    uname = request.POST.get('uname')
    password = request.POST.get('psw')
    f_name = request.POST.get('fname')
    l_name = request.POST.get('lname')
    dob = request.POST.get('dob')
    gender = request.POST.get('gen')
    contact_no = request.POST.get('c_no')
    email_id = request.POST.get("emailid")
    country = request.POST.get('country')
    state = request.POST.get("state")
    city = request.POST.get('city')
    district = request.POST.get('dist')
    zipcode = request.POST.get('zipcode')
    user_info = {'user_name': uname, 'password': password, 'first_name': f_name, 'last_name': l_name,
                 'date_of_birth': dob, 'gender': gender, 'contact_no': contact_no, 'email_id': email_id,
                 'country': country, 'state': state, 'district': district, 'city': city, 'zipcode': zipcode}
    flag = not all(user_info.values())
    if flag:
        messages.error(request, 'Fill all Field')
        print(not all(user_info.values()))
        return render(request, 'registration.html')
    else:
        if user_collection.find_one({"user_name": uname}):
            messages.error(request, 'Already Register Please Log In')
            return redirect('registration')
        else:
            u_id = user_collection.insert_one(user_info).inserted_id
            messages.success(request, 'Successfully Register' + f_name + ' ' + l_name)
            return redirect('show')

    # if u_id:
    #     messages.success(request,'Welcome'+f_name+' '+l_name)
    #     return redirect('hompage')
    # else:
    #     messages.error(request, "Invalid User Id")
    #     return redirect('registration')


def userSignUp(request):
    return render(request, 'registration.html')


def userLogOut(request):
    try:
        del request.session['0']
        del request.session['1']
        messages.success(request, 'Successfully Log Out')
        return redirect('show')
    except:
        messages.error(request, "User already log out")
        return redirect('show')




def userWatchList(request):
    if request.session.get('0') and request.session.get('1'):
        uid = request.session.get('0')
        data1 = []
        for obj in WatchList.objects.filter(u_id=uid).values():
            data1.append(obj)
        return render(request, 'watchlist.html', {'res': data1})

    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def userDiscription(request, id):
    if request.session.get('0') and request.session.get('1'):
        res1 = news_collection.find_one()
        dict_articles = res1['articles']
        l = len(dict_articles)
        for y in range(l):
            print(type(dict_articles[y]['id']), '----->', type(id))
            print((dict_articles[y]['id']), '----->', (id))
            if dict_articles[y]['id'] == id:
                print('match')
                print(dict_articles[y]['title'])
                return render(request, 'description.html',
                              {'res': dict_articles[y]['summary'], 'img': dict_articles[y]['media'],
                               'title': dict_articles[y]['title'], 'author': dict_articles[y]['author']})
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def addWatchList(request, id):
    if request.session.get('0') and request.session.get('1'):
        uid = request.session.get('0')
        res1 = news_collection.find_one()
        dict_articles = res1['articles']
        l = len(dict_articles)
        for y in range(l):
            print(type(dict_articles[y]['id']), '----->', type(id))
            print((dict_articles[y]['id']), '----->', (id))
            if dict_articles[y]['id'] == id:
                obj = WatchList(u_id=uid, article=dict_articles[y]['summary'], img=dict_articles[y]['media'],
                                title=dict_articles[y]['title'], author=dict_articles[y]['author'])
                obj.save()
                messages.success(request, 'Added To Watchlist')
                return redirect('homepage')
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def showWatchList(request, id):
    if request.session.get('0') and request.session.get('1'):
        obj=WatchList.objects.filter(w_id=id).values()

        for data in obj:
            print(data)
            return render(request, 'show_watchlist.html',{'res': data['article'], 'img': data['img'],
                               'title': data['title'], 'author': data['author']} )



    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')



#----------------****************-------------------------#
#newsapi


def langPreference(request,l,ref):
    if category:
        ref=category
    if sort:
        s=sort
    querystring = {"q": ref, "lang": l, "sort_by": s, "from": "yesterday", "page": "1", "media": "True", }
    headers = {
        "X-RapidAPI-Key": "81ca2c5f72mshb0e22d5ea9f9730p12ff74jsn9cc349c3988d",
        "X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    global language
    language=l
    print("lang",res)
    return redirect('homepage')



def searchResult(request,ref):
    if request.session.get('0') and request.session.get('1'):

        if language:
            l=language
            print(language)
        if sort:
            s=sort
        print(l, ref)

        querystring = {"q": ref, "lang": l, "sort_by": s, "from": "yesterday", "page": "1", "media": "True", }
        # querystring ={

        headers = {
            "X-RapidAPI-Key": "81ca2c5f72mshb0e22d5ea9f9730p12ff74jsn9cc349c3988d",
            "X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.json()
        print(res)
        global category
        category=ref
        #print(res['articles'])
        return redirect('homepage')
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def sortNews(request,s):
    if request.session.get('0') and request.session.get('1'):
        ref = ''
        if category:
            ref=category
        if language:
            l=language
        print('sort',ref,l,s)

        global sort
        sort=s
        querystring = {"q": ref, "lang": l, "sort_by": s, "from": "yesterday", "page": "1", "media": "True", }
        # querystring ={

        headers = {
            "X-RapidAPI-Key": "81ca2c5f72mshb0e22d5ea9f9730p12ff74jsn9cc349c3988d",
            "X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.json()

        return redirect('homepage')
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def userDashBoard(request):
    if request.session.get('0') and request.session.get('1'):
        uname=request.session.get('0')
        print(uname)
        user=user_collection.find_one({'user_name': uname})
        for x in user:
            print(x,'--dash')

        return render(request, 'user_dashboard.html', {'user':user})
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def userProfile(request):
    if request.session.get('0') and request.session.get('1'):
         uname = request.session.get('0')
         print(uname)
         user = user_collection.find_one({'user_name': uname})
         for x in user:
             print(x, '--dash')

         return render(request, 'user_profile.html', {'user': user})
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')

def userAccountSeetings(request):
    if request.session.get('0') and request.session.get('1'):
        uname = request.session.get('0')
        print(uname)
        user = user_collection.find_one({'user_name': uname})
        return render(request, 'user_account_setting.html',  {'user': user})

    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')
def userAccountUpdate(request):
    if request.session.get('0') and request.session.get('1'):
        uname = request.POST.get('uname')
        password = request.POST.get('psw')
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gen')
        contact_no = request.POST.get('c_no')
        email_id = request.POST.get("emailid")
        country = request.POST.get('country')
        state = request.POST.get("state")
        city = request.POST.get('city')
        district = request.POST.get('dist')
        zipcode = request.POST.get('zipcode')
        user_info = {'user_name': uname, 'password': password, 'first_name': f_name, 'last_name': l_name,
                     'date_of_birth': dob, 'gender': gender, 'contact_no': contact_no, 'email_id': email_id,
                     'country': country, 'state': state, 'district': district, 'city': city, 'zipcode': zipcode}
        flag = not all(user_info.values())
        if flag:
            messages.error(request, 'Fill all Field')
            print(not all(user_info.values()))
            return render(request, 'user_account_setting.html')

        else:
                u_id = user_collection.update_one(user_info)
                messages.success(request, 'Successfully Updated' + f_name + ' ' + l_name)
                return redirect('dashboard')
    else:
        messages.error(request,'Please LogIn First')
        return redirect('show')