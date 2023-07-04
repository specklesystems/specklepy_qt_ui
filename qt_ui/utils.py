
from textwrap import wrap

def splitTextIntoLines(text: str = "", number: int= 70) -> str: 
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

def constructCommitURLfromServerCommit(serverURL: str, stream_id: str) -> str:
    import requests 
    r = requests.get(serverURL)
    
    # check for frontend2 
    try: 
        header = r.headers['x-speckle-frontend-2']
        #url = streamUrl.replace("streams", "projects") + "/models/" + branch_id + "@" + commit_id
        url = serverURL + "/streams/" + stream_id # replace with 'projects' after it's implemented in Specklepy
    except:
        url = serverURL + "/streams/" + stream_id
    return url 

#def removeSpecialCharacters(text: str) -> str:
#    new_text = text.replace("[","_").replace("]","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(":","_").replace("\\","_").replace("/","_").replace("\"","_").replace("&","_").replace("@","_").replace("$","_").replace("%","_").replace("^","_")
#    return new_text

