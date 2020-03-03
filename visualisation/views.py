import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path = os. getcwd()
path_current = os.path.basename(path)


from django.shortcuts import render
from .paths import *

from django.http import JsonResponse

from .app.paths import dlib_model, eyes_image, blink_image



from .app.pre_treatment.pre_test import search_video_size
from .app.pre_treatment.writter import video_writter

from .app.recuperate_points.face_points import load_model_dlib
from .app.video_capture_to_face_APP_2 import video_capture_to_face


def visualisation(request):

    if request.method == 'POST':

        username = request.user
        video = request.POST.get('video')

        no_register = request.POST.get('no_register')
        register = request.POST.get('register')

        if video:

            video_path_media = BASE_DIR + "/" + video

            predictor, detector = load_model_dlib(dlib_model)

            video_size = search_video_size(video_path_media, predictor, detector, dlib_model)
            print(video_size)

            video_capture_to_face(video_path_media, video, eyes_image,
                                  blink_image, username, video_size)

            response = {"user": str(username)}

            return JsonResponse(response)


        elif no_register:
            path1 = in_treatment_video.format(str(username), "visualisation1.mp4")
            path2 = in_treatment_video.format(str(username), "visualisation2.mp4")

            os.remove(path1)
            os.remove(path2)

            return JsonResponse({"ok" : "ok"})

        elif register:
            path1 = in_treatment_video.format(str(username), "visualisation1.mp4")
            path2 = in_treatment_video.format(str(username), "visualisation2.mp4")

            os.remove(path2)

            liste = os.listdir(treated_video_path.format(str(username)))

            if liste == []:
                shutil.move(path1, treated_video.format(str(username), "visualisation1.mp4"))

            else:
                liste = sorted(liste)

                name = liste[-1][:-3]
                nb = ""
                for i in name:
                    try:
                        i = int(i)
                        if i == int(i):
                            nb += str(i)
                    except:
                        pass
  
                nb = int(nb)

                name = "visualisation" + str(nb + 1) + ".mp4"

                os.rename(in_treatment_video.format(str(username), "visualisation1.mp4"),
                          in_treatment_video.format(str(username), name))

                shutil.move(in_treatment_video.format(str(username), name),
                            treated_video.format(str(username), name))

                return JsonResponse({"ok" : "ok"})

    else:

        username = request.user
        path_user = upload_folder + "/" + str(username) + "/video"
        user_list = os.listdir(path_user)

        path_user_treated = upload_folder + "/" + str(username) + "/treated"
        path_user_treated = os.listdir(path_user_treated)

        liste_path = [upload_video.format(username, i) for i in user_list]
        liste_treated = [treated_video_path1.format(username, i) for i in path_user_treated]

        
        context = {"video_user": liste_path, "liste_treated":liste_treated}

        return render(request, "visualisation.html", context)
