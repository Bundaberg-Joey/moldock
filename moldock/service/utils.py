import os
from uuid import uuid4

import boto3

from moldock.utils import execute_cli_command


def launch_metaflow_workflow(metaflow_cli_command):
    metaflow_cli_command = metaflow_cli_command.rstrip()  # remove any trailing space

    if " run " not in metaflow_cli_command and " run" not in metaflow_cli_command:
        raise ValueError("Command must include the `run` flag.")

    tmp_name = f"tmp_{uuid4()}.txt"
    execute_cli_command(metaflow_cli_command + f" --run-id-file {tmp_name}")
    run_id = open(tmp_name, "r").read()
    os.remove(tmp_name)
    return run_id


def parse_s3_uri(s3_uri):
    chunks = s3_uri.replace("s3://", "").split("/")
    bucket_name = chunks[0]
    object_name = "/".join(chunks[1:])
    file_name = chunks[-1]
    return bucket_name, object_name, file_name


def download_s3_uri(s3_uri):
    bucket_name, object_name, file_name = parse_s3_uri(s3_uri=s3_uri)
    s3_client = boto3.client("s3")
    s3_client.download_file(bucket_name, object_name, file_name)
    return file_name


def upload_s3_uri(s3_uri):
    bucket_name, object_name, file_name = parse_s3_uri(s3_uri=s3_uri)
    s3_client = boto3.client("s3")
    s3_client.upload_file(file_name, bucket_name, object_name)
