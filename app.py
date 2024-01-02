from flask import Flask
import boto3
from botocore.exceptions import NoCredentialsError
from concurrent.futures import ThreadPoolExecutor
import logging
import time

cloudwatch_log = boto3.client("logs", 
                              region_name="us-east-1",
                              aws_access_key_id="AKIAV6E5X54W6BFMYWBF",
                              aws_secret_access_key="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"
                              )

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

executer = ThreadPoolExecutor(max_workers=5)

def __log_to_cloudwatch(message, log_group_name, log_stream_name):
    try:
        cloudwatch_log.put_log_events(
            logGroupName= log_group_name, 
            logStreamName = log_stream_name,
            logEvents=[
                {
                    'timestamp': int(round(time.time()*1000)),
                    'message': message
                }
            ]
        )
    except Exception as ex:
        print(ex)


def log_message(message):
    log_group_name = "youtube_demo_1"
    log_stream_name = "demo"
    future = executer.submit(__log_to_cloudwatch, message, log_group_name, log_stream_name)
    future.add_done_callback(handle_log_result)
    
def handle_log_result(future):
    print("Excecution completed")
    result = future.done()
    print(f"completed status : {result}")
    
    
app = Flask(__name__)

@app.route("/")
def index():
    log_message("This is my test message!!!")
    return "hello world!!"

if __name__ == "__main__":
    app.run()