import os

import tinys3

def collect_paths(source_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)
            target_path = os.path.relpath(source_path, source_dir)
            yield (source_path, target_path)

def get_current_paths(s3):
    for entry in s3.list(''):
        yield entry.get('key')

def delete_paths(s3, paths):
    for path in paths:
        s3.delete(path)

def upload_paths(s3, paths):
    for source, target in paths:
        with open(source, 'rb') as f:
            s3.upload(target, f)


if __name__ == '__main__':
    s3 = tinys3.Connection(
        os.environ['S3_KEY'],
        os.environ['S3_SECRET'],
        tls=True,
        default_bucket=os.environ['S3_BUCKET'],
        endpoint=os.environ['S3_REGION']
    )
    present_paths = get_current_paths(s3)
    delete_paths(s3, present_paths)
    future_paths = collect_paths('output')
    upload_paths(s3, future_paths)
