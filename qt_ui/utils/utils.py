from textwrap import wrap
from typing import Union
import requests

SYMBOL = "_x_x_"


def splitTextIntoLines(text: str = "", number: int = 40) -> str:
    msg = ""
    try:
        if len(text) > number:
            try:
                for i, text_part in enumerate(text.split("\n")):
                    lines = wrap(text_part, number)
                    for k, x in enumerate(lines):
                        msg += x
                        if k != len(lines) - 1:
                            msg += "\n"
                    if i != len(text.split("\n")) - 1:
                        msg += "\n"
            except Exception as e:
                print(e)
        else:
            msg = text
    except Exception as e:
        print(e)
        print(text)
    return msg


def constructCommitURL(
    streamWrapper,
    branch_id: Union[str, None] = None,
    commit_id: Union[str, None] = None,
) -> Union[str, None]:
    import requests

    try:
        if isinstance(streamWrapper, tuple) or isinstance(streamWrapper, list):
            streamWrapper = streamWrapper[0]
        streamUrl = streamWrapper.stream_url.split("?")[0].split("&")[0].split("@")[0]
        r = requests.get(streamUrl)

        url = streamUrl
        # check for frontend2
        try:
            header = r.headers["x-speckle-frontend-2"]  # will throw Exception in FE1
            url = (
                streamUrl.replace("streams", "projects")
                + "/models/"
                + branch_id
                + "@"
                + commit_id
            )
        except:
            url = streamUrl.replace("projects", "streams") + "/commits/" + commit_id
        return url
    except:
        return None


def constructCommitURLfromServerCommit(serverURL: str, stream_id: str) -> str:
    r = requests.get(serverURL)

    # check for frontend2
    # only check the url string
    try:
        header = r.headers["x-speckle-frontend-2"]
        url = (
            serverURL
            + "/projects/"
            + stream_id  # + "/models/" + branch_id + "@" + commit_id
        )
    except KeyError:
        url = serverURL + "/streams/" + stream_id
    return url
