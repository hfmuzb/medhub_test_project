from service.parsers import parse_full_s3_path


def test_s3_full_path_parser():
    s3_paths_to_test = [
        ('s3://bucket-name/object', ('bucket-name', 'object')),
        ('s3://bucket/some/path/to/object', ('bucket', 'some/path/to/object'))
    ]
    for path in s3_paths_to_test:
        assert parse_full_s3_path(path[0]) == path[1]
