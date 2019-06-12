


def trace(func):
    def request_wrapper(*args, **kwargs):
        resp = func()
        print("Request: {} | Status Code: {} | Response Body: {}".format(resp.url, resp.status_code, resp.text))
        return resp
    return request_wrapper

@trace
def get_posts(l):
    resp = l.client.get("/posts")
    return resp

@trace
def get_post(l, id=1):
    resp = l.client.get("/posts/{}".format(id))
    return resp

def create_post(l, payload):
    resp = l.client.post("/posts", payload)
    print("Request: {} | Status Code: {} | Response Body: {}".format(resp.url, resp.status_code, resp.text))
    # print("Response status code:", resp.status_code)
    # print("Response content:", resp.text)
    # print("Response:", resp.content)
    # print(resp.cookies)
    # print(resp.encoding)
    # print(resp.headers)  # Returns headers json: {'Via': '1.1 linkerd, 1.1 linkerd', 'Content-Encoding': 'gzip',
    # 'Date': 'Fri, 31 May 2019 14:12:00 GMT', 'Server': 'Kestrel', 'Content-Length': '227', 'Content-Type':
    # 'application/json; charset=utf-8'}
    # print(resp.json)
    # print(resp.ok)  # Should be True
    # print(resp.url)
    return resp

def update_post(l, payload={"id": 1, "title": "foo", "body": "bar", "userId": 1}):
    resp = l.client.post("/posts", payload)
    print("Request: {} | Status Code: {} | Response Body: {}".format(resp.url, resp.status_code, resp.text))
    return resp

def patch_post(l, id, payload):
    resp = l.client.patch("/posts/{}".format(id), payload)
    print("Request: {} | Status Code: {} | Response Body: {}".format(resp.url, resp.status_code, resp.text))
    return resp

def delete_post(l, id=1):
    resp = l.client.delete("/posts/{}".format(id))
    print("Request: {} | Status Code: {} | Response Body: {}".format(resp.url, resp.status_code, resp.text))
    return resp

def get_post_comments(l, post_id):
    resp = l.client.get("/posts/{}/comments".format(post_id))
    print("Request: {} | Status Code: {} | Response Body: {}".format(resp.url, resp.status_code, resp.text))
    return resp