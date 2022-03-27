from config import NEBULA_CONF
import os
import boto3

class MOVIE_S3:
    def __init__(self):
        #self.connect_db("nebula_development")
        config = NEBULA_CONF()
        self.download_bucket_name = "nebula-frames"
        self.s3 = boto3.client('s3', region_name='eu-central-1')
    
    def downloadDirectoryFroms3(self, arango_id):
        """
        Download a movie's directory of frames.
        @param: arango_id: movie ID including path, e.g. Movies/12345678
        @return: the number of downloaded frames
        """
        # prepare download bucket
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(self.download_bucket_name)

        # iterate download items
        keys = []
        for i, obj in enumerate(bucket.objects.filter(Prefix=arango_id)):
            if i == 0:
                continue  # first output is the directory
            keys.append(obj.key)

            if os.path.isfile(obj.key):  # frame already exists. skip download.
                continue

            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            bucket.download_file(obj.key, obj.key)  # save to same path

        return len(keys)

    def downloadFilesFroms3(self, folder_name, file_names):
        """
        Download a list of files from a folder.
        @param: folder_name: files folder path, e.g. Movies/12345678
        @param: file_names: list of file names, e.g. frame0218.jpg
        @return: the number of downloaded files
        """
        # prepare download bucket
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(self.download_bucket_name)
        # prepare set of files
        file_names_set = set()
        for fname in file_names:
            file_names_set.add(f'{folder_name}/{fname}')

        # iterate download items
        files_downloaded = []
        for i, obj in enumerate(bucket.objects.filter(Prefix=folder_name)):
            if i == 0:
                continue  # first output is the directory
            if (obj.key not in file_names_set):
                continue

            files_downloaded.append(obj.key)

            if os.path.isfile(obj.key):  # frame already exists. skip download.
                continue

            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            bucket.download_file(obj.key, obj.key)  # save to same path

        return len(files_downloaded)

    