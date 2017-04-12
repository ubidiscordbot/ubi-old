import asyncio
import re
import urllib.request
import requests


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
        self.msg = None
        self.received = []
        self.songs = []
        self.message = message
        self.channel = message.author.voice.voice_channel
        self.player = None
        self.playing = False
        self.votes = []
        print("initiated")

    async def music_runtime(self):
        await self.create_voice_client(self.channel)
        while True:
            if len(self.received) != 0:
                if self.received[0].content.startswith("$music add "):
                    payload = list(self.received[0].content)
                    for i in range(11):
                        payload.pop(0)
                    url = ''.join(payload)
                    if url_check(url) is True:
                        if url.find("youtube") == -1:
                            await self.client.send_message(self.received[0].channel, "```Not a valid youtube url!```")
                        else:
                            self.songs.append([url, self.received[0].author.name, find_name(url)])
                            await self.client.send_message(self.received[0].channel, "```" + self.songs[0][2] + " was added to the quene by "
                                                           + self.received[0].author.name + "```")
                            self.message = self.received[0]
                    else:
                        await self.client.send_message(self.received[0].channel, "```Not a valid youtube url!```")
                elif self.received[0].content.startswith("$music playlist"):
                    await self.client.send_message(self.received[0].channel, "```Playlist```")
                    string = ""
                    i2 = 0
                    for i in self.songs:
                        i2 += 1
                        string += str(i2) + ". " + i[2] + " " * 4 + "Suggested by: " + i[1] + "\n" * 2
                    if len(string) == 0:
                        string = "Playlist empty, add a new song with $music add"
                    await self.client.send_message(self.received[0].channel, "```" + string + "```")
                elif self.received[0].content.startswith("$music move"):
                    self.channel = self.received[0].author.voice.voice_channel
                    if self.channel is None:
                        await self.client.send_message(self.received[0].channel, "Please join a voice channel")
                    else:
                        try:
                            await self.voice.move_to(self.channel)
                        except Exception:
                            await self.client.send_message(self.received[0].channel, "Failed to join channel")
                elif self.received[0].content.startswith("$music skip"):
                    if self.playing:
                        if not self.received[0].author in self.votes:
                            self.votes.append(self.received[0].author)
                            if len(self.votes) == 1:
                                await self.client.send_message(self.received[0].channel, "```" + self.received[0].author.name
                                                               + " called a vote to skip this song (one more person needed"
                                                                 " to skip)```")
                            else:
                                await self.client.send_message(self.received[0].channel, "```Skipping " +
                                                               self.player.title + "```")
                                self.player.stop()
                        else:
                            await self.client.send_message(self.received[0].channel, "```"
                                                                                     "You already voted to skip this"
                                                                                     " song " +
                                                           self.received[0].author.name + "!```")
                elif self.received[0].content.startswith("$music"):
                    pass
                self.received.pop(0)

            if not self.playing and len(self.songs) != 0:
                self.player = await self.voice.create_ytdl_player(self.songs[0][0], after=self.done)
                self.songs.pop(0)
                self.playing = True
                self.player.start()
                try:
                    await self.client.send_message(self.message.channel, "```Now playing: " + self.player.title + "```")
                except Exception:
                    pass
            await asyncio.sleep(.01)

    def receive(self, payload):
        self.received.append(payload)

    async def create_voice_client(self, channel):
        self.voice = await self.client.join_voice_channel(channel)

    def done(self):
        print("Done")
        self.playing = False
        self.votes = []
