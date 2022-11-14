#!/bin/bash
### fast api 실행하기
source venv/bin/activate
uvicorn main:app --reload --port 30000 --host 0.0.0.0