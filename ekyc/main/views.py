from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import models as userModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from .ml import *
from decouple import config

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

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

def video(request):
    return render(request, "video.html")

def verify_ids(request):
    if request.method == 'POST':
        aadhar_no = request.POST['aadhar_no']
        pan_no = request.POST['pan_no']

        if len(aadhar_no) == 12 and aadhar_no.isdigit() and len(pan_no) == 10:
            profile = Profile.objects.get(user=request.user.id)

            if profile.aadhar_no == aadhar_no:
                if profile.pan_no == pan_no:
                    messages.info(request, 'Valid details.')
                    return redirect('verifydocs')
                else:
                    messages.info(request, 'Invalid pancard number.')
                    return redirect('verifyids')
            else:
                messages.info(request, 'Invalid aadhar number.')
                return redirect('verifyids')
        else:
            messages.error(request, "Enter valid details.")
            return redirect('verifyids')
    else:
        return render(request, 'aadharPan.html')

@login_required(login_url='login')
def verify_phone(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        print(phone)
        if len(phone) == 10 and phone.isdigit():
            import twilio
            # Download the helper library from https://www.twilio.com/docs/python/install
            from twilio.rest import Client
            import random # generate random number
            otp = random.randint(1000,9999)
            OTP.objects.create(otp_code=otp, user=request.user)
            print("Generated OTP is - ",otp)
            # Your Account Sid and Auth Token from twilio.com/console
            # DANGER! This is insecure. See http://twil.io/secure
            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)

            message = client.api.account.messages.create(
                    body='Hello Dear, ' + request.user.username +'Your Secure Device OTP is - ' + str(otp),
                    from_='+18102165640',
                    to='+91'+ phone
                )

            print(message.sid)
            return redirect('verifyotp')
        else:
            messages.error(request, "Please enter a valid phone number.")
            return redirect('verifyphone')

    else:
        return render(request, 'phone.html')

def verify_otp(request):
    if request.method == 'POST':
        ist = request.POST['ist']
        sec = request.POST['sec']
        third = request.POST['third']
        fourth = request.POST['fourth']

        digits = ist+sec+third+fourth

        otp = OTP.objects.filter(user_id = request.user.id)[0]

        print(otp)
        if int(digits) == otp.otp_code:
            print("otp maches")
            otp.delete()
            return redirect('verifyids') #redirect to verify video later
        else:
            print("otp didnt match")
            messages.error(request, "OTP did not match.")
            otp.delete()
            return redirect('verifyotp')
    else:
        return render(request, 'otp.html')

def delete_otp(request):
    otp = OTP.objects.filter(user_id = request.user.id)[0]
    otp.delete()
    return redirect('verifyphone')

def verify_docs(request):
    if request.method == 'POST':
        picture = ImageUpload(file=request.FILES.get('picture'), user=request.user)
        idproof = IdUpload(file=request.FILES.get('idproof'), user=request.user)
        addrproof = AddressUpload(file=request.FILES.get('addrproof'), user=request.user)
        picture.save()
        idproof.save()
        addrproof.save()
        return redirect('video')
    else:
        return render(request, 'documents.html')


def profile(request):
    prof = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {'prof':prof})

# def video(request):
    # return render(request, 'video.html')

    
import base64
@csrf_exempt
def video(request):
    if request.method == "POST":
        print(request.FILES.get('video'))
        vid = request.FILES.get('video')
        text = base64.b64encode(vid.read())
        # print(text)
        fh = open("media/videos/video.mp4", "wb")
        fh.write(base64.b64decode(text))
        fh.close()
        flag = 1
        try:
            flag = verification()
        except:
            print()
        if flag == 0:
            print("Verified")
            prof = Profile.objects.get(user_id=request.user.id)
            prof.is_kyc_verified = True
            prof.save()
            return redirect('verifyprofile')
        else:
            print("Recheck")
            mssg = "Please recheck your uploaded documents and ensure that there is proper lighting for the video. There was some problem in processing your request."
            return render(request, 'documents.html', {"message":mssg})
        # vid_final = VideoUpload(file=base64.b64decode(text), user=request.user)
        # vid_final.save()
    else:
        return render(request, 'video.html')

