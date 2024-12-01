import asyncio

from .main import main
from .dev_main import main as dev_main

if __name__ == '__main__':
    asyncio.run(main())
