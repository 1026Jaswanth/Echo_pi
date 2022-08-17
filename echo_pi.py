from os import listdir
from pygame import mixer
from random import shuffle
from time import sleep
import RPi.GPIO as GPIO
import os
string3 = 'ipaddress'
string4 = 'and'
string5 = 'ssid'
ipaddress = os.popen("hostname -I").read()
ssid = os.popen("iwconfig wlan0 \
                | grep 'SSID' \
                | awk '{print $4}' \
                | awk -F\\\" '{print $2}'").read()

string1 = ipaddress
string2 = ssid
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(4, GPIO.IN)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
mixer.init()
prev_input1 =0
prev_input2 =0
prev_input3 =0
prev_input4 =0
prev_input5 =0
prev_input6 =0
prev_input7 =0


playlist = listdir('/home/b/music/')
active_playlist = playlist
shuffled_playlist = []


file_range = len(playlist) - 1

logic=0
music_option = True
shuffle_music = False
indexed_track = 0
display_track = indexed_track + 1
is_stopped = True
is_paused = False
is_started = False
repeat_track = False
repeat_all = False



def shuffle_playlist():
    global shuffle_music, playlist, is_started, shuffled_playlist, indexed_track, is_stopped, active_playlist
    indexed_track = 0
    if shuffle_music:
        shuffle_music = False
        active_playlist = playlist
    else:
        shuffle_music = True
        shuffle(playlist)
        shuffled_playlist = playlist
        playlist = listdir('/home/b/music')
    



def repeat_loop():
    global repeat_all, repeat_track
    if not repeat_track and not repeat_all:
        repeat_track = True

    elif repeat_track:
        repeat_track = False
        repeat_all = True

    elif repeat_all:
        repeat_all = False

def start_music():
    global indexed_track, is_started, is_stopped, active_playlist

    if shuffle_music:
        active_playlist = shuffled_playlist
    else:
        active_playlist = playlist

    while not mixer.music.get_busy() and not is_stopped and not is_paused and not is_started:
        mixer.music.load(f"/home/b/music/{active_playlist.__getitem__(indexed_track)}")
        mixer.music.play(-1)
        is_started = True
    while mixer.music.get_busy():
        GPIO.output(24, GPIO.LOW)
        sleep(1)
        GPIO.output(24, GPIO.HIGH)
        sleep(0.5)
        break

    else:
        print("i started")
        if not is_stopped and not is_paused:
            
            if not repeat_all and not repeat_track and indexed_track == file_range:
                stop_music()
    
            
            elif repeat_track:
                indexed_track -= 1
    
            
            indexed_track += 1
            is_started = False
    
            
            if indexed_track < 0 or indexed_track > file_range:
                indexed_track = 0
            start_music()



def music_status():
    music_yes = mixer.music.get_busy()
    return music_yes



def stop_music():
    global is_stopped, is_started, indexed_track, repeat_all, repeat_track
    GPIO.output(24, GPIO.LOW)
    if is_stopped:
        indexed_track = 0
        repeat_all = False
        repeat_track = False
        
    mixer.music.stop()
    is_stopped = True
    is_started = False
    start_music()



def next_track():
    global indexed_track, is_started
    
    music_playing = music_status()
    if music_playing:
        mixer.music.stop()
        if indexed_track == file_range:
            indexed_track = 0
            is_started = False
        start_music()

    
    else:
        if indexed_track != file_range:
            indexed_track += 1
        else:
            indexed_track = 0



def prev_track():
    global indexed_track, is_started
    music_playing = music_status()
    if music_playing:
        if display_track == 1:
            indexed_track -= 1
            is_started = False
        else:
            indexed_track = file_range
        mixer.music.stop()
        start_music()
    else:
        if indexed_track != 0:
            indexed_track -= 1
        else:
            indexed_track = file_range


def play_track():
    global is_paused, is_stopped, logic
    music_playing = music_status()
    print("start")
    
    if music_playing and logic == 0:
        is_paused = True
        mixer.music.pause()
        logic = 1

    
    elif logic == 1:
        is_paused = False
        mixer.music.unpause()
        logic = 0

    
    is_stopped = False
    start_music()

def volumedown():
    mixer.music.set_volume(mixer.music.get_volume() - 0.1)
def volumeup():
    mixer.music.set_volume(mixer.music.get_volume() + 0.1)
mixer.music.load("/home/b/codes/mp.mp3")
mixer.music.play(0)
while 1:
    input_1 = GPIO.input(22)
    if ((not prev_input1) and input_1):
        print("prev_track pressed")
        prev_track()
    prev_input1 = input_1
    sleep(0.05)
    
    input_2 = GPIO.input(23)
    if ((not prev_input2) and input_2):
        print("nxt_track pressed")
        next_track()
    prev_input2 = input_2
    sleep(0.05)
    
    input_3 = GPIO.input(17)
    if ((not prev_input3) and input_3):
        print("play pressed")
        play_track()
    prev_input3 = input_3
    sleep(0.05)  
    
    input_4 = GPIO.input(27)
    if ((not prev_input4) and input_4):
        print("stop pressed")
        stop_music()
    prev_input4 = input_4
    sleep(0.05)

    input_5 = GPIO.input(14)
    if ((not prev_input5) and input_5):
        print("vol up pressed")
        volumeup()
    prev_input5 = input_5
    sleep(0.05)
    
    input_6 = GPIO.input(15)
    if ((not prev_input6) and input_6):
        print("vol down pressed")
        volumedown()
    prev_input6 = input_6
    sleep(0.05)
    
    input_7 = GPIO.input(4)
    if ((not prev_input7) and input_7):
        print("ip&ssid pressed")
        os.system(f'echo "{string3}" "{string1}" "{string4}" "{string5}"+"{string2}"   | festival --tts')
    prev_input7 = input_7
    sleep(0.05)
