from tornado.httpclient import AsyncHTTPClient

endpoint = "https://catfact.ninja"

async def get_cat_fact():
    http_client = AsyncHTTPClient()
    try:
        response = await http_client.fetch(f"{endpoint}/fact")
    except Exception as e:
        print("Error: %s" % e)
    else:
        return response.body