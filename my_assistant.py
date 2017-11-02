#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import sys
import random
import os
import subprocess

import aiy.assistant.auth_helpers
import aiy.voicehat
from playscroll import Player
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

player = Player(os.environ['EMAIL'], os.environ['GPASS'], os.environ['DEVICE_ID'])


def process_event(event, assistant):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        text = event.args['text']
        if text == "shut down":
            assistant.stop_conversation()
            aiy.audio.say("Goodbye")
            subprocess.call("sudo shutdown -h now", shell=True)
        if text == "self upgrade":
            assistant.stop_conversation()
            aiy.audio.say("Now upgrading packages...")
            status = subprocess.call("sudo apt-get update && sudo apt-get upgrade -y", shell=True)
            if status == 0:
                aiy.audio.say("Upgrade completed successfully.")
            else:
                aiy.audio.say("Sorry but I could not complete the upgrade.")
        elif "connect to the Bluetooth speaker" in text:
            assistant.stop_conversation()
            aiy.audio.say("Sure thing.")
            subprocess.call("/bin/bash startup.sh", shell=True)
            aiy.audio.say("Is this thing on?")
        elif text.startswith("play"):
            assistant.stop_conversation()
            playlist = text.replace("play","").strip()
            if player.load_playlist(playlist) is not None:
                aiy.audio.say("Playing " + playlist)
                player.start_playlist()
        elif text == "stop the music":
            assistant.stop_conversation()
            if player.playing:
                player.stop()
            else:
                aiy.audio.say("There is no music playing.")
        status_ui.status('ready')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(event, assistant)


if __name__ == '__main__':
    main()
