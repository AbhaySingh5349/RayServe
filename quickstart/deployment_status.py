from starlette.requests import Request
from starlette.responses import JSONResponse
import ray
from ray import serve

@serve.deployment(route_prefix="/status")
class StatusCheck:
    async def __call__(self, request: Request):
        # Use Ray Serve's built-in function to list deployments and their status
        deployments = serve.list_deployments()
        deployment_status = {name: deployment.to_dict() for name, deployment in deployments.items()}
        return JSONResponse(deployment_status)
    
status_check_app = StatusCheck.bind()

serve.run(status_check_app)

# import requests

# # Check the status of the deployment
# status_response = requests.get("http://127.0.0.1:8000/status")
# status_info = status_response.json()

# print("Deployment Status: ", status_info)
