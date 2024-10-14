import json

from ray import serve

def parse_serve_status(serve_status):
    output = {
        "proxies": {},
        "applications": {}
    }

    # Parse proxy status
    for proxy_id, proxy_status in serve_status.proxies.items():
        output["proxies"][proxy_id] = proxy_status.name

    # Parse applications and deployments
    for app_name, app_info in serve_status.applications.items():
        app_overview = {
            "status": app_info.status.name,
            "last_deployed_time": app_info.last_deployed_time_s,
            "deployments": {}
        }
        for deployment_name, deployment_info in app_info.deployments.items():
            app_overview["deployments"][deployment_name] = {
                "status": deployment_info.status.name,
                "replica_states": deployment_info.replica_states,
                "message": deployment_info.message
            }
        output["applications"][app_name] = app_overview

    return json.dumps(output, indent=4)

def save_to_file(json_data, filename):
    with open(filename, 'w') as file:
        file.write(json_data)

status = serve.status()

formatted_output = parse_serve_status(status)

filename = "serve_status_output.json"
save_to_file(formatted_output, filename)
