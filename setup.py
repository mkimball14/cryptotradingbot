from setuptools import setup, find_packages

setup(
    name="crypto_trading_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "websockets",
        "python-dotenv",
        "pyjwt[crypto]",
        "numpy>=1.24.0"
    ],
    python_requires=">=3.7",
) 