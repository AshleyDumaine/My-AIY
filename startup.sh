#!/bin/bash
pulseaudio --start --realtime --no-cpu-limit -D
echo -e "connect ${BLUETOOTH_SPEAKER_ADDRESS}" | bluetoothctl
if [[ `pacmd list-cards | sed -n '1 p'` == "2"* ]] ; then
  pacmd set-card-profile ${BLUETOOTH_SPEAKER_CARD_NAME} a2dp
  pacmd set-card-profile alsa_card.platform-soc_sound input:analog-stereo
else
  pacmd set-card-profile alsa_card.platform-soc_sound output:analog-stereo+input:analog-stereo
fi
amixer sset Master 55%
