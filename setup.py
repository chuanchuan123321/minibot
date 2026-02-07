from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Minibot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Minibot - 一个轻量级的 AI 自动化工具，可以执行系统命令、文件操作、网页搜索等任务",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Minibot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.20.0",
        "rich>=13.0.0",
        "beautifulsoup4>=4.11.0",
    ],
    entry_points={
        "console_scripts": [
            "minibot=chat:main",
        ],
    },
)
