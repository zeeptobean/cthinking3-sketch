# Computational Thinking mid-term project: careersearch

your skills - your path - from learning to earning

## Members
#### Group name: Lorem_Ipsum
- 24127003 - Vũ Trần Minh Hiếu
- 24127240 - Hoàng Đức Thịnh
- 24127270 - Trần Viết Bảo
- 24127326 - Đoàn Quốc Bảo

## Tech stack
- Dart: Fetch data
- Python: Main logic & GUI using Flet

## Prerequisites
- Dart 3.9.2 or later (optional, for fetching data)
- Python 3.13 or later

## Run instruction

### 0. Prepare data (optional):
#### Fetch data directly from ESCO
- Navigate to `fetch-esco` folder and run Dart code
```
cd fetch-esco
dart run
```

Three files would be created in `fetch-esco/data` folder
- `data.json` : Job data
- `knowledge.json` : Unique knowledge list from list of jobs, including essential and optional 
- `skill.json` : Unique skill list from list of jobs, including essential and optional 

#### Copy these three files to `assets` folder
- `fetch-esco/data/data.json` -> `assets/job.json`
- `fetch-esco/data/knowledge.json` -> `assets/knowledge.json`
- `fetch-esco/data/skill.json` -> `assets/skill.json`

#### Prepare knowledge detail
- Set up .env file at base directory
```
GOOGLE_GENAI_API_KEY=AIza...
```
- Run `python3 knowledge_prompt.py`

### 1. Run
#### 1a. Run manually
- Create a virtual Python enviroment
- If are on a Linux system, and do not want to install GPU version of pytorch, run `pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu`, then run `pip install -r requirements-docker.txt`
- If otherwise, or you are using Windows or MacOS, run `pip install -r requirements.txt`
- Run `python src/gui.py`. If you are on a headless-server then Flet will run as a webserver, otherwise it will run as an desktop app
- Or run `flet run --web src/gui.py` to run the app as Flet Webapp. The webpage will autostart after a while of initialization
#### 1b. Run with Docker
- `docker build -t <your-tag-name> .`
- `docker run -d <your-tag-name>`

The webapp is now uprunning and can be access through port 8000