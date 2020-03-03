import os
import shutil
from django.shortcuts import render
from django.http import JsonResponse

from .models import video_upload
from .forms import video_upload_form

from .paths import upload_folder

def verify_folder(user):

    path_user = upload_folder + "/" + str(user)
    
    if not os.path.exists(path_user):
        os.makedirs(path_user)

        path_video  = upload_folder  + "/" + str(user)  + "/" + "treated"
        path_treated = upload_folder + "/" + str(user)  + "/" + "video"
        path_in_treated = upload_folder + "/" + str(user)  + "/" + "in_treatment"


        os.makedirs(path_video)
        os.makedirs(path_treated)
        os.makedirs(path_in_treated)

    return path_user



def deplacement_video(video_name, path_user):

    current_path = upload_folder + "/" + str(video_name)
    deplacement_path = path_user + "/video/" + str(video_name)
    shutil.move(current_path, deplacement_path)



def uploading_file(request):
    """Here is a function for uploading files.
    We call the form, verif his validity, cleanning it, save it
    and return name of video for the next AJAX"""

    #Call form.
    form = video_upload_form(request.POST, request.FILES)

    #Post from template.²
    if request.method == 'POST' and request.user.is_authenticated:

        print("Uploading video.")

        #Verify validity of the form.
        if form.is_valid():

            print("Form uploading video is valid.")
            
            #Uploading file.
            name_video = request.FILES['docfile']                       #Recuperate the file.
            form.cleaned_data['docfile'].name                           #Cleanning.
            
            newdoc = video_upload(docfile = request.FILES['docfile'])   #Call model.

            path_user = verify_folder(request.user)
            newdoc.save()              #Saving.
            deplacement_video(name_video, path_user)


            print("video name's : ", str(name_video))

            return JsonResponse({"video_name" : str(name_video)})


    else:
        return JsonResponse({"error" : "coonection", "form": form})





def telechargement(request):

    form = video_upload_form(request.POST, request.FILES)
    context = {"form": form}
    return render(request, "telechargement.html", context)
















