import sys

from langchain.chains import LLMChain, StuffDocumentsChain
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.prompts import PromptTemplate


from model_helper import ModelHelper


class TranscriptProcessor:

    def __init__(self, model):
        self.model = model

    def process(self, input):
        system_prompt = "please summarize "
        prompt_template = system_prompt + "{text}"
        prompt = PromptTemplate.from_template(prompt_template)

        llm_chain = LLMChain(llm=self.model, prompt=prompt)
        chain = StuffDocumentsChain(llm_chain=llm_chain, input_key="text")
        loader = YoutubeLoader.from_youtube_url(
            input,
            add_video_info=True,
            language=["en", "en-US", "zh", "zh-Hans", "zh-Hant", "zh-TW"],
            translation="en",
        )
        youtube_transcript = loader.load()

        return chain.invoke(youtube_transcript)


if __name__ == "__main__":

    input = sys.argv[1]

    processor = TranscriptProcessor(ModelHelper.get_model("llama3.1"))

    response = processor.process(input)
    print(response["output_text"])
