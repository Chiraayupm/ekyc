from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import models as userModel
from django.views.decorators.csrf import csrf_exempt
from .models import *

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
            messages.error(request, "Please enter a valid phone number.")
            return redirect('verifyphone')

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
            return redirect('verifyids') #redirect to verify video later
        else:
            print("otp didnt match")
            messages.error(request, "OTP did not match.")
            otp.delete()
            return redirect('verifyotp')
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
        return redirect('video')
    else:
        return render(request, 'documents.html')


def profile(request):
    prof = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {'prof':prof})

# def video(request):
    # return render(request, 'video.html')
def verification():
    import face_recognition
    import numpy
    import cv2
    import time
    import os
    import glob
    import os

    list_of_files = glob.glob('media/ids/*.jpeg') # * means all if need specific format then *.csv
    latest_file_document = max(list_of_files, key=os.path.getctime)
    list_of_files_1 = glob.glob('media/images/*.jpeg') # * means all if need specific format then *.csv
    latest_fileimages = max(list_of_files_1, key=os.path.getctime)
    list_of_files_2 = glob.glob('media/videos/*.mp4') # * means all if need specific format then *.csv
    latest_file_videos = max(list_of_files_2, key=os.path.getctime)
    

    flag = 0
    path = 'media/videos/video.mp4'

    cap = cv2.VideoCapture(latest_file_videos)
    width = 1280
    heigh = 720

    i= 0
    while True:

        success, img = cap.read()

        if i == 20:
            break

        try:


            cv2.resize(img,(width,heigh))
            cv2.imwrite('C:/Users/varun/codecell/ekyc/main/vid_ss/camera' + str(i) + '.jpeg', img)
            i += 1


        except Exception as e:
            break



        cv2.waitKey(1)


    imgtest = face_recognition.load_image_file(latest_file_document)

    imgtest = cv2.cvtColor(imgtest , cv2.COLOR_BGR2RGB)
    imgtest = cv2.resize(imgtest , (512,512))
    face_loc_test = face_recognition.face_locations(imgtest)
    encodingtest = face_recognition.face_encodings(imgtest)
    if not len(face_loc_test):
        flag = 1

    img = face_recognition.load_image_file(latest_fileimages)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img , (512,512))
    face_loc = face_recognition.face_locations(img)
    encoding1 = face_recognition.face_encodings(img)
    if not len(face_loc):
        flag = 1





    if flag == 0:
            path = 'C:/Users/varun/codecell/ekyc/main/vid_ss'

            n = (len(os.listdir(path)))
            values = []
            values1 = []
            for i in range(n):
                img = face_recognition.load_image_file('C:/Users/varun/codecell/ekyc/main/vid_ss/camera'+str(i)+'.jpeg')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_loc = face_recognition.face_locations(img)
                if not len(face_loc):
                    #print("Cant sorry")
                    continue
                encoding= face_recognition.face_encodings(img)
                results = face_recognition.compare_faces([encoding[0]],encodingtest[0])

                results1 = face_recognition.compare_faces([encoding[0]],encoding1[0])

                values.append(results)
                values1.append(results1)

            print(values)
            print(values1)

            c=0
            ctc=0
            cfc=0
            if len(values)>3:
                for v in values:
                    a = v[0]

                    if a == True:
                        ctc+=1
                        c+=1
                    else:
                        cfc+=1

                if c//len(values)>0.60:


                    print(c//len(values)*100)
                    

                if ctc>cfc:
                    flag =0
                    print("verified truely")
                else:
                    flag=1
                    print("false verification")



            else:
                flag = 1
                print("Couldnt recognise face , please try again")

            d=0
            dtd=0
            dfd=0
            if len(values1)>3:
                for v in values1:
                    a = v[0]

                    if a == True:
                        dtd+=1
                        d+=1
                    else:
                        dfd+=1

                if d//len(values1)>0.60:
                    print("Verified")
                    #print(c//len(values)*100)

                if dtd>dfd:
                    flag =0
                    print("verified truely")
                else:
                    flag=1
                    print("false verification")



            else:
                flag = 1
                print("Couldnt recognise face , please try again")

            print(flag)


    else:
        print("Please Check Your Uploaded Documents")

    return flag
    
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
        flag = verification()
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

