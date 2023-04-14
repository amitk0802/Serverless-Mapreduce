from flask import escape
import json

def map_function(request):

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

    print(f"IP files : {files}")
    from google.cloud import storage
    from nltk.tokenize import word_tokenize
    import nltk
    nltk.download('punkt')

    # Checking files in the bucket
    client = storage.Client()
    bucket = client.get_bucket('amit-bucket-1')
    file_binary = bucket.list_blobs()
    final_dictionary = {}

    for filename in files:
        print(filename)
        input_file = bucket.blob(filename)
        in_download = input_file.download_as_string()
        in_file = in_download.decode("utf-8")
        file_text = in_file
        for i in range(1):
            text_tokens = word_tokenize(file_text)

        n = len(text_tokens)
        
        list_dictionary = {}
        for i in range(n):
            list_dictionary[text_tokens[i]] = list_dictionary.get(text_tokens[i], 0) + 1

        for j in list_dictionary:
            if j in final_dictionary:
                final_dictionary[j].append([list_dictionary.get(j),filename])
            else:
                final_dictionary[j] = [[list_dictionary.get(j),filename]]

    # Write files in a bucket
    client = storage.Client()
    bucket = client.get_bucket('amit-bucket-3')
    destination_blob_name = f"map_{count[0]}"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(str(final_dictionary))

        
    return 'COMPLETED'
