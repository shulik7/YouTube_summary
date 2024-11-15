import requests
import re
import sys


class YoutubeChannel:
    base_url = "https://www.youtube.com/watch?v="
    videos_html_suffix = "/videos"

    def __init__(self, url):
        self.url = url
        self.videos_html = self.get_videos_html()
        self.name = self.get_name()
        self.videos_info = self.get_videos_info()

    def get_name(self):
        if self.videos_html == "":
            self.videos_html = self.get_videos_html()

        return re.search("<title>(.+)\ -\ YouTube</title>", self.videos_html).groups()[
            0
        ]

    def get_videos_html(self):
        return requests.get(self.url + self.videos_html_suffix).text

    def get_videos_info(self):
        if self.videos_html == "":
            self.videos_html = self.get_videos_html()

        title_and_info = [
            x.rsplit(" by ", 1)
            for x in re.findall(
                '(?<={"label":")[^}]*?(?="}\}\},"descriptionSnippet")', self.videos_html
            )
        ]

        urls = re.findall('{"videoRenderer":{"videoId":"(.+?)",', self.videos_html)

        return [
            (x[0], re.search("views\ (.+?)\ ago", x[1]).groups()[0], self.base_url + y)
            for x, y in zip(title_and_info, urls)
        ]


if __name__ == "__main__":
    channel_url = sys.argv[1]
    youtube_channel = YoutubeChannel(channel_url)
    print(f"Channel name: {youtube_channel.name}")

    for i in youtube_channel.videos_info:
        print(i)
