import urllib.request
import re
import random


def main():
    save = str(random.randint(1111, 9999))
    with urllib.request.urlopen('https://c.xkcd.com/random/comic/') as response:
        html = response.read().decode('utf-8')
    cs = re.search("Image URL", html).end()
    css = cs + 29
    developed = ""
    while not html[css] + html[css + 1] + html[css + 2] + html[css + 3] == ".jpg" and not html[css] + html[css + 1] + \
            html[css + 2] + html[css + 3] == ".png":
        developed += html[css]
        css += 1
    developed += html[css] + html[css + 1] + html[css + 2] + html[css + 3]
    fs = save + html[css] + html[css + 1] + html[css + 2] + html[css + 3]
    urllib.request.urlretrieve(developed, "server/bin/comics" + fs)
    return [["fileRemove", "server/bin/comics" + fs]]
