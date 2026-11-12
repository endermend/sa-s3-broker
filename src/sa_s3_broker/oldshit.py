import os
import sys

import boto3
import requests
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from mypy_boto3_s3 import S3Client

load_dotenv(override=True)

def initialize_client() -> S3Client:
    config = Config(
        region_name='ru-central-1',
        signature_version='s3v4',
        s3={'addressing_style': 'path'}
    )
    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv('S3__ENDPOINT'),
        aws_access_key_id=f'{os.getenv('S3__TENANT_ID')}.{os.getenv('S3__ACCESS_KEY')}',
        aws_secret_access_key=os.getenv('S3__SECRET_KEY'),
        config=config,
        region_name='ru-central-1',
    )
    return s3_client

def upload_secret_report(s3_client: S3Client, bucket_name: str) -> str:
    local_file_path = 'secret_report.txt'
    s3_key = 'reports/secret_report.txt'

    with open(local_file_path, 'w') as f:
        f.write("This is secreet file.\n")

    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_key)
        print(f"[2] Файл {local_file_path} успешно загружен в {s3_key}")
    except ClientError as e:
        print(f"Ошибка загрузки: {e}")
        sys.exit(1)
    return s3_key

def check_privasy(bucket_name: str, s3_key: str) -> None:
    direct_url = f"{os.getenv('S3__GLOBAL_ENDPOINT')}/{bucket_name}/{s3_key}"

    response = requests.get(direct_url)

    print(f"[3] Прямой запрос к {direct_url}")
    print(f"    Статус: {response.status_code} {response.reason}")

def presigned_get(s3_client: S3Client, bucket_name: str, s3_key: str) -> None:
    presigned_get_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_key},
        ExpiresIn=600,
    )
    print("[4] Сгенерирован Presigned GET URL (срок жизни 600 сек)")

    get_response = requests.get(presigned_get_url)
    print(f"    Статус скачивания: {get_response.status_code} {get_response.reason}")
    print(f"    Содержимое файла: {get_response.text.strip()}")

def presigned_put(s3_client: S3Client, bucket_name: str, s3_key: str) -> None:
    presigned_put_url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name, 'Key': s3_key},
        ExpiresIn=600
    )
    print("[5] Сгенерирован Presigned PUT URL:")
    print(f"    {presigned_put_url}")
        

def main() -> None:
    print("Hello from sa-s3-broker!")

    s3_client = initialize_client()
    bucket_name = os.getenv('S3__BUCKET_NAME')
    if not bucket_name:
        print("Ошибка чтения ENV.")
        sys.exit(1)
    s3_key = upload_secret_report(s3_client, bucket_name)
    check_privasy(bucket_name, s3_key)
    presigned_get(s3_client, bucket_name, s3_key)
    presigned_put(s3_client, bucket_name, 'incoming/solution.txt')

if __name__ == "__main__":
    main()

