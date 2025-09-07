from app.Config import ENV_PROJECT
import os
import sys
import asyncio
from asyncio.windows_events import ProactorEventLoop

from fastapi import FastAPI
from uvicorn import Config, Server

if sys.platform.startswith("win"):
    asyncio.set_event_loop(asyncio.ProactorEventLoop())


print("🔥 start.py is executing...")

if __name__ == "__main__":
    try:
        class ProactorServer(Server):
            def run(self, sockets=None):
                loop = ProactorEventLoop()
                asyncio.set_event_loop(loop) # since this is the default in Python 3.10, explicit selection can also be omitted
                asyncio.run(self.serve(sockets=sockets))
                
        port = int(os.environ.get("PORT", 8010))
        print(f"🚀 Starting server on port {port}...")
        config = Config(app="app.main:app", host="0.0.0.0", port=port, reload=False)
        server = ProactorServer(config=config)
        server.run()
        print('✅ Server Started Successfully.')

    except Exception as e:
        print(f"❌ Failed to start: {e}")
