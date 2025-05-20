import http.client
import json

def solvedac_api(boj_id: str) -> json:
    conn = http.client.HTTPSConnection("solved.ac")

    headers = {
        'x-solvedac-language': "",
        'Accept': "application/json"
    }

    url = f"/api/v3/search/user?query={boj_id}"

    conn.request("GET", url, headers=headers)

    res = conn.getresponse()

    if res.status != 200:
        raise Exception(f"solved.ac API error: {res.status} {res.reason}")

    data = res.read()

    conn.close()

    return json.loads(data.decode("utf-8"))