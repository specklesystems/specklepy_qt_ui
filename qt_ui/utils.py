
from textwrap import wrap

def splitTextIntoLines(text: str = "", number: int= 40) -> str: 
    print("__splitTextIntoLines")
    #print(text)
    msg = ""
    try:
        if len(text)>number:
            try:
                lines = wrap(text, number)
                for i, x in enumerate(lines):
                    msg += x
                    if i!= len(lines) - 1: 
                        msg += "\n"
            except Exception as e: print(e)
        else: 
            msg = text
    except Exception as e:
        print(e)
        print(text)
    return msg

def constructCommitURL(streamWrapper, branch_id: str = None, commit_id: str = None) -> str:
    import requests 
    try:
        if isinstance(streamWrapper, tuple) or isinstance(streamWrapper, list):
            streamWrapper = streamWrapper[0]
        streamUrl = streamWrapper.stream_url.split("?")[0].split("&")[0].split("@")[0]
        r = requests.get(streamUrl)
        
        url = streamUrl 
        # check for frontend2 
        try: 
            header = r.headers['x-speckle-frontend-2']
            url = streamUrl.replace("streams", "projects") + "/models/" + branch_id + "@" + commit_id
        except:
            url = streamUrl.replace("projects", "streams") + "/commits/" + commit_id
        return url 
    except:
        pass 

def constructCommitURLfromServerCommit(serverURL: str, stream_id: str) -> str:
    import requests 
    r = requests.get(serverURL)
    
    # check for frontend2 
    try: 
        header = r.headers['x-speckle-frontend-2']
        #url = streamUrl.replace("streams", "projects") + "/models/" + branch_id + "@" + commit_id
        url = serverURL + "/projects/" + stream_id # replace with 'projects' after it's implemented in Specklepy
    except:
        url = serverURL + "/streams/" + stream_id
    return url 

#def removeSpecialCharacters(text: str) -> str:
#    new_text = text.replace("[","_").replace("]","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(":","_").replace("\\","_").replace("/","_").replace("\"","_").replace("&","_").replace("@","_").replace("$","_").replace("%","_").replace("^","_")
#    return new_text
