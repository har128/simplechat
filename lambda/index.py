# lambda/index.py
import json
import urllib.request

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        user_message = body.get("message", "")

        data = json.dumps({"input": user_message}).encode("utf-8")
        req = urllib.request.Request(
            "https://3140-34-48-84-241.ngrok-free.app/predict",  # あなたのColabエンドポイント
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req) as res:
            response_body = res.read().decode("utf-8")
            response_json = json.loads(response_body)
            reply = response_json["output"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": reply,
                "conversationHistory": [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": reply}
                ]
            })
        }

    except Exception as error:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
