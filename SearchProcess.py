import json
import os
#from datetime import time
import time
import Searcher
from SpeechToText import recognize_speech
from voice_auth import recognize, enroll, delete

audio_files = []
text_files = []
request_data_base = {}    #None
results_data_base = {}    #None
results_db_path = 'results.json'    #'Новая папка/results.json'
requests_db_path = 'requests.json'        #'Новая папка/requests.json'
results = {}    #[]#None
last_update_time = {"time": '2021-12-12 00:10:00'}    #'"2000-01-01 00:10:00"}#2000/01/01 00:10:00"}#None
last_update_time_path = 'last_update_time.json'        #tx''25.11.2021'#'01.01.2000'
to_search_in_text_files = False         #rch_in_text_files = False
to_search_in_audio_files = False
result_audio_files = []
result_text_files = []
request_of_process = ''
voice_auth_data_base = {}
voice_auth_data_base_path = 'voice_auth_data_base.json'

def find_text_files():
    global text_files#result_text_files
    #result_text_files = []
    text_files = []
    for file_name in os.listdir('.'):
        if file_name.endswith('.txt'):
            text_files.append(file_name)#result_text_files.append(file_name)

def find_audio_files():
    global audio_files#result_audio_files
    audio_files = []
    for file_name in os.listdir('.'):
        if file_name.endswith(('.wav')) or file_name.endswith('flac'):
            audio_files.append(file_name)

def find_required_files(request):
    global request_of_process, result_text_files, result_audio_files, results
    request_of_process = request
    global results, result_audio_files, result_text_files
    result_audio_files = audio_files.copy()
    results[request_of_process]= []#.
    result_text_files = text_files.copy()
    keys = request_data_base.keys()
    if request in request_data_base.keys():
        results[request] = results_data_base[request]
        file_name_position = 0
        while file_name_position < len(results[request]):#for file_name in results[request]:#:#[0]["path"]:#"[2]:#['path']:#.:
            'if not not not not '
            if not not data_check(format_data(os.path.getmtime(results[request][file_name_position]["path"])), last_update_time["time"]):    #check_data(os.path.getmtime(file_name) > last_update_time:#stat(file_name):
                results[request] = results[request][0: file_name_position] + results[request][file_name_position + 1: len(results[request])] #)# .remove(file_name_position)#del results[request][file_name]#.remove(file_name)
                file_name_position -= 1
            file_name_position += 1
    else:
        request_data_base[request] = []#''
        #return
    #''
    for file_name in results[request]:
        if to_search_in_audio_files or 1:
            #if file_name['path'] in result_audio_files:#if to_search_in_audio_files:
            for path in result_audio_files:
                if path == file_name['path']:
                    result_audio_files.remove(file_name['path'])#.remove(file_name)
        #if file_name['path'] in result_text_files:
            for path in result_text_files:
                if path == file_name['path']:
                    result_text_files.remove(file_name['path'])

def load_data_bases():
            global request_data_base, results_data_base, last_update_time, voice_auth_data_base
            check_data_bases()
            file = open(requests_db_path, 'r')
            request_data_base = json.load(file)
            file.close()
            file = open(results_db_path, 'r')
            results_data_base = json.load(file)
            file.close()
            if os.path.exists(last_update_time_path):
                file = open(last_update_time_path, 'r')
                last_update_time = json.load(file)
                file.close()
            voice_auth_data_base_file = open(voice_auth_data_base_path, 'r')#w')
            voice_auth_data_base = json.load(voice_auth_data_base_file)#s(voice_auth_data_base_file)
            voice_auth_data_base_file.close()
            find_audio_files()
            find_text_files()

def check_data_bases():
    global results_data_base, request_data_base
    if not os.path.exists(results_db_path):
        results_data_base = {}
        results_data_base_file = open(results_db_path, 'w')
        json.dump(results_data_base, results_data_base_file)
        results_data_base_file.close()
    #else:
        #results_data_base = json.load(open(results_db_path, 'r'))
    if not os.path.exists(requests_db_path):
        requests_data_base = {}
        requests_data_base_file = open(requests_db_path, 'w')
        json.dump(requests_data_base, requests_data_base_file)
        requests_data_base_file.close()
    #else:
        #requests_data_base = json.load(open(requests_db_path, 'r'))
    if not os.path.exists(last_update_time_path):
        last_update_time['time'] =last_update_time['time']
        last_time_update_file = open(last_update_time_path, 'w')
        json.dump(last_update_time, last_time_update_file)
        last_time_update_file.close()
    if not os.path.exists(voice_auth_data_base_path):
        voice_auth_data_base = {}
        voice_auth_data_base_file = open(voice_auth_data_base_path, 'w')
        json.dump(voice_auth_data_base, voice_auth_data_base_file)
        voice_auth_data_base_file.close()

def format_data(data):
    formatted_data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data))
    return formatted_data

def data_check(probably_older_data, other_data):
    if time.strptime(probably_older_data, '%Y-%m-%d %H:%M:%S') > time.strptime(other_data, '%Y-%m-%d %H:%M:%S'):
        return True
    return False

def updateAudioBase():
    #audio_files = find_audio_files()
    find_audio_files()
    for audio_file in audio_files:
        result_of_recognition = recognize(audio_file)
        if not result_of_recognition[0]: #recognize(audio_file):
            enroll(audio_file, audio_file)
            voice_auth_data_base[audio_file] = []
            voice_auth_data_base[audio_file].append(audio_file)
        else:
            voice_auth_data_base[result_of_recognition[1]].append(audio_file)
    save_data_bases()
    load_data_bases()

def remove_repeating_words():
    return

def get_text_from_file(path):
    with open(path, encoding='UTF-8') as file:#utf-8') as file:
        text = file.read()
        file.close()
        return text

def StartProcess(request, language):
    #load_data_bases()
    global results, result_audio_files
    find_required_files(request)
    if to_search_in_text_files and not to_search_in_audio_files:
        for file_path in result_text_files:
            text = get_text_from_file(file_path)
            if Searcher.first_level(request, text, file_path):
                continue
            if Searcher.second_level(request, text, file_path):
                continue
            Searcher.third_level(request, text, file_path)
    if to_search_in_audio_files or 1:
            #''''tensorflow
            if to_search_in_audio_files:
                result_recognition = recognize('request.wav')#x')
                if not result_recognition[0]:
                     pass
                 #''
                else:
                    speaker = result_recognition[1]
                    files_with_voice = voice_auth_data_base[speaker]
                    result_audio_files = set(result_audio_files) & set(files_with_voice)#voice_auth_data_base)#'''
            for file_path in result_audio_files:
                '''if to_search_in_audio_files:# _audio_files:
                    speaker = recognize('request.wav')#enroll
                    if !speaker[]:'''

                '''if to_search_in_audio_files and not (recognize(file_path)[1] == recognize('request.wav')[1]):905
                6
                    continue'''
                text = recognize_speech(file_path, language)#get_text_from_file(file_path)
                if Searcher.first_level(request, text, file_path):
                    continue
                if Searcher.second_level(request, text, file_path):
                    continue
                Searcher.third_level(request, text, file_path)
    delete('request.wav')
    parse_result()#result[request].append(Searcher.RESULTS)
    save_data_bases()
    load_data_bases()

def initialize_process(search_in_text, search_in_audio):
    global to_search_in_text_files, to_search_in_audio_files
    to_search_in_text_files = search_in_text
    to_search_in_audio_files = search_in_audio

def parse_result():
    global results
    for result in Searcher.RESULTS:
        #results[request_of_process] = []
        results[request_of_process].append({"request": result.request, "path": result.path, \
                                            "priority": result.priority, "coordinates": result.coordinates})
    results_data_base[request_of_process] = results[request_of_process]
    Searcher.RESULTS = []

def save_data_bases():
    file = open(results_db_path, 'w')
    json.dump(results_data_base, file)
    file.close()
    file = open(requests_db_path, 'w')
    json.dump(request_data_base, file)
    file.close()
    file = open(voice_auth_data_base_path, 'w')
    json.dump(voice_auth_data_base, file)
    file.close()