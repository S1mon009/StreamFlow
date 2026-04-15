# StreamFlow - CLI Media Fetcher
![Static Badge](https://img.shields.io/badge/Python-Python?style=for-the-badge&logo=python&logoColor=%23fefefe&labelColor=%233776AB&color=%233776AB) ![Static Badge](https://img.shields.io/badge/inquirer-FastAPI?style=for-the-badge&logo=inquirer&logoColor=%23333&labelColor=%23F0DB4F&color=%23F0DB4F) 

StreamFlow CLI is a modular Python tool for fetching and streaming multimedia content directly from the terminal.

> StreamFlow is designed for educational and personal use.  
> Use only with **authorized or publicly available sources**.

---

## Features
- Stream and process media in real time
- Simple and interactive CLI interface
- Modular architecture
- Lightweight and fast

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/S1mon009/StreamFlow.git
cd streamflow
```
### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## FFmpeg Requirement
StreamFlow requires FFmpeg to process multimedia.

### Install FFmpeg
Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install ffmpeg
```
macOS (Homebrew)
```bash
brew install ffmpeg
```
Windows
Download from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Verify installation
```bash
ffmpeg -version
```

## Usage
Run the CLI tool:
```bash
python main.py
```
Follow the interactive prompts in the terminal.

## Example Use Cases
- Learning CLI application design in Python
- Personal media streaming tool
- Lightweight terminal-based media manager
