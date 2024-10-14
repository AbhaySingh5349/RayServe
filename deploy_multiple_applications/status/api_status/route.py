from fastapi import APIRouter, HTTPException

import requests

router = APIRouter(prefix="/applications", tags=["AppStatus"])

RAY_DASHBOARD_URL = "http://localhost:8265"

@router.get('/status', status_code=200)
def get_all_app_status():
    resp = requests.get(f"{RAY_DASHBOARD_URL}/api/serve/applications/")
    return resp.json()

@router.get('/{app_name}', status_code=200)
def get_app_status(app_name: str):
    resp = requests.get(f"{RAY_DASHBOARD_URL}/api/serve/applications/")
    applications = resp.json().get("applications", {})

    if app_name not in applications:
        raise HTTPException(status_code=404, detail="Application not found")

    return applications[app_name]

@router.get('/{app_name}/{deployment_name}', status_code=200)
def get_deployment_status(app_name: str, deployment_name: str):
    resp = requests.get(f"{RAY_DASHBOARD_URL}/api/serve/applications/")
    applications = resp.json().get("applications", {})

    if app_name not in applications:
        raise HTTPException(status_code=404, detail="Application not found")
    
    deployments = applications[app_name].get("deployments", {})
    
    if deployment_name not in deployments:
        raise HTTPException(status_code=404, detail="Deployment not found")

    return deployments[deployment_name]

@router.delete('/', status_code=200)
def delete_applications():
    try:
        resp = requests.delete(f"{RAY_DASHBOARD_URL}/api/serve/applications/")
        
        if resp.status_code == 200:
            if resp.content:
                return {"message": "Applications deleted successfully", "details": resp.json()}
            else:
                return {"message": "Applications deleted successfully", "details": "No content in response"}
        else:
            raise HTTPException(status_code=resp.status_code, detail=resp.json())
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ray dashboard: {str(e)}")