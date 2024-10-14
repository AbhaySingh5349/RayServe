import starlette
from transformers import pipeline
from fastapi import FastAPI
from ray import serve

app = FastAPI()

@serve.deployment(name="Translation")
class Translator:
    def __init__(self):
        self.model = pipeline("translation_en_to_de", model="t5-small")

    def translate(self, text: str) -> str:
        return self.model(text)[0]["translation_text"]

    async def __call__(self, req: starlette.requests.Request):
        req = await req.json()
        return self.translate(req["text"])

# Create a FastAPI route
@app.post("/translate")
async def translate(text: str):
    translator = await serve.get_deployment("Translator").get_handle()
    return await translator.translate.remote(text)

# Bind the Translator deployment
serve_app = Translator.options(route_prefix="/translate").bind()
