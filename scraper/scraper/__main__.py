"""Entry point for running the scraper as a module.

Executes the scraper when invoked with 'uv run python -m scraper'.
"""

import asyncio

from scraper.main import main

if __name__ == "__main__":
    asyncio.run(main())
