import requests
import starlette
from transformers import pipeline
from io import BytesIO
from PIL import Image
from fastapi import FastAPI
from ray import serve
from ray.serve.handle import DeploymentHandle

app = FastAPI()

@serve.deployment
def downloader(image_url: str):
    image_bytes = requests.get(image_url).content
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return image

@serve.deployment(name="Classification")
class ImageClassifier:
    def __init__(self, downloader: DeploymentHandle):
        self.downloader = downloader
        self.model = pipeline(
            "image-classification", model="google/vit-base-patch16-224"
        )

    async def classify(self, image_url: str) -> str:
        image = await self.downloader.remote(image_url)
        results = self.model(image)
        return results[0]["label"]

    async def __call__(self, req: starlette.requests.Request):
        req = await req.json()
        return await self.classify(req["image_url"])

# Create a FastAPI route
@app.post("/classify")
async def classify(image_url: str):
    classifier = await serve.get_deployment("ImageClassifier").get_handle()
    return await classifier.classify.remote(image_url)

# Bind the downloader and classifier together
serve_app = ImageClassifier.options(route_prefix="/classify").bind(downloader.bind())
