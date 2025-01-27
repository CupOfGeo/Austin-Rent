from setuptools import setup, find_packages

setup(
    name="notification",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "structlog>=24.1.0",
        "gunicorn>=21.2.0",
        "structlog-gcp>=0.1.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "responses>=0.24.1",
        ],
    },
)
