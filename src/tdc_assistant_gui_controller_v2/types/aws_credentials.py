from typing import TypedDict


class AWSCredentials(TypedDict):
    access_key: str
    secret_key: str
    region: str
    bucket_name: str
    object_url_domain: str
