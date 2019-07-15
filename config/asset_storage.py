from storages.backends.s3boto3 import S3Boto3Storage

# S3Boto3Storage 오버라이딩
class MediaStorage(S3Boto3Storage):
    location = '' # static과 같은 버킷에 있을 때 구분하기 위해 작성한 것
    bucket_name = 'teamproject05.media.hellocoding.shop'
    region_name = 'ap-northeast-2'
    file_overwrite = False
    # custom_domain = 's3.%s.amazonaws.com/%s' % (region_name, bucket_name)
    custom_domain = bucket_name