from typing import List, Dict
from fastapi import FastAPI, Body, Query, Path
from pytz import timezone

from log import logger
from model import LatencyMonitorSchema, PerformanceMonitorSchema
import pandas as pd
from src.utils import get_project_root, convert_latency_dataframe_to_list_of_dict, convert_tps_dataframe_to_list_of_dict
from datetime import datetime, timedelta

project_dir = get_project_root()
app = FastAPI(title="Latency check", description="latency check")


@app.get("/")
def home():
    return {"data": "home"}

@app.post("/performance")
def monitor_performance(patch: PerformanceMonitorSchema = Body(example=
                                                              {
                                                                  'memory': 426733568,
                                                                  'cpu': 0.0,
                                                                  'check_time': 1668682862229
                                                              })):
    """
    클라이언츠 어플리케이션 performance(cpu, memory ) 5초 주기로 측정
    :param patch:
    :return:
    """

    memory = patch.memory
    cpu = patch.cpu
    check_time = patch.check_time
    check_time = datetime.fromtimestamp(check_time/1000.0, tz=timezone("Asia/Seoul"))
    check_time = check_time.strftime("%Y-%m-%dT%H:%M:%S")
    ### 파일에 performance 데이터 저장하기
    with open(file=f"{project_dir}/log_script/performance_check.csv", mode="a+") as f:
        f.seek(0)
        text_append = f"{check_time}\t{memory}\t{cpu}"

        if f.read():
            ### 내용이 존재하면 받아온값을 추가해준다.
            f.write(f"\n{text_append}")

        else:
            ### 내용이 존재하지 않으면 칼럼을 먼저 추가하고 내용을 추가한다.
            f.write(f"check_time\tmemory\tcpu")
            f.write(f"\n{text_append}")
    return patch

@app.get("/performance")
def get_performance(check_timestamp_gte: int =Query(default=1668683106806),
                    check_timestamp_lte: int =Query(default=1668720399000)) -> List[Dict]:
    """
    저장된 performance의 시계열 조회
    :param timestamp_gte: 마지막 시간
    :param timestamp_lte: 시작 시간
    :return:
    """

    ###1. 필터링 할 날짜 타입 변환(타임스탬프 -> datetime)
    datetime_gte = datetime.fromtimestamp(check_timestamp_gte/1000.0)
    datetime_lte = datetime.fromtimestamp(check_timestamp_lte/1000.0)
    logger.debug(f"datetime_gte:{datetime_gte}/ datetime_lte:{datetime_lte}")

    ###2.  퍼포먼스 로그 데이터 읽고 pandas 이용하여 시계열 필터링
    df = pd.read_csv(f"{project_dir}/log_script/performance_check.csv", sep="\t")

    df['check_time'] = pd.to_datetime(df['check_time'], format="%Y-%m-%dT%H:%M:%S")

    df = df[(df['check_time'] >= f'{datetime_gte}') & (df['check_time'] <= f'{datetime_lte}')]


    ###3. 데이터프레임 -> List[Dict]
    data_list = []
    for idx in df.index:
        check_time = df.at[idx, "check_time"]
        memory = df.at[idx, "memory"]
        cpu = df.at[idx, "cpu"]

        #
        data = {
                "check_time": check_time,
                "memory": int(memory),
                "cpu": float(cpu)
                }
        data_list.append(data)
    return data_list
    # return {"data_list": data_list}

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
def get_latency(timestamp_gte: int, timestamp_lte: int) -> List[Dict]:
    """
    저장된 latency의 timestamp 조회
    :param timestamp_gte: 마지막 시간
    :param timestamp_lte: 시작 시간
    :return:
    """

    ###1. 필터링 할 날짜 타입 변환(타임스탬프 -> datetime)
    datetime_gte = datetime.fromtimestamp(timestamp_gte/1000.0, tz=timezone("Asia/Seoul"))
    datetime_lte = datetime.fromtimestamp(timestamp_lte/1000.0, tz=timezone("Asia/Seoul"))
    logger.debug(f"datetime_gte:{datetime_gte}/ datetime_lte:{datetime_lte}")

    ###2. latency 로그 데이터 읽고 pandas 이용하여 시계열 필터링
    df = pd.read_csv(f"{project_dir}/log_script/latency_check.csv", sep="\t")
    df['start_time_timestamp'] = pd.to_datetime(df['start_time_timestamp'], unit='ms', utc=True).map(lambda x: x.tz_convert('Asia/Seoul'))

    df = df[(df['start_time_timestamp'] > f'{datetime_gte}') & (df['start_time_timestamp'] < f'{datetime_lte}')]

    ###3. 데이터프레임 -> List[Dict]
    data_list = []
    for idx in df.index:
        start_time_timestamp = df.at[idx, "start_time_timestamp"]
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
    return data_list
    # return {"data_list": data_list}

@app.get("/tps")
def get_tps_by_timestamp(timestamp_to_be_measured: int = Query(default=1668453034507), per_unit_time_sec: int = Query(default=5)) -> Dict:
    """
    저장된 latency를 이용하여 측정 대상 시간의 tps 를 조회 ( tz : Asia/Seoul)

    param

        timestamp_to_be_measured: 측정 대상 시간(timestamp(ms))
        per_unit_time_sec: 집계 단위 구간( 단위 : 초)
    return

    """

    ###tps 는 트랜젝션의 종료시간을 기준으로 측정한다. log_script/latency_check.csv 의 데이터를 활용하여 트랜젝션 종료시간을 구한다.


    ## tps = count(time_to_be_measured - 5(지정된 구간) <= transaction_end_time <= time_to_be_measured) / 5

    ##1. latency 데이터 가져오기
    df = pd.read_csv(f"{project_dir}/log_script/latency_check.csv", sep="\t")

    ## 2. transaction_end_timestamp = start_time_timestamp + latency
    df["transaction_end_timestamp"] = df["start_time_timestamp"] + df["latency"]

    ## 3.timestamp to datetime( tz = Asia/Seoul)
    df['transaction_end_time'] = pd.to_datetime(df['transaction_end_timestamp'], unit='ms', utc=True).map(lambda x: x.tz_convert('Asia/Seoul'))

    ## 4. 집계한 시간의 구간 구하기( start_time_to_be_measured ~ end_time_to_be_measured)
    per_unit_time = timedelta(seconds=per_unit_time_sec)
    end_time_to_be_measured = datetime.fromtimestamp(timestamp_to_be_measured/1000, tz=timezone("Asia/Seoul"))
    start_time_to_be_measured = end_time_to_be_measured - per_unit_time
    logger.debug(f"단위 시간은 {per_unit_time_sec} 초 입니다. {start_time_to_be_measured} ~ {end_time_to_be_measured} 까지의 완료된 트랜젝션 수를 구합니다.")

    ## 5. transaction_end_time이 구간에 해당하는 transaction 을 구한다.
    df = df[(df['transaction_end_time'] >= f'{start_time_to_be_measured}') & (df['transaction_end_time'] < f'{end_time_to_be_measured}')]

    ## 6. 단위시간으로 나누어 1초구간에 대한 값으로 변경합니다.
    tps_per_unit_time = len(df)
    tps_per_sec = tps_per_unit_time/per_unit_time_sec
    logger.debug(f"단위시간 동안 집계된 트랜젝션 수: {tps_per_unit_time}/ 초당 트랜젝션 수: {tps_per_sec}")


    transaction_list = convert_latency_dataframe_to_list_of_dict(df)

    data = {"tps_per_sec": tps_per_sec, "per_unit_time_sec": per_unit_time_sec, "timestamp_to_be_measured": end_time_to_be_measured, "transaction_list": transaction_list}
    return data



@app.get("/tps/period")
def get_tps_by_timestamp_period(start_timestamp_to_be_measured: int = Query(default=1668453034507),
                                end_timestamp_to_be_measured: int = Query(default=1668453034507+180000),
                                per_unit_time_sec: int = Query(default=5)) -> Dict:
    """
    저장된 latency 데이터를 이용하여 측정 대상 시간의 tps 를 구간별 조회 ( tz : Asia/Seoul)

    param
        timestamp_to_be_measured: 측정 대상 시간(timestamp(ms))
        per_unit_time_sec: 집계 단위 구간( 단위 : 초)
    return

    """

    ##1. latency 데이터 가져오기
    df_latency = pd.read_csv(f"{project_dir}/log_script/latency_check.csv", sep="\t")

    ## 2. transaction_end_timestamp = start_time_timestamp + latency
    df_latency["transaction_end_timestamp"] = df_latency["start_time_timestamp"] + df_latency["latency"]
    df_latency['transaction_end_time'] = pd.to_datetime(df_latency['transaction_end_timestamp'], unit='ms', utc=True).map(lambda x: x.tz_convert('Asia/Seoul'))

    ## 3. timestamp -> datetime
    start_time_to_be_measured = datetime.fromtimestamp(int(start_timestamp_to_be_measured / 1000), tz=timezone("Asia/Seoul"))
    end_time_to_be_measured = datetime.fromtimestamp(int(end_timestamp_to_be_measured / 1000), tz=timezone("Asia/Seoul"))

    ## 4. 위에서 구한 기간을 초단위로 시계열 데이터 만들기
    range = pd.date_range(start_time_to_be_measured, end_time_to_be_measured, freq='1s')
    df = pd.DataFrame(index=range)

    ##5. 구간별로 집계(단위시간 : per_unit_time) 구간에 해당하는 latency 데이터를 집계하여 tps, latency 평균값 구하기
    for time in df.index:

        #구간의 시작 시간
        period_start = time - timedelta(seconds=per_unit_time_sec)

        #구간의 마지막 시간
        period_end = time

        #1. 구간에 해당하는 latency 데이터를 가지고 온다.
        df_latency_filterd_by_time = df_latency[(df_latency["transaction_end_time"] >= period_start) & (df_latency["transaction_end_time"] <= period_end)]

        #2. tps 를 구한다. tps는 해당 구간동안 발생한 트랜젝션을 단위시간으로 나눈 값이다.
        df.at[time, "tps"] = len(df_latency_filterd_by_time)/per_unit_time_sec

        #3. 단위 시간동안의 latency 평균값을 구한다. sum(latency)/트랜젝션 수
        df.at[time, "avg_latency"] = int(sum(df_latency_filterd_by_time["latency"])/len(df_latency_filterd_by_time)) if len(df_latency_filterd_by_time) != 0 else None

    data = convert_tps_dataframe_to_list_of_dict(df)
    return data
