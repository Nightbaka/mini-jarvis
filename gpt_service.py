import openai
import os
import subprocess
from pathlib import Path

def send_request(request):
    bing_script_path = Path("bing_integration/bing.js")
    bing_request = subprocess.run(["node", bing_script_path, request], stderr= subprocess.PIPE, stdout= subprocess.PIPE)
    response, error = bing_request.communicate()
    return response, error

if __name__ == "__main__":
    send_request("hello world")