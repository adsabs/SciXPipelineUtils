import logging

import io
import boto3
from botocore.exceptions import ClientError, ParamValidationError


class S3Provider:
    """
    Class for interacting with a particular S3 provider
    """

    def __init__(self, provider, config):
        """
        input:

        provider: The name of the S3 provider
        config: The imported Pipeline configuration
        """
        if provider == "AWS":
            self.s3 = boto3.resource("s3")
            self.bucket = self.s3.Bucket(config.get("AWS_BUCKET_NAME"))
        else:
            self.s3 = boto3.resource(
                "s3",
                endpoint_url=config.get(str(provider) + "_S3_URL"),
                aws_access_key_id=config.get(str(provider) + "_ACCESS_KEY_ID"),
                aws_secret_access_key=config.get(str(provider) + "_SECRET_ACCESS_KEY"),
                aws_session_token=None,
            )
            self.bucket = self.s3.Bucket(config.get(str(provider) + "_BUCKET_NAME"))

    def write_object_s3(self, file_bytes, object_name):
        try:
            response = self.bucket.put_object(Body=file_bytes, Key=object_name)
            logging.info(response)
        except (ClientError, ParamValidationError) as e:
            logging.exception(e)
            raise e
        return response.e_tag

    def read_object_s3(self, object_name):
        try:
            with io.BytesIO() as s3_obj:
                self.bucket.download_fileobj(object_name, s3_obj)
                s3_obj.seek(0)
                s3_file = s3_obj.read().decode('UTF-8')
        except (ClientError, ParamValidationError) as e:
            logging.exception(e)
            raise e
        return s3_file


def load_s3_providers(config):
    """
    Loops over all providers specified in config and returns them as a dict

    input:

    config: The imported Pipeline configuration

    return:

    provider_dict: a dictionary with entries of the form "PROVIDER_NAME": class s3_provider
    """
    provider_dict = {}
    for provider in config.get("S3_PROVIDERS", ["AWS"]):
        provider_dict[provider] = S3Provider(provider, config)
    return provider_dict
