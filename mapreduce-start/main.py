from flask import escape
import json

def start_mapreduce(request):
  if request.method == 'OPTIONS':
    # Allows GET requests from any origin with the Content-Type
    # header and caches preflight response for an 3600s
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '3600'
    }

    return ('', 204, headers)
  import requests
  from google.cloud import storage

  client_check = storage.Client()
  bucket_check = client_check.get_bucket('amit-bucket-4')
  file_binary_check = bucket_check.list_blobs()
  files_op = []
  for i in file_binary_check:
    files_op.append(i.name)
  print(files_op)

  if len(files_op) == 0:

    # Checking files in the bucket
    client = storage.Client()
    bucket = client.get_bucket('amit-bucket-1')
    file_binary = bucket.list_blobs()
    files = []
    for i in file_binary:
      files.append(i.name)

    map1_files = files[0:int(len(files)/2)]
    map2_files = files[int(len(files)/2):]

    print('MAP FUNCTION STARTING')
    print(map1_files)
    print(map2_files)

    first_map = 'NOT COMPLETED'
    second_map = 'NOT COMPLETED'

    print('First Mapper...')
    map_func = "https://us-central1-fa21-bl-engr-e516-amkasera.cloudfunctions.net/map-function"
    param1 = {"input": map1_files, "count": 1}
    first_map = requests.get(map_func, param1).text

    print('Second Mapper...')

    param2 = {"input": map2_files, "count": 2}
    second_map = requests.get(map_func, param2).text

    print('Barrier Synchronization')
    print(first_map)
    print(second_map)
    
    while True:
      if first_map == 'COMPLETED' and second_map == 'COMPLETED':
        break;
    
    print('All Files are created by Map Function')
    map_bucket = client.get_bucket('amit-bucket-3')
    map_op_files_names = map_bucket.list_blobs()
    map_op_files = []
    for j in map_op_files_names:
      map_op_files.append(j.name)
    
    print(map_op_files)
    print('REDUCE FUNCTION STARTED')
    first_reduce = 'NOT COMPLETED'

    reduce_func = "https://us-central1-fa21-bl-engr-e516-amkasera.cloudfunctions.net/reduce-function"
    reduce_param1 = {"input": map_op_files, "count": 1}
    first_reduce = requests.get(reduce_func, reduce_param1).text

    while True:
      if first_reduce == 'COMPLETED':
        break;
    
    print('REDUCE COMPLETED')

    request_json = request.get_json()
    if request_json and 'search_word' in request_json:
      word = request_json['search_word']
    else:
      print("Not found")

    print('WORD SEARCH STARTED')
    ui_bucket = client.get_bucket('amit-bucket-4')
    ui_op_files_names = ui_bucket.list_blobs()
    ui_op_files = []
    for j in ui_op_files_names:
      ui_op_files.append(j.name)

    ui_func = "https://us-central1-fa21-bl-engr-e516-amkasera.cloudfunctions.net/ui-function"
    ui_param = {"input":ui_op_files, "word":word}
    ui_search = requests.get(ui_func, ui_param).text

    print('WORD SEARCH COMPLETED')
    return str(ui_search)
  
  else:
    request_json = request.get_json()
    if request_json and 'search_word' in request_json:
      word = request_json['search_word']
    else:
      print("Not found")
    print('WORD SEARCH STARTED')
    ui_client = storage.Client()
    ui_bucket = ui_client.get_bucket('amit-bucket-4')
    ui_op_files_names = ui_bucket.list_blobs()
    ui_op_files = []
    for j in ui_op_files_names:
      ui_op_files.append(j.name)

    ui_func = "https://us-central1-fa21-bl-engr-e516-amkasera.cloudfunctions.net/ui-function"
    ui_param = {"input":ui_op_files, "word":word}
    ui_search = requests.get(ui_func, ui_param).text

    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    print('WORD SEARCH COMPLETED')
    return (json.dumps({"result": str(ui_search)}), 200, headers)