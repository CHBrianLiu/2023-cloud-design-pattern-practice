import os

LOCAL = os.environ.get("LOCAL", "0").lower() in ("true", "1", "yes")

AZ_STORAGE_ACCOUNT_CONNECTION_STRING = os.environ.get("AZ_STORAGE_ACCOUNT_CONNECTION_STRING", "")
AZ_DEV_STORAGE_ACCOUNT_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;"
AZ_STORAGE_ACCOUNT_NAME = "brianasyncreqreply"
AZ_STORAGE_QUEUE_NAME = "picturegeneration"
AZ_STORAGE_BLOB_CONTAINER_NAME = "picturegeneration"
