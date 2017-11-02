#!/bin/bash
pulseaudio --start
echo -e "connect ${BLUETOOTH_SPEAKER_ADDRESS}" | bluetoothctl && sleep 5
pacmd set-card-profile ${BLUETOOTH_SPEAKER_CARD_NAME} a2dp
pacmd set-card-profile alsa_card.platform-soc_sound input:analog-stereo
