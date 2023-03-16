import pymongo
from django.contrib import messages
import requests
from django.shortcuts import render, redirect
from News.models import DefaulNewsCategory
from User.views import userLogInCheck
from django.contrib import sessions


# Create your views here.
client = pymongo.MongoClient(
        "mongodb+srv://Shubham:Shubh_012@cluster0.8ji46re.mongodb.net/?retryWrites=true&w=majority")
database = client.MongoP
news_collection=database.app1_crud
url = "https://newscatcher.p.rapidapi.com/v1/search_enterprise"

def showNews(request):
    obj=DefaulNewsCategory()
    ref=obj.ref
    l=obj.lang
    s=obj.sort
    querystring = {"q":ref, "lang":l, "sort_by":'date',"from":"today","page": "1", "media": "True", }
    headers = {
        "X-RapidAPI-Key": "81ca2c5f72mshb0e22d5ea9f9730p12ff74jsn9cc349c3988d",
        "X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    print(res)
    for i in res['articles']:
        i['id']=i['_id']
        del i['_id']

    collections=database.app1_crud.replace_one({},res)
    res1=news_collection.find_one({})
    if request.session.get('0') and request.session.get('1'):
        return redirect('homepage')
    else:
        return render(request, 'index.html', {'res':res1})


def logInCheck(request):
    print('session',request.session.get('0'))
    if request.session.get('0') and request.session.get('1'):
        print(True)
        return redirect('homepage')
    else:
        messages.error(request,'Please Log In First')
        return redirect('show')



#----------------------******-----------------------#