import os
import sys
from functools import wraps
from typing import Callable

import boto3
import botocore

from logger.json_log_formatter import LAMBDA_REQUEST_ID_ENVIRONMENT_VALUE_NAME
from logger.my_logger import MyLogger

from ._aws_tools import prepare_get_boto3_client

logger = MyLogger(__name__)


get_ce_client = prepare_get_boto3_client("ce")


def save_information(lambda_handler) -> Callable:
    @wraps(lambda_handler)
    def _execute(event, context):
        try:
            os.environ[
                LAMBDA_REQUEST_ID_ENVIRONMENT_VALUE_NAME
            ] = context.aws_request_id
        except Exception:
            pass
        logger.info(
            "event and versions",
            event=event,
            vesions={
                "python": sys.version,
                "boto3": boto3.__version__,
                "botocore": botocore.__version__,
            },
        )
        try:
            result = lambda_handler(event, context)
            logger.info("result", result=result)
            return result
        except Exception as e:
            logger.error("lambda error", error=e)
            raise

    return _execute
