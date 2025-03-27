# tools : is_endpoint_running, invoke_model
# uv --derectory DERECTORY run main_lsschool.py

import json

import boto3
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mlschool")

@mcp.tool()
async def is_endpoint_running(endpoint: str) -> bool:
    """Check if a SsageMaker endpoint is currently running.
    
    Args:
        endpoint: The name of the sageMaker endpoint to check

    Returns:
        bool: True if the endpoint is in service, False otherwise
    """
    try:
        sagemaker_clien = boto3.client("sagemaker")
    except Exception as e:
        print(f"Error checing endpoint status: {e}")
        return False
    
@mcp.tool()
async def invoke_model(payload: list[dict]) -> str:
    """Invoke a hosted model with the give payload array.

    Args:
        payload: the paload to invoke the model with. The payload is an array of dictionaries,
        each representing a sample. Here is an example payload:

        ```
        [
            {"island": "Biscoe", "culmen_length_mm": 48.6, "culmen_depth_mm": 16.0, "flipper_length_mm": 230.0, "body_mass_g":5000.0},
            {"island": "Biscoe", "culmen_length_mm": 48.6, "culmen_depth_mm": 16.0, "flipper_length_mm": 230.0, "body_mass_g":5000.0},
            {"island": "Biscoe", "culmen_length_mm": 48.6, "culmen_depth_mm": 16.0, "flipper_length_mm": 230.0, "body_mass_g":5000.0}            
        ]
        ```

    Returns:
        str: The response from the model
    
    """
    endpoint_url = "http://127.0.0.1:8080/invocations"
    headers = {"Content-Type": "application/json"}

    try:
        predictions = requests.post(
            url=endpoint_url,
            headers=headers,
            data=json.dump(
                {
                    "inputs": payload,
                }
            ),
            timeout=5,
        )
        return predictions.json()
    
    except Exception as e:
        print(f"Error invoking model: {e}")
        return str(e)
    
if __name__ == "__main__":
    # Start the MCP server
    mcp.run()