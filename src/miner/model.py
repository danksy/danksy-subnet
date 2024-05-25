import os

from communex.module import Module, endpoint
from openai import OpenAI

from subnet.utils import logger


class Miner(Module):
    """
    A module class for mining and generating responses to prompts.

    Attributes:
        inference_client: A client that will generate an LLM inference response. Can be locally run or fetched from an API

    Methods:
        generate: Generates a response to a given prompt using a specified model.
    """

    def __init__(
            self,
            model_name: str = "accounts/fireworks/models/llama-v3-70b-instruct",
            inference_url: str = "https://api.fireworks.ai/inference/v1",
    ) -> None:
        super().__init__()
        inference_url = os.getenv("DANKSY_INFERENCE_URL") or inference_url
        inference_api_key = os.getenv("DANKSY_INFERENCE_API_KEY")
        model_name = os.getenv("DANKSY_INFERENCE_MODEL_NAME") or model_name
        if inference_api_key is None:
            raise Exception("DANKSY_INFERENCE_API_KEY env variable not set")
        self.inference_client = OpenAI(
            base_url=inference_url,
            api_key=inference_api_key,
        )
        self.model_name = model_name
        return

    def _inference(self, prompt: str) -> str:
        try:
            chat_completion = self.inference_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            response = chat_completion.choices[0].message.content
            return response
        except Exception as e:
            logger.error(e)
            return ""

    """
        Generates a response to a given prompt using a specified model.

        Args:
            prompt: The prompt to generate a response for.

        Returns:
            str: The response formatted as a string
    """

    @endpoint
    def generate(self, prompt: str) -> dict[str, str]:
        """
        By default, we call fireworks api with a default model. 
        As long as a proper response (formatted as a string) is returned, feel free to modify the code to use any number of models or API providers
        """
        resp = self._inference(prompt)
        logger.info(f"technical response was {resp}")
        return {"answer": resp}
