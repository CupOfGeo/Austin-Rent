import asyncio
import threading
import time

from scraper.main import main
from scraper.utils.simple_webserver import run_simple_webserver, stop_webserver

if __name__ == "__main__":
    # a webserver is needed for deploying to cloud run.
    stop_event = threading.Event()
    webserver_thread = threading.Thread(target=run_simple_webserver, args=(stop_event,))
    webserver_thread.start()

    asyncio.run(main())

    # Sleep a little to keep the application running for health check
    time.sleep(30)
    stop_webserver(stop_event)
    webserver_thread.join()
