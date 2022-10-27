from botocore.exceptions import ClientError
from ..log import Log
import boto3


class S3:
    def __init__(self, log: Log, session: boto3.Session):
        self._log = log
        self._s3 = session.client("s3")
        self._log.info("Boto3 S3 initialized")

    # def s3(self):
    #     return self._s3

    def list_buckets(self) -> list:
        self._log.info("Make call to S3.list_buckets")
        try:
            return self._s3.list_buckets()
        except ClientError as error:
            self._log.error("Client error executing list_buckets: {}".format(error), True)

    def waiter_names(self) -> list:
        self._log.info("Make call to S3.waiter_names")
        return self._s3.waiter_names
