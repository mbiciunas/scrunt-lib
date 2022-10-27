from ..log import Log
import boto3
from .s3 import S3


class AWS:
    def __init__(self, log: Log, access_key, secret_access_key):
        self._log = log
        self._log.info("Initialize boto3 Session - aws_access_key_id: {}, aws_secret_access_key: {}".format(access_key, secret_access_key))
        self._session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
        self._log.info("Boto3 Session initialized")

        self._log.info("Create and return s3 client")
        self._s3 = S3(self._log, self._session)

    def s3(self):
        self._log.info("Return S3 client")
        return self._s3

    def sts(self):
        self._log.info("Return STS client")
        return self._session.client("sts")
