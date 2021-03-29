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