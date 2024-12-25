import requests
from requests.auth import HTTPBasicAuth

def toList(input, s):
    videos=input.split("\n")
    tmp = []
    for file in videos:
        if s in input:
            if ".thumb" in file:
                continue
            
            if file != "":
                tmp.append(f"videos/{file}" )
            
    return tmp

def get_file_lists(server_url,user,password):
    
    out=[""]
    try:
        response = requests.get(f"{server_url}", auth=HTTPBasicAuth(user, password))
        if response.status_code == 200:
            resp = response.text.splitlines()
            for r in resp:
                if ".mp4" in r or ".jpg" in r or ".png" in r:
                    if out[0]=="":
                        out[0]= r
                    out.append(r)
            return out
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_frames(video_url,user, password):
    try:
        response = requests.get(video_url, auth=HTTPBasicAuth(user, password))
        response.raise_for_status()
        return response.iter_lines()
    except requests.exceptions.RequestException as e:
        print(f"Failed to perform request: {e}")
