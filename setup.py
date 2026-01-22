"""
VIZPILOT MCP Server - Setup Configuration
Package for distributing VIZPILOT MCP server to PyPI
"""
from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vizpilot-mcp",
    version="1.0.0",
    author="VizuLabs",
    author_email="support@vizulabs.com",
    description="VIZPILOT MCP Server - Access development protocols and steering rules in your IDE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vizulabs/vizpilot-mcp",
    project_urls={
        "Bug Tracker": "https://github.com/vizulabs/vizpilot-mcp/issues",
        "Documentation": "https://docs.vizpilot.com/mcp",
        "Homepage": "https://vizpilot.com",
        "Source": "https://github.com/vizulabs/vizpilot-mcp",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    keywords="mcp ide protocols development django react vue angular nodejs python javascript",
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "vizpilot-mcp=mcp_server.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
