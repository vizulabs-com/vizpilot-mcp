"""
VIZPILOT MCP Setup
"""
from setuptools import setup, find_packages

setup(
    name="vizpilot-mcp",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'vizpilot-mcp=vizpilot_mcp.server:main',
        ],
    },
    python_requires='>=3.8',
)
