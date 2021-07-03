import os
import Assist as pAssist



work_folder = os.getcwd() + "/TrinhNgu/"

image_origin = work_folder + "image.jpg"
image_logo = work_folder + "image_logo.jpg"

nameVideo = "trinhngu"
origin_video = work_folder + nameVideo + ".webm"
origin_audio = work_folder + nameVideo +  ".mp3"
changer_audio = work_folder + nameVideo + "_changer.mp3"
video_image_audio = work_folder + nameVideo +  "_image_audio.mp4" # video was created by image + audio
video_overlayed = work_folder +  nameVideo + "_overlay.mp4" # video was crated by overlay 
video_logo = work_folder + nameVideo + "_logo.mp4" # 

video_1h = work_folder + nameVideo +  "1h.mp4"

effect_video = work_folder   + "flower_effect.mp4"
effect_video_loop = work_folder + "flower_effect_loop.mp4"


logo = work_folder + "logo.png"

def main():
    #Buoc 1 add logo to image
    pAssist.add_logo_to_video(image_origin,logo,image_logo,1)

    #Buoc 2 convert origin video to origin audio
    pAssist.convert_video_to_audio(origin_video,origin_audio)

    #Buoc 3 Create video from audio and image
    pAssist.create_video_by_image_and_audio(image_logo,origin_audio,video_image_audio)

    #Buoc 4 Loop effect Video
    duration = pAssist.get_duration_video(effect_video)
    loop_number = 1 + 300 // duration
    
    pAssist.loop_video(effect_video,loop_number,effect_video_loop,work_folder)

    #Buoc 5 overlay video
    pAssist.overlay_video(video_image_audio,effect_video_loop,video_overlayed)


    #Buoc 6 loop 1hour video
    duration = pAssist.get_duration_video(video_overlayed)
    loop_number = 1 + 3600 // duration
    pAssist.loop_video(video_overlayed,loop_number,video_1h)

    pass


main()