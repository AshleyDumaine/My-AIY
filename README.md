My AIY
======

The code I'm using on my Google AIY (most logic comes from 
https://github.com/google/aiyprojects-raspbian/tree/voicekit)

## What can it do?
#### Regular Google Assistant stuff
Personally I have fun using Google Assistant's [Easter eggs]
(https://www.reddit.com/r/aiyprojects/comments/6ab6p5/some_of_the_aiy_easter_eggs/), 
but it can do basic Google Assistant things like conversions, setting timers, etc. 

#### Music
I wanted to integrate with Google Music and hook this up to my BlueTooth speaker
to play songs with voice commands but alas, the assistant does not seem to have
Google Music functionality built-in. Oddly it says the functionality is
supported when asking it to "play some music", but it gets confused when asked
to play a genre, album, song, etc. I used [this repo]
(https://github.com/Tom-Archer/gmusicaiy) to help get around
the issue somewhat, but it only supports playlists on your account as opposed to
genres, albums, or specific songs. The repo documentation is slightly out of
date now that `actor.add_keyword` is deprecated in the AIY code.

#### Voice shutdown
Pretty basic, but useful for when I don't want to leave it running all day.

#### Package upgrades
So I can make sure everything's the latest and greatest. Eventually I'll
probably have it update its own code too.

## Dependencies
For the music to work, you'll need to install gmusicapi with
```
pip install gmusicapi
```
and vlc with
```
sudo apt-get install vlc
```

## Known Issues
Right now it seems the RasPi 3 has issues with Bluetooth connectivity, at least
for the built-in dongle. I'm able to play music through my Bluetooth speaker
(although the sound quality isn't that great due to a [known issue with WiFI and
Bluetooth compatibility on RasPi 3s](https://github.com/raspberrypi/linux/issues/1402),
but it cuts out eventually with the following in `journalctl -r`:
```
Nov 05 19:50:54 google-aiy kernel: Bluetooth: hci0 link tx timeout
<working fine for the stream besides a few skipped microseconds>
```
It seems it's not an uncommon issue for others as well:
https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=166564
Aside from possibly disabling WiFi and/or using a Bluetooth dongle, I don't
really have a solution to the issue other than using the AIY's speaker, but then
Google Assistant will likely be unable to hear you over its own speaker since the
mic is right next to it.
