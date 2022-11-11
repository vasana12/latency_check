from fastapi import FastAPI, Request, Response, Body
from log import logger
from model import LatencyMonitorSchema
import pandas as pd
from src.utils import get_project_root
from datetime import datetime
import os
import csv

project_dir = get_project_root()
app = FastAPI(title="Latency check", description="latency check")


@app.get("/")
def home():
    return {"data": "home"}

@app.post("/latency")
def monitor_latency(patch: LatencyMonitorSchema = Body(example=
                                                       {
                                                           'start_time_timestamp': 1668135781887,
                                                           'method': 'GET',
                                                           'url': 'http://127.0.0.1:8000/insight/influencer?hashtag=%EB%A7%81%EB%B8%94%EC%B2%B4%ED%97%98%EB%8B%A8&limit=10&max_follower=1000&min_follower=0',
                                                           'status_code': 200,
                                                           'latency': 126
                                                       })):
    """
    클라이언츠 어플리케이션 url 호출시 실시간 latency check
    :param patch:
    :return:
    """

    start_time_timestamp = patch.start_time_timestamp
    method = patch.method
    url = patch.url
    status_code = patch.status_code
    latency = patch.latency


   ### 파일에 latency 저장하기
    with open(file=f"{project_dir}/log_script/latency_check.csv", mode="a+") as f:
        f.seek(0)
        text_append = f"{start_time_timestamp}\t{method}\t{url}\t{status_code}\t{latency}"
        if f.read():
            ### 내용이 존재하면 받아온값을 추가해준다.
            f.write(f"\n{text_append}")

        else:
            ### 내용이 존재하지 않으면 칼럼을 먼저 추가하고 내용을 추가한다.
            f.write(f"start_time_timestamp\tmethod\turl\tstatus_code\tlatency")
            f.write(f"\n{ text_append}")

    return patch

@app.get("/latency")
def get_latency(timestamp_gte: int, timestamp_lte:int):
    """
    저장된 latency의 timestamp 조회
    :param timestamp_gte: 마지막 시간
    :param timestamp_lte: 시작 시간
    :return:
    """
    datetime_gte = datetime.fromtimestamp(timestamp_gte/1000.0)
    datetime_lte = datetime.fromtimestamp(timestamp_lte/1000.0)

    df = pd.read_csv(f"{project_dir}/log_script/latency_check.csv",sep="\t")
    df['start_time_timestamp'] = pd.to_datetime(df['start_time_timestamp'], unit='ms')
    df = df[(df['start_time_timestamp'] > f'{datetime_gte}') & (df['start_time_timestamp'] < f'{datetime_lte}')]

    data_list = []
    for idx in df.index:
        start_time_timestamp = df.at[idx, "start_time_timestamp"]
        print(start_time_timestamp)
        method = df.at[idx, "method"]
        url = df.at[idx, "url"]
        status_code = int(df.at[idx, "status_code"])
        latency = int(df.at[idx, "latency"])
        #
        data = {
                "start_time_timestamp": start_time_timestamp,
                "method":method,
                "url":url,
                "status_code":status_code,
                "latency":latency
                }
        data_list.append(data)
    print(data_list)
    return data_list
    # return {"data_list": data_list}
