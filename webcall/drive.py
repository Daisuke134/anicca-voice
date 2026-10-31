import asyncio, base64, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--autoplay-policy=no-user-gesture-required","--use-fake-ui-for-media-stream"])
        pg=await b.new_page(); await pg.goto("http://127.0.0.1:8765/page.html")
        await pg.evaluate("run()")
        await pg.wait_for_function("window.DONE===true",timeout=200000)
        open("call.webm","wb").write(base64.b64decode(await pg.evaluate("window.REC")))
        print("\n".join(await pg.evaluate("LOG")))
        await b.close()
asyncio.run(main())
