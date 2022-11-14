# latency_check RESt API
- rest api 요청 latency 측정
- 요구사항
  1. 임의의 application 의 url 호출시 latency 데이터를 전송받아 csv 형식으로 저장
  2. 임의의 application cpu(%), memory(Bytes) 사용량 전송받아 이를 저장
  3. 위 1,2 데이터는 csv 형식으로 조회 할 수 있어야 함.

## System requirements
- OS: ubuntu18.04, mac m1
- python3.10, 3.9
- requirements.txt

## 사용방법
1. git clone https://github.com/vasana12/latency_check
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. 실행 : sh latency_monitoring_start.sh

## result
- log_script/latency_check.csv
