from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score,precision_score, recall_score, f1_score

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return render(request,"hospital/hospital_home.html")
    else:
        if request.method=="POST":
            email=request.POST['email']
            password=request.POST['password']
            username = User.objects.get(email=email.lower()).username

            user=authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                name= user.first_name
                return render(request,"hospital/hospital_home.html", {'name':name})
            else:
                messages.error(request, "User Doesn't Match")
                return redirect("login")


    return render(request,'hospital/index.html')

def signup(request):

    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        username=request.POST['username']
        contact=request.POST['contact']
        password=request.POST['password']
        conpass=request.POST['conpass']

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = name
        
        
        myuser.save()
        messages.success(request, "Your Account has been successfully created.")
        return redirect('login')



    return render(request,'hospital/signup.html')

def signout(request):
    logout(request)
    messages.success(request, "Successfully Loged out")
    
    return render(request,'hospital/index.html')

def test(request):
    return render(request,'hospital/test.html')

def test_result(request):
    base_model= joblib.load('model.sav');
    df=pd.read_csv(request.FILES['df'])
    df.dropna(inplace=True)
    # new_row = {'gender': 'Other', 'age': 39, 'hypertension': 0, 'heart_disease':0, 'smoking_history':'not current', 'bmi':31.24, 'HbA1c_level':6.2, 'blood_glucose_level':85, 'diabetes':0}
    # df1=pd.DataFrame(new_row)
    # df = pd.concat([df, df1], ignore_index = True)
    # df.reset_index()
    ds = pd.get_dummies(df, columns = ['gender', 'smoking_history'])
    total_data=df.shape
    total_row=total_data[0]
    X=ds.drop(columns='diabetes')
    y=ds[['diabetes']]
    y_pred = base_model.predict(X)

    accuracy=accuracy_score(y, y_pred)
    precision=precision_score(y, y_pred)
    recall=recall_score(y, y_pred)
    f1=f1_score(y, y_pred)
    cm = confusion_matrix(y, y_pred)

    variable={'df':df.head(20),'total_data':total_row,'score':accuracy,'precision':precision, 'recall':recall, 'f1':f1,'TP':cm[0][0],'FP':cm[0][1],'FN':cm[1][0],'TN':cm[1][1]}
    return render(request,'hospital/test_result.html', context=variable)

def home(request):
    # user=User.objects.get().username
    if request.user.is_authenticated:
        # Do something for authenticated users.
        return render(request,'hospital/hospital_home.html')
    else:
        logout(request)
        return render(request,'hospital/index.html')
    

