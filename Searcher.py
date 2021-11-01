def match(textForMatching, text):
    if textForMatching == text:
        print('match')
        return True
    return False

class Result:
    request = ''
    path = ''
    priority = 0
    coordinates = ''
    def __init__(self, request, path, priority, coordinates):
        self.request = request
        self.path = path
        self.priority = priority
        self.coordinates = coordinates

RESULTS = []
REQUIRE_PERCENT_OF_MATCHING = 60

def match_particullary(word, otherWord):
    shortWord = otherWord
    longWord = word
    count_of_matched = 0
    if len(word) < len(otherWord):
        global shortWord, longWord
        shortWord = word
        longWord = otherWord
    '''else:
        shortWord = otherWord'''
    for i in range(0, len(longWord)):
        if longWord[i] == shortWord[0]:
            j = i
            part_count = 0
            while longWord[j] == shortWord[j] and part_count < len(shortWord):
                part_count += 1
                j += 1
            global count_of_matched
            if part_count > count_of_matched:
                count_of_matched = part_count
    return count_of_matched

def first_level(request, text, path):
    for i in range(0, len(text)):
        if match(text[i: i + len(request)], request):
            RESULTS.append((Result(request=request, path=path, priority=0, coordinates=str(i))))

def second_level(request, text, path):
    words_of_request = request.split(' ')
    position_of_first_found = -1
    first_found = False
    count_of_found_words = 0
    for word in text.split(' '):
        if not first_found:
            position_of_first_found += 1
        for request_word in words_of_request:
            if match_particullary(word, request_word) >= REQUIRE_PERCENT_OF_MATCHING:
                count_of_found_words += 1
                break#continue
    return

