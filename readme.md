# **Echo-Echo-Rpi**
## _Pre requisites to develop_
* install 32 rpi desktop os/ lite os 
* updtae the config.txt file
* installing samba 
* installing pygame

>sudo nano /boot/config.txt
```
gpio=18,13,a5
audio_pwm_mode=2
dtoverlay=audremap,pins_18_13
```
## Testing the Ouput 
 >speaker-test -c2 -twav -l7
 
 Now the output will be audible but it has to be chosen from which the output has to be obtained.
 >cat /proc/asound/modules
 
 This shows the audio devices available and thebelow command gives the output from specific device
 
 >speaker-test -c2 -twav -l7 -D plughw:N,0

where N is the number(0 or 1 or 2) before snd_usb_audio.

## Testing with audio players 
 The omxplayer or VLC player are compatible with the rpi 0 2 W

## Installing Samba server

>sudo apt-get install samba samba-common-bin

>sudo nano /etc/samba/smb.conf

edit the _.conf_ file add the below at last section

```
[pihome]
   comment= Pi Home
   path=/home/b
   browseable=Yes
   writeable=Yes
   only guest=no
   create mask=0777
   directory mask=0777
   public=no
```
>sudo smbpasswd -a pi

replace pi with default username

set id and password for sftp server and restart the service 

>sudo systemctl restart smbd

## pygame installation
>sudo apt-get install python3-pygame

>sudo apt-get install libsdl2-mixer-2.0-0

command alternative for bash gpio control

>>raspi-gpio help

>>>sudo systemctl enable PiPlayer.service

## finding ip adress and ssid using text to speech installations
>sudo apt-get install festival -y
## nodered wifi changer 

install nodered

install node-red-dashboard in manage pallete and import nodered flow 

## References
https://flows.nodered.org/flow/c3c7a393b05f6383b888bdee39aa5fa5

https://peakup.org/blog/how-to-setup-raspberry-pi-as-access-point-router-ap-hotspot/#:~:text=Raspberry%20Pi%20(Rpi)%203%20has,use%20Raspberry%20Pi%20as%20router.

https://sites.google.com/view/steam-for-vision/raspberry-pi/text-to-speech
