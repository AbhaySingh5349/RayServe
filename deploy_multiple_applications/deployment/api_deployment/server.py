# # uvicorn main:app --host 0.0.0.0 --port 8000

import ray
from fastapi import FastAPI
from ray import serve

from image_classifier import serve_app as image_classifier_app
from text_translator import serve_app as text_translator_app

app = FastAPI()

# Start Ray and Serve
ray.init()
serve.start()

# Deploy the applications
serve.run(image_classifier_app)
# serve.run(text_translator_app)

# FastAPI route for health check
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

########################################################

# import ray
# from fastapi import FastAPI, Request
# from ray import serve
# from image_classifier import ImageClassifier, downloader
# from text_translator import Translator

# # Create a FastAPI app
# app = FastAPI()

# # Initialize Ray and Serve
# ray.init(ignore_reinit_error=True)
# serve.start()

# # Deploy Ray Serve applications
# downloader._deploy()
# ImageClassifier._deploy(downloader)
# Translator._deploy()

# # FastAPI route for image classification
# @app.post("/classify")
# async def classify(req: Request):
#     body = await req.json()
#     image_url = body["image_url"]
    
#     # Call the Ray Serve deployment
#     classifier = ImageClassifier.get_handle()
#     result = await classifier.classify.remote(image_url)
#     return {"label": result}

# # FastAPI route for text translation
# @app.post("/translate")
# async def translate(req: Request):
#     body = await req.json()
#     text = body["text"]
    
#     # Call the Ray Serve deployment
#     translator = Translator.get_handle()
#     result = await translator.translate.remote(text)
#     return {"translation": result}

# # FastAPI route for health check
# @app.get("/health")
# def health():
#     return {"status": "ok"}



#########################


# import ray
# from fastapi import FastAPI, Request
# from ray import serve
# from image_classifier import ImageClassifier, downloader
# from text_translator import Translator

# # Initialize Ray
# ray.init(ignore_reinit_error=True)

# # Create a FastAPI app
# app = FastAPI()

# # Ray Serve Application
# @serve.deployment
# @serve.ingress(app)  # Ingress FastAPI to allow FastAPI routing
# class FastAPIIngress:
#     def __init__(self):
#         pass

#     @app.post("/classify")
#     async def classify(self, req: Request):
#         body = await req.json()
#         image_url = body["image_url"]
        
#         # Call the Ray Serve deployment
#         classifier = await serve.get_deployment("ImageClassifier").get_handle()
#         result = await classifier.classify.remote(image_url)
#         return {"label": result}

#     @app.post("/translate")
#     async def translate(self, req: Request):
#         body = await req.json()
#         text = body["text"]
        
#         # Call the Ray Serve deployment
#         translator = await serve.get_deployment("Translator").get_handle()
#         result = await translator.translate.remote(text)
#         return {"translation": result}

#     @app.get("/health")
#     def health(self):
#         return {"status": "ok"}

# # Deploy Ray Serve applications
# downloader.deploy()
# ImageClassifier.deploy(downloader)
# Translator.deploy()

# # Deploy FastAPI Ingress (it will be deployed via Ray Serve)
# FastAPIIngress.deploy()

# # Start the Serve application
# serve.run(FastAPIIngress.bind())
