#!/usr/bin/env python3
"""
Setup script for Healo Mental Health Chatbot
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="healo-mental-health-chatbot",
    version="1.0.0",
    author="Healo Team",
    author_email="team@healo-chatbot.com",
    description="AI-powered mental health chatbot providing empathetic and professional support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/healo-mental-health-chatbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "healo=api_server:main",
            "healo-train=advanced_model_training:main",
            "healo-test=simple_accuracy_test:main",
        ],
    },
    include_package_data=True,
    package_data={
        "healo": [
            "data/*.csv",
            "assets/css/*.css",
            "assets/js/*.js",
            "templates/*.html",
        ],
    },
    keywords=[
        "mental-health",
        "chatbot",
        "ai",
        "nlp",
        "machine-learning",
        "healthcare",
        "therapy",
        "counseling",
        "support",
        "wellness",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/healo-mental-health-chatbot/issues",
        "Source": "https://github.com/yourusername/healo-mental-health-chatbot",
        "Documentation": "https://healo-chatbot.readthedocs.io/",
        "Homepage": "https://healo-chatbot.com",
    },
)
