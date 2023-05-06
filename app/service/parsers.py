def parse_full_s3_path(full_s3_path: str) -> (str, str):
    """
    Parse full s3 path of the object, and return bucket and s3 keys.
    :param full_s3_path: str, in the format s3://<bucket_name>/s3_key
    :return: bucket_name: str, s3_key: str
    """
    path_to_object: str = full_s3_path.split(sep='//', maxsplit=1)[1]
    bucket_name, s3_key = path_to_object.split(sep='/', maxsplit=1)
    return bucket_name, s3_key
