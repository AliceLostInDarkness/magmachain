from quart import Quart
from quart import request, jsonify
import os

import aiohttp
from arsenic import get_session
from arsenic.browsers import Chrome
from arsenic.services import Chromedriver

app = Quart(__name__)

async def make_snapshot(website: str):
    
    service = Chromedriver(log_file=os.devnull)
    browser = Chrome(chromeOptions={ 'args': ['--headless', '--disable-gpu', '--hide-scrollbars', '--window-size=1920,1080', '--no-gpu' ] })

    async with get_session(service, browser) as session:
        await session.get(website)
        image = await session.get_screenshot()
        image.seek(0)

        async with aiohttp.ClientSession() as sess:

            headers = {
                "Authorization": "Client-ID 6656d64547a5031"
            }
            data = {
                "image": image,
            }

            async with sess.post("https://api.imgur.com/3/image", data=data, headers=headers) as r:
                link = (await r.json())["data"]["link"]

                return link

@app.route("/")
async def main():
    return "OwO, what's this? Made by F4stZ4p#3507 and chr1s#7185 with ❤"

@app.route("/v1")
async def web_screenshot():
    
    try:
        website = request.headers.get("website")
    except:
        return jsonify({
            "snapshot": "https://i.imgur.com/ZHPcdlW.jpg",
            "website": "was not specified",
            "status": request.status
            })
    
    snapshot = await make_snapshot(website)

    return jsonify({
        "snapshot": snapshot,
        "website": website,
        "status": request.status
        })

app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)
