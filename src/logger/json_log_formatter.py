import json
import logging
import os
from decimal import Decimal

LAMBDA_REQUEST_ID_ENVIRONMENT_VALUE_NAME = "LAMBDA_REQUEST_ID"


def default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if int(obj) == obj else float(obj)
    try:
        return str(obj)
    except Exception:
        return None


class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        result = {
            "lambda_request_id": os.environ.get(
                LAMBDA_REQUEST_ID_ENVIRONMENT_VALUE_NAME
            )
        }

        for attr, value in record.__dict__.items():
            if attr == "asctime":
                value = self.formatTime(record)
            if attr == "exc_info" and value is not None:
                value = self.formatException(value)
                if isinstance(value, str):
                    value = value.split("\n")
            if attr == "stack_info" and value is not None:
                value = self.formatStack(value)
            if attr == "msg":
                try:
                    value = record.getMessage()
                except Exception:
                    pass

            result[attr] = value
        return json.dumps(result, default=default)
