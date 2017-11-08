from gmusicapi import Mobileclient
from vlc import EventType, Instance
from threading import Thread
import json
import os.path

class Player(object):

    def __init__(self, email, password, device_id):
        self.api = Mobileclient()
        self.vlc = Instance()
        self.loaded_tracks = []
        self.playing = False
        self.thread_running = False
        self.player = self.vlc.media_player_new()
        self.track_index = -1
        self.api.login(email, password, device_id)

    def load_song(self, name):
        name = name.strip().lower()
        print("Looking for song: ", name)
        if os.path.isfile("songs.json"):
            # Load from file
            print("Found songs data.")
            with open('songs.json') as input_file:
                self.song_library = json.load(input_file)
        else:
            self.song_library = self.api.get_all_songs()
            # Save to file
            with open('songs.json', 'w') as output_file:
                json.dump(self.song_library, output_file)    

        for song_dict in self.song_library:
            song_name = song_dict['title'].strip().lower()
            if (song_name == name) or (name in song_name):
                print("Found match: ", song_dict['title'])
                self.loaded_tracks.append(song_dict)
                return song_dict['title']
            else:
                print("Song not found :(")
        return None

    def load_playlist(self, name):
        name = name.strip().lower()
        print("Looking for playlist: ", name)
        if os.path.isfile("playlists.json"):
            # Load from file
            print("Found playlist data.")
            with open('playlists.json') as input_file:
                self.playlists = json.load(input_file)
        else:
            self.playlists = self.api.get_all_user_playlist_contents()
            # Save to file
            with open('playlists.json', 'w') as output_file:
                json.dump(self.playlists, output_file)
            
        self.loaded_tracks = []
        for playlist_dict in self.playlists:
            playlist_name = playlist_dict['name'].strip().lower()
            if (playlist_name == name) or (name in playlist_name):
                print("Found match...", playlist_dict['name'])
                for track_dict in playlist_dict['tracks']:
                    self.loaded_tracks.append(track_dict)
                return playlist_dict['name']
            else:
                print("Found...", playlist_dict['name'])
        return None
 
    def end_callback(self, event, track_index):
        if track_index < len(self.loaded_tracks):
            self.play_song(self.loaded_tracks[track_index])
            event_manager = self.player.event_manager()
            event_manager.event_attach(EventType.MediaPlayerEndReached, self.end_callback, track_index + 1)
            self.playing = True
        else:
            self.playing = False

    def start_playlist(self):
        if len(self.loaded_tracks) > 0:
            self.track_index = 0
            self.play_song(self.loaded_tracks[self.track_index])
        
            if len(self.loaded_tracks) > 1:
                event_manager = self.player.event_manager()
                event_manager.event_attach(EventType.MediaPlayerEndReached, self.end_callback, 1)
  
    def play_song(self, song_dict):
        stream_url = ""
        if 'trackId' in song_dict:
          stream_url = self.api.get_stream_url(song_dict['trackId'])
        else:
          stream_url = self.api.get_stream_url(song_dict['nid'])
        media = self.vlc.media_new(stream_url)
        self.player.set_media(media)
        self.player.play()

        song_string = ""
        # for playlists there are track dictionaries
        if 'track' in song_dict:
            song_string = song_dict['track']['artist'] + " - " + song_dict['track']['title']
        else:
            song_string = song_dict['artist'] + " - " + song_dict['title']
        print("Playing ", song_string)
        
        self.playing = True

    def stop(self):
        if self.player != None:
            self.player.stop()
        self.thread_running = False
        self.playing = False

    def toggle_pause(self):
        if self.player != None:
            self.player.pause()

    def next(self):
        if self.player != None:
            if self.track_index < (len(self.loaded_tracks) - 1):
                self.track_index += 1
                self.play_song(self.loaded_tracks[self.track_index])

    def previous(self):
        if self.player != None:
            if self.track_index > 0:
                self.track_index -= 1
                self.play_song(self.loaded_tracks[self.track_index])
