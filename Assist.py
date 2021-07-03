import os


def get_duration_video(nameVideo):
    '''return duration of video'''
    cmd = str.format('''ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {0}''',nameVideo)
    duration = os.popen(cmd).read()
    return (int)(duration.split('.')[0])

def convert_video_to_audio(video_input,audio_output):
    cmd = str.format("ffmpeg -y -i {0} -vn {1}",video_input, audio_output)
    os.system(cmd)
    pass

def remove_segment_video(nameInput,nameOutput,timeSegment,frequency):
    duration = get_duration_video(nameInput)
    n = duration // frequency
    arr = []
    for i in range(n):
        strIndex = str.format("between(t,{0},{1})",i*frequency,(i+1)*frequency-timeSegment)
        arr.append(strIndex)
    between = str.join("+",arr)
    cmd = str.format('''ffmpeg -y -i {0} -vf "select='{1}', setpts=N/FRAME_RATE/TB" -af "aselect='{1}', asetpts=N/SR/TB" {2}''',nameInput,between,nameOutput)
    os.system(cmd)
    pass

def speedup_video(name_input,name_output,speed):
    cmd = str.format('''ffmpeg -y -i {0} -filter_complex "[0:a]atempo={1};[0:v]setpts=PTS/{1}" {2}''',name_input,speed,name_output)
    os.system(cmd)
    pass

def zoom_video(name_input, name_output, zoom):
    cmd = str.format('''ffmpeg -y -i {0} -filter_complex "[0:v]crop=in_w/{2}:in_h/{2},scale=1920x1080" -c:a copy {1}''',name_input,name_output,zoom)
    os.system(cmd)
    pass

def change_voice_video(name_input, name_output,frequence):
    '''change audio voice in video with keeping duration
    frequence < 1: giong tram
    frequence > 1: giong cao
    '''
    cmd = str.format('''ffmpeg -y -i {0} -filter_complex "[0:a]asetrate=44100*{2}, atempo=1/{2}" -c:v copy {1} ''',name_input,name_output,frequence)
    os.system(cmd)
    pass

def remove_logo(name_input,name_output,x,y,w,h):
    cmd = str.format('''ffmpeg -y -i {0} -vf "delogo=x={2}:y={3}:w={4}:h={5}" -c:a copy {1} ''',name_input,name_output,x,y,w,h)
    os.system(cmd)
    pass

def change_voice_audio(name_input, name_output,frequence):
    '''change audio voice in video with keeping duration
    frequence < 1: giong tram
    frequence > 1: giong cao
    '''
    cmd = str.format('''ffmpeg -y -i {0} -filter_complex "[0:a]asetrate=44100*{2}" {1} ''',name_input,name_output,frequence)
    os.system(cmd)
    pass


def hflip_video(nameInput,nameOutput):
    '''Dung de flip video'''
    cmd = str.format('''ffmpeg -y -i {0} -vf hflip -c:a copy {1}''',nameInput,nameOutput)
    os.system(cmd)
    pass

def boxblur_video(nameInput,nameOutput):
    cmd = str.format('''ffmpeg -y -i {0} -vf "boxblur=luma_radius=2:luma_power=1" -c:a copy {1}''',nameInput,nameOutput)
    os.system(cmd)
    pass

def get_file_in_folder(folderPath,extension = ".mp4"):
    if os.path.isdir(folderPath) ==False:
        return []
    fileNames = []
    for file in os.listdir(folderPath):
        if file.endswith(extension):
            fileNames.append(file)
    return fileNames

def render_thunho(nameInputs,_inputFolder,_outputFolder):
    print("Start render video...................")
    for nameInput in nameInputs:
        pathInput = _inputFolder + "\\" + nameInput
        pathOutput = _outputFolder + "\\output_thunho" + nameInput
        cmdRender = str.format(''' ffmpeg -y -i "{0}" -i "thumb.png" -filter_complex "[0:v]scale=960x730,setpts=PTS/1,pad=iw+8:ih+5:5:5:color=white,boxblur=0.5[v]; movie='videobgFHD.mp4':loop=999,setpts=N/(FRAME_RATE*TB)[bg]; [bg][v]overlay=shortest=1:x=2:y=150[v1]; [v1][1:v]overlay=0:0;   [0:a]atempo=1,bass=frequency=300:gain=-70,volume=+20dB,aecho=1:0.6:2:0.3,bass=g=3:f=110:w=20,bass=g=3:f=500:w=20,bass=g=3:f=300:w=30,bass=g=10:f=110:w=20,bass=g=20:f=110:w=40,firequalizer=gain_entry='entry(0,-23);entry(250,-11.5);entry(6000,0);entry(12000,8);entry(16000,16)',compand=attacks=4:decays=1:points=-90/-90 -70/-60 -15/-15 0/-10:soft-knee=1:volume=-70:gain=3,pan=stereo| FL < FL + 0.5*FC + 0.6*BL + 0.6*SL | FR < FR + 2*FC + 1*BR + 2*SR,highpass=f=300,lowpass=f=700,volume=10" -vcodec libx264 -pix_fmt yuv420p -r 48 -g 60 -b:v 1550k -shortest -acodec aac -b:a 128k -ar 44100 -map_metadata -1  -threads 0 -preset superfast "{1}"''',pathInput,pathOutput)
        os.system(cmdRender)
        pass
    print("Render video has finished............")
    pass

def filter_curves(name_input,name_output,filter_option):
    '''
    -option =
    none,
    color_negative,
    cross_process,
    darker,
    increase_contrast,
    lighter,
    linear_contrast,
    medium_contrast,
    negative,
    strong_contrast,
    vintage,
    '''
    cmd = str.format('''ffmpeg -y -i {0} -vf curves={2} -c:a copy {1}''',name_input,name_output,filter_option)
    os.system(cmd)

    pass

def loop_video(video_loop, loop_number,video_output,directory = ""):
    '''
    change directory before loop video
    '''
    os.chdir(directory)
    textFile = "list.txt"
    if os.path.isfile(textFile):
        os.remove(textFile)
    f = open(textFile,'a')
    for i in range(loop_number):
        f.write('file ' + video_loop + '\n')
        pass
    f.close()
    cmd = str.format("ffmpeg -y -f concat -safe 0 -i {0} -c copy {1}",textFile,video_output)
    os.system(cmd)
    pass

def render_xoay(nameInputs,skew,zoom,speed,_inputFolder,_outputFolder):
    for nameInput in nameInputs:
        pathInput = _inputFolder + "\\" + nameInput
        pathOutput = _outputFolder + "\\output_xoay_" + nameInput
        rotate_zoom_video(pathInput,skew, pathOutput,zoom,speed)
    pass

def rotate_zoom_video(pathInput,skew, pathOutput,zoom,speed):
    cmdRender = str.format('''ffmpeg -y -i "{0}" -filter_complex "[0:a]volume=1,aecho=0.8:0.9:50:0.3,atempo={4}[outA];[0:v]scale=1920x1080[v1];[0:v]scale=1920x1080[v2];[v2]rotate={1}[vRotate];[vRotate]crop=in_w/{3}:in_h/{3},scale=1920x1080[vZoom];[v1][vZoom]overlay=shortest=1:enable='lt(mod(t,5),2)*gte(t,2)':x=0:y=0[overlayV];[overlayV]colorbalance=rs=0:gs=0.6:bs=0,colorchannelmixer=aa=0.8[outV1];[outV1]setpts=PTS/{4}[outV]" -map [outV] -map [outA] -map_metadata -1 -threads 0 -preset superfast "{2}"''',pathInput,skew, pathOutput,zoom,speed)
    os.system(cmdRender)
    pass

def remove_audio(name_input,name_output):
    cmd = str.format('''ffmpeg -y -i {0} -an -c:v copy {1}''',name_input,name_output)
    os.system(cmd)
    pass

def add_audio_to_video(name_input,name_output,audio):
    cmd = str.format('''ffmpeg -y -i {0} -i {2} -map 0:v -map 1:a -c:v copy -shortest {1}''',name_input,name_output,audio)
    print(cmd)
    os.system(cmd)
    pass

def overlay_video(video_input, video_overlay, video_output,aa=0.25):
    '''
    aa
    Adjust contribution of input red, green, blue and alpha channels for output alpha channel. Default is 1 for aa, and 0 for ar, ag and ab.
    Allowed ranges for options are [-2.0, 2.0].
    '''
    cmd = str.format('''ffmpeg  -y -i "{0}" -i {1} -filter_complex "[0:a]volume=1[outA];[1:v]format=rgba,colorchannelmixer=aa={3}[fg];[0:v][fg]overlay=shortest=1[outV]" -map [outV] -map [outA] {2}''',video_input,video_overlay,video_output,aa)
    print(cmd)
    os.system(cmd)
    pass

def add_logo_to_video(input,logo,output,posistion):
    '''
    posistion = 1 ---- top_left
    posistion = 2 ---- top_right
    posistion = 3 ---- bottom_left
    posistion = 4 ---- bottom_right
    '''
    overlay = "(W-w)/2:(H-h)/2"
    if posistion == 1:
        overlay = "5:5"
    elif posistion == 2:
        overlay = "main_w-overlay_w-5:5"
    elif posistion == 3:
        overlay = "5:main_h-overlay_h"
    elif posistion == 4:
        overlay = "main_w-overlay_w-5:main_h-overlay_h-5"
    cmd = str.format('''ffmpeg -y -i {0} -i {1} -filter_complex "overlay={3}"  {2}''',input,logo,output,overlay)
    os.system(cmd)
    pass


def overlay_image_on_video(video_input, image_bg, video_output,scale):
    '''
    ovelay image on video
    '''
    cmd = str.format('''ffmpeg -y -i {0} -i {1} -filter_complex "[0:v]scale=in_w/{3}:in_h/{3}[fg];[1:v][fg]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" -shortest -c:a aac -b:a 128k {2}''',video_input, image_bg, video_output,scale)
    os.system(cmd)
    pass

def overlay_image_on_image(image_input, image_fg, video_output,scale):
    '''
    ovelay image on image
    '''
    cmd = str.format('''ffmpeg -y -i {0} -i {1} -filter_complex "[0:v]scale=in_w/{3}:in_h/{3}[fg];[1:v][fg]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2"  {2}''',image_input, image_fg, video_output,scale)
    os.system(cmd)
    pass

def cut_video(nameInput,nameOutput,startTime,durationTime):
    cmd = str.format('''ffmpeg -y -i {0} -ss {1} -t {2} -c:a copy -c:v copy {3}''',nameInput,startTime,durationTime,nameOutput)
    os.system(cmd)
    pass

def create_video_by_image_and_audio(image,audio,name_output):
    cmd = str.format(''' ffmpeg -y -loop 1 -i {0} -i {1} -shortest -c:a copy {2}''',image,audio,name_output)
    os.system(cmd)
    pass

def draw_text(input,output,txt,color,size,x,y):
    cmd = str.format('''ffmpeg -y -i {0} -vf "drawtext=text='{1}':x={5}:y={6}:fontsize={2}:fontcolor={3}"  {4}''',input,txt,size,color,output,x,y)
    print(cmd)
    os.system(cmd)
    pass

def load_json_str(pathJson):
    f = open(pathJson,'r')
    jsonStr = f.read()
    f.close()
    return jsonStr
