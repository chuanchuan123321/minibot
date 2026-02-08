from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="minibot-ai",
    version="1.0.0",
    author="chuanchuan123321",
    author_email="2774421277@qq.com",
    description="Minibot - A lightweight AI automation tool for executing system commands, file operations, web search and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chuanchuan123321/minibot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.20.0",
        "rich>=13.0.0",
        "beautifulsoup4>=4.11.0",
        "chardet>=5.0.0",
        "lark-oapi>=1.5.0",
        "nest_asyncio>=1.5.0",
        "certifi>=2023.0.0",
        "reportlab>=4.0.0",
        "markdown>=3.4.0",
        "fpdf2>=2.7.0",
    ],
    entry_points={
        "console_scripts": [
            "minibot=chat:main",
        ],
    },
    keywords="ai automation agent task execution",
    project_urls={
        "Bug Reports": "https://github.com/chuanchuan123321/minibot/issues",
        "Source": "https://github.com/chuanchuan123321/minibot",
    },
)

