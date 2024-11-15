import sys
import json

from youtube_channel import YoutubeChannel
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.prompts import PromptTemplate

from model_helper import ModelHelper
from time_converter import TimeConverter
from transcript_processor import TranscriptProcessor


def get_youtube_channels(channel_file):
    with open(channel_file) as f:
        return [YoutubeChannel(y) for y in (x.rstrip() for x in f.readlines())]


def filter_video(videos_info, time_window_minutes):
    for name, time, url in videos_info:
        time_in_minutes = time_converter.to_minutes(time)
        if time_in_minutes <= time_window_minutes:
            yield (name, time, url)
            continue

        break


if __name__ == "__main__":
    channel_file = sys.argv[1]
    time_window = sys.argv[2]
    output_file = sys.argv[3]

    youtube_channels = get_youtube_channels(channel_file)

    llm = ModelHelper.get_model()
    time_converter = TimeConverter(llm)
    time_window_minutes = time_converter.to_minutes(time_window)
    results = {
        "timeWindow": time_window,
        "timeWindowMinutes": time_window_minutes,
        "channels": [],
    }

    processor = TranscriptProcessor(llm)

    for channel in youtube_channels:
        this_channel = {"channelName": channel.name, "videos": []}

        for name, time, url in filter_video(channel.videos_info, time_window_minutes):
            summary = processor.process(url)["output_text"]
            this_channel["videos"].append(
                {"videoName": name, "videoAge": time, "url": url, "summary": summary}
            )

        results["channels"].append(this_channel)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
