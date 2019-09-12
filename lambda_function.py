import os
import json
import urllib.request
import datetime

def lambda_handler(event, context):
    response = post_slack()
    return response

def post_slack():

    # Slackに関する設定
    SLACK_POST_URL = os.environ['SLACK']
    username = os.environ['USERNAME']
    icom = ":sunglasses:"
    channnel = os.environ['CHANNEL']
    method = "POST"

    # connpass API エンドポイント
    url = os.environ['URL']
    
    print(url)
    req = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read().decode("utf-8")
            body_json = json.loads(body)
            
            # メッセージの組み立て
            dt_now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            message = str(body_json['events'][0]['accepted']) + '人が申し込んでいます！' + ' (' + str(dt_now) + ' 現在)'
            send_data = {
                "username": username,
                "icon_emoji": icom,
                "text": message,
                "channel": channnel
            }
            send_text = ("payload=" + json.dumps(send_data)).encode('utf-8')
        
            request = urllib.request.Request(
                SLACK_POST_URL,
                data=send_text,
                method=method
            )
            with urllib.request.urlopen(request) as response:
                response_body = response.read().decode('utf-8')
    
    except urllib.error.HTTPError as e:
        if e.code >= 400:
            print(e.reason)
        else:
            raise e

    return response_body
