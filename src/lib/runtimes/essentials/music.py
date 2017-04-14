import asyncio
import re
import urllib.request
import requests
import time
import math
import discord

def get_second():
    time_since_1970 = time.time()
    time_since_2000 = math.floor(time_since_1970 + 60 * 60 * 24 * 365 * 30)
    return time_since_2000


def url_check(url):
    try:
        site_ping = requests.head(url)
        if site_ping.status_code < 400:
            return True
    except Exception:
        return False


def find_name(url):
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
    cs = re.search('<meta property="og:title" content="', html).end()
    title = ""
    while html[cs] != ">":
        title += html[cs]
        cs += 1
    l = list(title)
    l.pop(len(l) - 1)
    return ''.join(l)


class Music:
    def __init__(self, client, message):
        self.voice = None
        self.client = client
        self.received = []
        self.songs = []
        self.message = message
        self.channel = message.author.voice.voice_channel
        self.player = None
        self.playing = False
        self.paused = False
        self.votes = []

    async def music_runtime(self):
        await self.create_voice_client(self.channel)
        while True:
            if len(self.received) != 0:
                if self.received[0].content.startswith(";music add "):
                    payload = list(self.received[0].content)
                    for i in range(11):
                        payload.pop(0)
                    url = ''.join(payload)
                    if url_check(url) is True:
                        if url.find("youtube") == -1:
                            await self.client.send_message(self.received[0].channel, "[**Music**] Not a valid youtube url!")
                        else:
                            self.songs.append([url, self.received[0].author.name, find_name(url)])
                            await self.client.send_message(self.received[0].channel, "[**Music**] " + self.songs[0][2] + " was added to the queue by "
                                                           + self.received[0].author.name)
                            self.message = self.received[0]
                    else:
                        await self.client.send_message(self.received[0].channel, "[**Music**] Not a valid youtube url!")
                elif self.received[0].content.startswith(";music playlist"):
                    string = ""
                    i2 = 0
                    for i in self.songs:
                        i2 += 1
                        string += str(i2) + ". " + i[2] + " " * 4 + "-- Suggested by: " + i[1] + "\n" * 2
                    if len(string) == 0:
                        string = "Playlist empty, add a new song with ;music add"
                    embed = discord.Embed(title="Playlist", description=string)
                    await self.client.send_message(self.received[0].channel, embed=embed)
                elif self.received[0].content.startswith(";music move"):
                    self.channel = self.received[0].author.voice.voice_channel
                    if self.channel is None:
                        await self.client.send_message(self.received[0].channel, "[**Music**] Please join a voice channel")
                    else:
                        try:
                            await self.voice.move_to(self.channel)
                        except Exception:
                            await self.client.send_message(self.received[0].channel, "[**Music**] Failed to join channel")
                elif self.received[0].content.startswith(";music skip"):
                    if self.playing:
                        if not self.received[0].author in self.votes:
                            self.votes.append(self.received[0].author)
                            if len(self.votes) == 1:
                                await self.client.send_message(self.received[0].channel, "[**Music**] " + self.received[0].author.name
                                                               + " called a vote to skip this song (one more person needed"
                                                                 " to skip)")
                            else:
                                await self.client.send_message(self.received[0].channel, "[**Music**] Skipping " +
                                                               self.player.title)
                                self.player.stop()
                        else:
                            await self.client.send_message(self.received[0].channel, "[**Music**] "
                                                                                     "You already voted to skip this"
                                                                                     " song " +
                                                           self.received[0].author.name + "!")
                elif self.received[0].content.startswith(";music pause"):
                    if self.playing and not self.paused:
                        self.player.pause()
                        await self.client.send_message(self.message.channel, "[**Music**] Paused " + self.player.title)
                        self.paused = True
                    elif not self.playing:
                        await self.client.send_message(self.message.channel, "[**Music**] There is no song playing")
                    elif self.paused:
                        await self.client.send_message(self.message.channel, "[**Music**] Songs already paused")
                elif self.received[0].content.startswith(";music resume"):
                    if self.playing and self.paused:
                        self.player.resume()
                        await self.client.send_message(self.message.channel, "[**Music**] Resumed " + self.player.title)
                        self.paused = False
                    elif not self.playing:
                        await self.client.send_message(self.message.channel, "[**Music**] There is no song playing")
                    elif not self.paused:
                        await self.client.send_message(self.message.channel, "[**Music**] Song is already playing")
                elif self.received[0].content.startswith(";music"):
                    pass
                self.received.pop(0)

            if not self.playing and len(self.songs) != 0:
                try:
                    self.player = await self.voice.create_ytdl_player(self.songs[0][0], after=self.done)
                    self.songs.pop(0)
                    self.playing = True
                    self.player.start()
                except Exception:
                    await self.client.send_message(self.message.channel, "[**Music**] Failed to play song.")
                try:
                    await self.client.send_message(self.message.channel, "[**Music**] Now playing: " + self.player.title)
                except Exception:
                    pass
            if self.playing:
                if not self.player.is_playing():
                    self.playing = False
            await asyncio.sleep(.01)
            if self.playing:
                if self.player.error is not None:
                    print("Error Occurred")
                    try:
                        self.done()
                        self.create_voice_client(self.channel)
                        self.player = None
                    except Exception:
                        print("Closing Socket")
                        return None

    def receive(self, payload):
        self.received.append(payload)

    async def create_voice_client(self, channel):
        self.voice = await self.client.join_voice_channel(channel)

    def done(self):
        print("Ubi> Song ended")
        self.playing = False
        self.votes = []
