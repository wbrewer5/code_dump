import boto3
import sys
import csv


def download_file(bucket_name, key, output_path):
    # Create a session using your AWS credentials
    session = boto3.Session(
        aws_access_key_id='A',
        aws_secret_access_key='B'
    )

    # Create an S3 client
    s3 = session.client('s3')

    # Download the file
    s3.download_file(bucket_name, key, output_path)


def download_mapping_stats(bucket_name, prefix, sample, download_directory):
    session = boto3.Session(
        aws_access_key_id='A',
        aws_secret_access_key='B'
    )

    s3 = session.client('s3')

    # Retrieve the list of objects in the bucket with the given prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Iterate over the objects and match them with the partial names
    mapping_stats = []
    for obj in response['Contents']:
        key = obj['Key']
        for s in sample:
            if s in key:
                mapping_stats.append(key)
                # mapping stat file names suck so just rename to samplename + mapping_stats.csv
                output_path = f'{download_directory}/{s}_mapping_stats.csv'
                download_file(bucket_name, key, output_path)
                break

    return mapping_stats

    bucket_name = 'x'
    prefix = 'y/'
    download_directory = 'User/wbrewer/Desktop/mapping_stats/'

    # User inputs a list of sample names in csv format as an argument after calling this script
    ifile = sys.argv[1]

    # Read partial names from CSV file
    sample = []
    with open(ifile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            sample.extend(row)

    download_mapping_stats(bucket_name, prefix, sample, download_directory)
