# sar-aws-daily-billing-report

## 概要
AWSの利用料金を毎日SNS Topicに通知します。  

毎日09:00 (JST)にSNS TopicにPublishされます。  
SNSにPublishする部分でAWS Lambda Destinationsを使用しています。

## SNS Topic
SNS Topicは2つ使用します。

- NotificationTopic
  - 料金の通知に使用するSNSトピック
  - `${AWS::StackName}-NotificationTopicArn`という名前でエクスポートしてます
- ErrorTopic
  - 想定外のエラーが起きた場合に通知されるSNS Topic
  - `${AWS::StackName}-ErrorTopicArn`という名前でエクスポートしてます

## NotificationTopicをサブスクライブして得られるEvent
(このEventはSNS Topicを`Email-JSON`でサブスクライブして得た内容です)
(Topicをサブスクライブする種類で少しデータは変わると思われます)

```
{
  "Type" : "Notification",
  "MessageId" : "0e6e7b52-140a-5689-90ae-2d2c88cc1f96",
  "TopicArn" : "arn:aws:sns:ap-northeast-1:355081757265:daily-billing-report-NotificationTopic-1QG2X96EZRG60",
  "Message" : "{\"version\":\"1.0\",\"timestamp\":\"2019-12-26T11:33:26.229Z\",\"requestContext\":{\"requestId\":\"b2d28b49-9f60-4194-bc44-267ecc6c2c67\",\"functionArn\":\"arn:aws:lambda:ap-northeast-1:355081757265:function:daily-billing-report-PublisherFunction-VG8J1SX17YLM:$LATEST\",\"condition\":\"Success\",\"approximateInvokeCount\":1},\"requestPayload\":{},\"responseContext\":{\"statusCode\":200,\"executedVersion\":\"$LATEST\"},\"responsePayload\":{\"daily\":{\"isSuccess\":true,\"data\":{\"start\":\"2019-12-25\",\"end\":\"2019-12-26\",\"billing\":\"0.1359202924\",\"unit\":\"USD\"}},\"monthly\":{\"isSuccess\":true,\"data\":{\"start\":\"2019-12-01\",\"end\":\"2019-12-26\",\"billing\":\"9.2169205453\",\"unit\":\"USD\"}},\"premonth\":{\"isSuccess\":true,\"data\":{\"start\":\"2019-11-01\",\"end\":\"2019-12-01\",\"billing\":\"9.6199614962\",\"unit\":\"USD\"}}}}",
  "Timestamp" : "2019-12-26T11:33:26.311Z",
  "SignatureVersion" : "1",
  "Signature" : "Y9CJFP9EeHxe0BW7VSwVUrd7Eoa3PwKdFy+bj2q7+knfhS8YYaLPuDf58wmrrh3X+ae,waifjaifwajf:awoefajefmailjfaliejliwes/aijaoifjaoiefajweoirajeazwierpqaoee/hoJ4M744ADmy+kGpq+malwfakiwemafilemafelfaksdflaw==",
  "SigningCertURL" : "https://sns.ap-northeast-1.amazonaws.com/SimpleNotificationService-awfiewafalweifajilfjalsd.pem",
  "UnsubscribeURL" : "https://sns.ap-northeast-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ap-northeast-1:355081757265:daily-billing-report-NotificationTopic-afawefae:993b662a-b4d7-4039-8616-02bc91f5f124"
}
```

このMessageの中身をJSONで解析すると次のようになっています。  
(この中身、特に`responsePayload`の中身が本当に欲しいものです)
```
{
  "version": "1.0",
  "timestamp": "2019-12-26T11:33:26.229Z",
  "requestContext": {
    "requestId": "b2d28b49-9f60-4194-bc44-267ecc6c2c67",
    "functionArn": "arn:aws:lambda:ap-northeast-1:355081757265:function:daily-billing-report-PublisherFunction-VG8J1SX17YLM:$LATEST",
    "condition": "Success",
    "approximateInvokeCount": 1
  },
  "requestPayload": {},
  "responseContext": {
    "statusCode": 200,
    "executedVersion": "$LATEST"
  },
  "responsePayload": {
    "daily": {
      "isSuccess": true,
      "data": {
        "start": "2019-12-25",
        "end": "2019-12-26",
        "billing": "0.1359202924",
        "unit": "USD"
      }
    },
    "monthly": {
      "isSuccess": true,
      "data": {
        "start": "2019-12-01",
        "end": "2019-12-26",
        "billing": "9.2169205453",
        "unit": "USD"
      }
    },
    "premonth": {
      "isSuccess": true,
      "data": {
        "start": "2019-11-01",
        "end": "2019-12-01",
        "billing": "9.6199614962",
        "unit": "USD"
      }
    }
  }
}
```

形式は次のようになります。

```
{
  "responsePayload": {
    "daily": {
      "isSuccess": True|False,
      "data": {
        "start": "string",
        "end": "string",
        "billing": "float",
        "unit": "string"
      },
      "error": {
        "message": "string",
        "stacktrace": "string"
      }
    },
    "monthly": {
      "isSuccess": True|False,
      "data": {
        "start": "string",
        "end": "string",
        "billing": "float",
        "unit": "string"
      },
      "error": {
        "message": "string",
        "stacktrace": "string"
      }
    },
    "premonth": {
      "isSuccess": True|False,
      "data": {
        "start": "string",
        "end": "string",
        "billing": "float",
        "unit": "string"
      },
      "error": {
        "message": "string",
        "stacktrace": "string"
      }
    }
  }
}
```

Message Structure
- (dict) --
  - **responsePayload** (dict) --  
    SNS TopicにPublishされた内容
    - **daily** (dict) --  
      昨日一日の利用費の情報
      - **isSuccess** (boolean) --  
        利用費の取得に成功かしたか否か
      - **data** (dict) --  
        利用費の情報
        - **start** (string) --  
          利用費を集計する期間の開始の日付(集計の際この日付を含める)。例、```2019-01-02```。
        - **end** (string) --
          利用費を集計する期間の終了の日付(集計の際この日付を含めない)。例、```2019-01-03```。
        - **billing** (string) --
          利用費。floatの数値を文字列として返す。例、```9.6199614962```。
        - **unit** (string) --
          利用費の単位。例、```USD```。
      - **error** (dict) --
        利用費取得時に発生したエラーの情報。
        - **message** (string) --
          エラーメッセージ。
        - **stacktrace** (string) --
          スタックトレース。
    - **monthly** (dict) --  
      今月分(昨日まで)の利用費の情報
      - **isSuccess** (boolean) --  
        利用費の取得に成功かしたか否か
      - **data** (dict) --  
        利用費の情報
        - **start** (string) --  
          利用費を集計する期間の開始の日付(集計の際この日付を含める)。例、```2019-01-02```。
        - **end** (string) --
          利用費を集計する期間の終了の日付(集計の際この日付を含めない)。例、```2019-01-03```。
        - **billing** (string) --
          利用費。floatの数値を文字列として返す。例、```9.6199614962```。
        - **unit** (string) --
          利用費の単位。例、```USD```。
      - **error** (dict) --
        利用費取得時に発生したエラーの情報。
        - **message** (string) --
          エラーメッセージ。
        - **stacktrace** (string) --
          スタックトレース。
    - **premonth** (dict) --  
      先月分の利用費の情報
      - **isSuccess** (boolean) --  
        利用費の取得に成功かしたか否か
      - **data** (dict) --  
        利用費の情報
        - **start** (string) --  
          利用費を集計する期間の開始の日付(集計の際この日付を含める)。例、```2019-01-02```。
        - **end** (string) --
          利用費を集計する期間の終了の日付(集計の際この日付を含めない)。例、```2019-01-03```。
        - **billing** (string) --
          利用費。floatの数値を文字列として返す。例、```9.6199614962```。
        - **unit** (string) --
          利用費の単位。例、```USD```。
      - **error** (dict) --
        利用費取得時に発生したエラーの情報。
        - **message** (string) --
          エラーメッセージ。
        - **stacktrace** (string) --
          スタックトレース。
