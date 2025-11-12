## 1. Fetch data from ESCO:
- Navigate to `fetch-esco` folder and run Dart code
```
cd fetch-esco
dart run
```

Three files would be created in `fetch-esco/data` folder
- `data.json` : Job data
- `knowledge.json` : Unique knowledge list from list of jobs, including essential and optional 
- `skill.json` : Unique skill list from list of jobs, including essential and optional 

## Generate knowledge extension
- Navigate to main folder
- Add an .env file, having your own Google Gen AI API key
```
GOOGLE_GENAI_API_KEY=AIz.....
```
- Install python requirements
```
pip install -r requirements.txt
```

- Run `skill_prompts.py`
- Output file have the format of `ailog_%Y-%m-%dT%H-%M-%S_{MODEL}_temp{TEMPERATURE}_thinkbudget{THINKING_BUDGET}.txt`. eg. `ailog_2025-11-11T21-39-15_gemini-2.5-flash-preview-09-2025_temp0.8_thinkbudget8192.txt`