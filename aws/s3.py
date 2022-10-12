from log import Log
import boto3


class S3:
    def __init__(self, log: Log, session: boto3.Session):
        self._log = log
        self._s3 = session.client("s3")
        self._log.info("Boto3 S3 initialized")

    # def s3(self):
    #     return self._s3

    def waiter_names(self):
        return self._s3.waiter_names

        # return self._s3.
