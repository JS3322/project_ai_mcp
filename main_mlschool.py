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
    
    """
    try:
        sagemaker_clien = boto3.client("sagemaker")
    except Exception as e:
        print(f"Error checing endpoint status: {e}")
        return False
    