from typing import Callable

import boto3
from botocore.client import BaseClient


def prepare_get_boto3_client(service: str) -> Callable:
    client = None

    def get_aws_client() -> BaseClient:
        nonlocal client
        if client is None:
            client = boto3.client(service)
        return client

    return get_aws_client
