from flask import escape
import json

def reduce_function(request):
    request_json = request.get_json()
    files = []
    if request.args and 'input' in request.args:
        print("In Args", request.args)
        files = request.args.getlist('input')
        count = request.args.getlist('count')
    elif request_json and 'input' in request_json:
        print("In JSON", request_json['input'])
        files = request_json['input']
        count = request_json['count']
    print(files)

    from google.cloud import storage

    # Checking files in the bucket
    client = storage.Client()
    bucket = client.get_bucket('amit-bucket-3')
    file_binary = bucket.list_blobs()
    final_dictionary = {}

    for filename in files:
        print(filename)
        input_file = bucket.blob(filename)
        in_download = input_file.download_as_string()
        in_file = in_download.decode("utf-8")
        file_text = eval(in_file)
        print(file_text)

        for j in file_text:
            if j in final_dictionary:
                for i in range(len(file_text.get(j))):
                    final_dictionary[j].append(file_text.get(j)[i])
            else:
                final_dictionary[j] = file_text.get(j)

    for key in final_dictionary:
        final_dictionary[key] = sorted(final_dictionary[key], key = lambda x:int(x[0]), reverse = True)
        
    # Write files in a bucket
    client = storage.Client()
    bucket = client.get_bucket('amit-bucket-4')
    destination_blob_name = f"reduce_{count[0]}"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(str(final_dictionary))

    print(files)
    return 'COMPLETED'