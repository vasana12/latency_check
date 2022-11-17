from pathlib import Path
import math

import numpy


def get_project_root() -> Path:
    return Path(__file__).parent.parent

def convert_latency_dataframe_to_list_of_dict(df):
    data_list = []
    for idx in df.index:

        start_time_timestamp = int(df.at[idx, "start_time_timestamp"])
        transaction_end_timestamp = int(df.at[idx, "transaction_end_timestamp"])
        method = df.at[idx, "method"]
        url = df.at[idx, "url"]
        status_code = int(df.at[idx, "status_code"])
        latency = int(df.at[idx, "latency"])
        #
        data = {
            "start_time_timestamp": start_time_timestamp,
            "transaction_end_timestamp": transaction_end_timestamp,
            "method": method,
            "url": url,
            "status_code": status_code,
            "latency": latency
        }
        data_list.append(data)
    return data_list

def isNaN(num):
    return num != num

def convert_tps_dataframe_to_list_of_dict(df):
    data_list = []
    for idx in df.index:
        tps = int(df.at[idx, "tps"])
        avg_latency = df.at[idx, "avg_latency"] if not numpy.isnan(df.at[idx, "avg_latency"]) else None
        data = {
            "time": idx,
            "tps": tps,
            "avg_latency": avg_latency
        }
        data_list.append(data)
    return data_list