from communex.module import Module, endpoint
from communex.key import generate_keypair
from keylimiter import TokenBucketLimiter
import os

from openai import OpenAI


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
        modelname: str = "accounts/fireworks/models/llama-v2-34b-code-instruct"
    ) -> None:
        super().__init__()
        inference_url = os.getenv("DANKSY_INFERENCE_URL")
        inference_api_key = os.getenv("DANKSY_INFERENCE_API_KEY")
        if inference_url is None:
            raise Exception("DANKSY_INFERENCE_URL env variable not set")
        self.inference_client = OpenAI(
            base_url = inference_url,
            api_key = inference_api_key
        )

        self.modelname = modelname
        
    

     """
        Generates a response to a given prompt using a specified model.

        Args:
            prompt: The prompt to generate a response for.

        Returns:
            str: The response formatted as a string
        """
    @endpoint
    def generate(self, prompt: str):
        """
        By default, we call fireworks api with a default model. 
        As long as a proper response (formatted as a string) is returned, feel free to modify the code to use any number of models or API providers
        """

        chat_completion = self.inference_client.chat.completions.create(
        model=self.modelname,
        messages=[
        {
            "role": "user",
            "content": prompt,
        },
         ],
        )
        resp = chat_completion.choices[0].message.content
        return resp

if __name__ == "__main__":
    """
    Start the miner instance, feel free to modify as needed to use other models or LLM inference providers
    """
    from communex.module.server import ModuleServer
    import uvicorn

    key = generate_keypair()
    miner = Miner()
    refill_rate = 1 / 400
    # Implementing custom limit
    bucket = TokenBucketLimiter(2, refill_rate)
    server = ModuleServer(miner, key, ip_limiter=bucket, subnets_whitelist=[3])
    app = server.get_fastapi_app()

    # Only allow local connections
    uvicorn.run(app, host="127.0.0.1", port=8000)
