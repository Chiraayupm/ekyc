from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import models as userModel
from .models import *

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        username = fname + " " + lname

        if password1 == password2:
            if userModel.User.objects.filter(username=username).exists():
                print('Usernme exists')
                messages.info(request, 'Username exists')
                return redirect('register')
            elif userModel.User.objects.filter(email=email).exists():
                print('email exists')
                messages.info(request, 'Email exists')
                return redirect('register')
            else:
                user = userModel.User.objects.create_user(
                    username=username, email=email, password=password1, first_name=fname, last_name=lname)
                user.save()
                return redirect('login')
        else:
            print('pass dosent match')
            messages.info(request, 'Password didn\'t match')
            return redirect('register')
        return redirect('/')
    else:
        return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = userModel.auth.authenticate(username=username, password=password)

        if user is not None:
            userModel.auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid details')
            return redirect('login')
    else:
        return render(request, "login.html")
    return render(request, "login.html")
    
def logout(request):
    userModel.auth.logout(request)
    return redirect('/')

def verify_ids(request):
    if request.method == 'POST':
        aadhar_no = request.POST['aadhar_no']
        pan_no = request.POST['pan_no']

        profile = Profile.objects.get(user=request.user.id)

        if profile.aadhar_no == aadhar_no:
            if profile.pan_no == pan_no:
                messages.info(request, 'Valid details.')
                redirect('verifyphone')
            else:
                messages.info(request, 'Invalid pancard number.')
        else:
            messages.info(request, 'Invalid aadhar number.')

    else:
        return render(request, 'verify.html')

def verify_phone(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        print(phone)
        import twilio
        # Download the helper library from https://www.twilio.com/docs/python/install
        from twilio.rest import Client
        import random # generate random number
        otp = random.randint(1000,9999)
        OTP.objects.create(otp_code=otp, user=request.user)
        print("Generated OTP is - ",otp)
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = 'AC703679e4bfdc618b2c00d92b79be454c'
        auth_token = '49fb345bb91b32322a28a510da05aa6e'
        client = Client(account_sid, auth_token)

        message = client.api.account.messages.create(
                body='Hello Dear, ' + request.user.username +'Your Secure Device OTP is - ' + str(otp),
                from_='+18102165640',
                to='+91'+ phone
            )

        print(message.sid)
        return redirect('verifyotp')
    else:
        return render(request, 'phone.html')

def verify_otp(request):
    if request.method == 'POST':
        digits = request.POST['otp']
        otp = OTP.objects.filter(user_id = request.user.id)[0]
        print(otp)
        if int(digits) == otp.otp_code:
            print("otp maches")
            otp.delete()
            return redirect('/') #redirect to verify video later
        else:
            print("otp didnt match")
    else:
        return render(request, 'otp.html')

def verify_docs(request):
    if request.method == 'POST':
        picture = ImageUpload(file=request.FILES.get('picture'), user=request.user)
        idproof = IdUpload(file=request.FILES.get('idproof'), user=request.user)
        addrproof = AddressUpload(file=request.FILES.get('addrproof'), user=request.user)
        picture.save()
        idproof.save()
        addrproof.save()
        return render(request, 'profile.html')
    else:
        return render(request, 'documents.html')


def profile(request):
    return render(request, 'profile.html')