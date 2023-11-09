from django.http import HttpResponse
from django.shortcuts import render
import joblib

# Create your views here.
def home(request):
    return render(request,'predict/index.html')


def about(request):
    return render(request,'predict/about.html')


def predict(request):
    return render(request,'predict/predict.html')

def result(request):
    
    model= joblib.load('model.sav');
    data=[]

    data.append(float(request.POST['age']))
    data.append(float(request.POST['tension']))
    data.append(float(request.POST['heart']))
    data.append(float(request.POST['bmi']))
    data.append(float(request.POST['hb']))
    data.append(float(request.POST['glucose']))
    if request.POST['gender']=='Female' :
        data.append(1.0)
        data.append(0.0)
        data.append(0.0)
    elif request.POST['gender']=='Male' : 
        data.append(0.0)
        data.append(1.0)
        data.append(0.0)
    elif request.POST['gender']=='Other' : 
        data.append(0.0)
        data.append(0.0)
        data.append(1.0)
    
    data.append(0.0) #smoking No_info

    if request.POST['smoking']=='current':
        data.append(1.0)
        data.append(0.0)
        data.append(0.0)
        data.append(0.0)
        data.append(0.0)
    elif request.POST['smoking']=='ever':
        data.append(0.0)
        data.append(1.0)
        data.append(0.0)
        data.append(0.0)
        data.append(0.0)
    elif request.POST['smoking']=='former':
        data.append(0.0)
        data.append(0.0)
        data.append(1.0)
        data.append(0.0)
        data.append(0.0)
    elif request.POST['smoking']=='never':
        data.append(0.0)
        data.append(0.0)
        data.append(0.0)
        data.append(1.0)
        data.append(0.0)
    elif request.POST['smoking']=='not_current':
        data.append(0.0)
        data.append(0.0)
        data.append(0.0)
        data.append(0.0)
        data.append(1.0)
    
    res=model.predict([data])
    return render(request,'predict/result.html',{'res':res[0],'data':data})