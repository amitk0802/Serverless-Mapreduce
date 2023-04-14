from flask import escape
import json

def ui_function(request):
    request_json = request.get_json()
    files = []
    if request.args and 'input' in request.args:
        print("In Args", request.args)
        files = request.args.getlist('input')
        word = request.args.getlist('word')
    elif request_json and 'input' in request_json:
        print("In JSON", request_json['input'])
        files = request_json['input']
        word = request_json['word']
    print(files)
    from google.cloud import storage

    # Checking files in the bucket
    client = storage.Client()
    bucket = client.get_bucket('amit-bucket-4')
    file_binary = bucket.list_blobs()
    final_dictionary = {}

    for filename in files:
        print(filename)
        input_file = bucket.blob(filename)
        in_download = input_file.download_as_string()
        in_file = in_download.decode("utf-8")
        file_text = eval(in_file)
        print(file_text)
    
    word_out = file_text[word[0]]
    final_msg = ''
    for i in range(len(word_out)):
        out_count = word_out[i][0]
        out_file = word_out[i][1]
        out_msg = f'The word appears {out_count} times in {out_file} file'
        final_msg = final_msg + '\n' + out_msg
    print(word_out)
    return str(final_msg)
