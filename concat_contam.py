import boto3
import sys
import csv
import os
import glob


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


def download_contam_stats(bucket_name, prefix, sample, download_directory):
    session = boto3.Session(
        aws_access_key_id='A',
        aws_secret_access_key='B'
    )

    s3 = session.client('s3')

    # Retrieve the list of objects in the bucket with the given prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Iterate over the objects and match them with the partial names
    contam_stats = []
    for obj in response['Contents']:
        key = obj['Key']
        for s in sample:
            if s in key:
                contam_stats.append(key)
                # contamination filenames only include sample name. Fine if they are all going to the contamination directory for temp use.
                output_path = f'{download_directory}/{s}'
                download_file(bucket_name, key, output_path)
                break

    return contam_stats

    bucket_name = 'x'
    prefix = 'contamination_stats/'
    download_directory = 'User/wbrewer/Desktop/contamination/'

    # User inputs a list of sample names in csv format as an argument after calling this script
    ifile = sys.argv[1]

    # Read partial names from CSV file
    sample = []
    with open(ifile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            sample.extend(row)

    download_contam_stats(bucket_name, prefix, sample, download_directory)

    # identify all CSV files
    all_contam_files = glob.glob(os.path.join("/User/wbrewer/desktop/contamination/*sample*.csv"))

    # merge all CSV files into one DataFrame
    concat_contam = pd.concat((pd.read_csv(contam) for contam in all_contam_files), ignore_index=True)
    concat_contam.to_csv("contam_stats.csv")

    # all_contam_files only includes filenames including "sample" in the name. Do not include "sample" in permanant contamination filenames.
    for individual_contam in all_contam_files:
        os.remove(individual_contam)
