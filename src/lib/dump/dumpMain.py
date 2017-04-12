import requests


def url_check(url):
    try:
        site_ping = requests.head(url)
        if site_ping.status_code < 400:
            return True
    except Exception:
        return False

url = "https://www.youtube.com/watch?v=VuCy2Dq7rEI"
print(url_check(url))
print(url.find("youtube"))