import boto3
import sys
import csv
import os
import gzip
from Bio import SeqIO


def download_file(bucket_name, key, output_path):
    session = boto3.Session(
        aws_access_key_id='A',
        aws_secret_access_key='B'
    )

    s3 = session.client('s3')

    s3.download_file(bucket_name, key, output_path)


def download_fastqs(bucket_name, prefix, sample, download_directory):
    session = boto3.Session(
        aws_access_key_id='A',
        aws_secret_access_key='B'
    )

    s3 = session.client('s3')

    # Retrieve the list of objects in the bucket with the given prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Iterate over the objects and match them with the partial names
    fastqs = []
    for obj in response['Contents']:
        key = obj['Key']
        for s in sample:
            if s in key:
                fastqs.append(key)
                # I need to pull out both forward and reverse reads
                file_name = key.split('/')[-1]
                if "R1" in file_name:
                    output_path = f'{download_directory}/{s}_R1.fastq.gz'
                elif "R2" in file_name:
                    output_path = f'{download_directory}/{s}_R2.fastq.gz'
                else:
                    continue

                download_file(bucket_name, key, output_path)

                break

    return fastqs

    bucket_name = 'x'
    prefix = 'y/'
    download_directory = 'User/wbrewer/Desktop/fastqs/raw'

    # User inputs a list of sample names in csv format as an argument after calling this script
    ifile = sys.argv[1]

    # Read partial names from CSV file
    sample = []
    with open(ifile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            sample.extend(row)

    download_fastqs(bucket_name, prefix, sample, download_directory)

# subsample using SeqIO. I am NOT waiting for millions of reads to map

def subsample_fastq(input_1, input_2, output_1, output_2, subsample_size):
    count = 0
    with gzip.open(input_1, "r") as f1, gzip.open(input_2, "r") as f2, \
         open(output_1, "w") as out1, open(output_2, "w") as out2:
        for rec1, rec2 in zip(SeqIO.parse(f1, "fastq"), SeqIO.parse(f2, "fastq")):
            count += 1
            if count > subsample_size:
                break
            rec1.id = "sub_" + rec1.id
            rec1.description = ""
            rec2.id = "sub_" + rec2.id
            rec2.description = ""
            SeqIO.write(rec1, out1, "fastq")
            SeqIO.write(rec2, out2, "fastq")

def process_directory(input_directory, output_directory, subsample_size):

    for file1 in os.listdir(input_directory):
        if file1.endswith("_R1.fastq"):
            file2 = file1.replace("_R1.fastq", "_R2.fastq")
            if file2 in os.listdir(input_directory):
                input_1 = os.path.join(input_directory, file1)
                input_2 = os.path.join(input_directory, file2)
                output_1 = os.path.join(output_directory, file1.replace(".fastq", "_sub.fastq"))
                output_2 = os.path.join(output_directory, file2.replace(".fastq", "_sub.fastq"))
                subsample_fastq(input_1, input_2, output_1, output_2, subsample_size)

if __name__ == '__main__':
    input_directory = "/User/wbrewer/Desktop/fastqs/raw/"
    output_directory = "/User/wbrewer/Desktop/fastqs/"
    subsample_size = 1000

    process_directory(input_directory, output_directory, subsample_size)


