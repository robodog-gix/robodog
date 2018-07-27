#!/usr/bin/env python3
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

test_text = 'good boy. bad dog. come here. sit! call jack. fetch! lets play! do I have any appointments? What do you see? Where am I? Do you see me? Hi mom! Call John! I feel ill, please dial mom. I am very happy. I am feeling ill. call john. dial mom. come here. fetch me a stick. come to the room. I do not feel so good'
sid = SentimentIntensityAnalyzer()
mic = sr.Recognizer()

def main():
    while True:
        capture_speech()

def capture_speech():
    with sr.Microphone() as source:
        print ("say someting")
        audio = mic.listen(source, phrase_time_limit=3)
    try:
        text = mic.recognize_google(audio)
        parsed = parse_speech(text)
        return parsed

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return []
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return []

def parse_speech(text):
    sentences = sent_tokenize(text)
    parsed = []
    for sent in sentences:
        tokens = word_tokenize(sent)
        pos_tagged = nltk.pos_tag(tokens)
        p = parse_tagged(pos_tagged)
        p['sentence'] = sent
        ss = sid.polarity_scores(sent)
        p['sentiment'] = ss['compound']
        parsed.append(p)
    return parsed
            
def detect_regex(tag_str, word_list, pattern):
    results = []
    matches = [(m.start(0), m.end(0)) for m in re.finditer(pattern, tag_str)]
    for start, end in matches:
        start_spaces = tag_str[:start].count(' ')
        end_spaces = tag_str[:end].count(' ')
        results.append(' '.join(word_list[start_spaces:end_spaces+1]))
    return results

def detect_conditions(tag_list, word_list):
    if word_list[0].lower() == 'i':
        tag_list[0] = 'PRP'
    tag_str = ' '.join(tag_list)
    pattern = 'PRP( VB(P)? RB)? VB(P|D)? ((VBN)|(JJ)|(VBG NN)|(RB(( JJ(R|S)?))*))'
    return detect_regex(tag_str, word_list, pattern)

def detect_commands(tag_list, word_list):
    actionable_verbs = ['call', 'dial', 'phone', 'come', 'fetch', 'sit', 'play']
    commands = []
    cur_command = []
    for i, word in enumerate(word_list):
        if word.lower() in actionable_verbs:
            if len(cur_command) > 0:
                commands.append(' '.join(cur_command))
            cur_command = [word]
        elif len(cur_command) > 0:
            cur_command.append(word)
            if tag_list[i] in ['NN', 'RB']:
                commands.append(' '.join(cur_command))
                cur_command = []
    
    if len(cur_command) > 0:
                commands.append(' '.join(cur_command))
    return commands

def detect_questions(tag_list, word_list):
    if len(tag_list) < 2:
        return []
    if tag_list[0] in ['WDT', 'WP', 'WP$', 'WRB', 'r'] or (word_list[0].lower() == 'do' and tag_list[1] == 'PRP'):
        return [' '.join(word_list)]
    return []

def parse_tagged(tagged):
    tag_list = [tag for word, tag in tagged if tag not in ['.', ',']]
    word_list = [word for word, tag in tagged if tag not in ['.', ',']]
    conditions = detect_conditions(tag_list, word_list)
    commands = detect_commands(tag_list, word_list)
    questions = detect_questions(tag_list, word_list)
    return {
        'conditions': conditions,
        'commands': commands,
        'questions': questions
    }

def generate_strings(text):
    sentences = sent_tokenize(text)
    parsed = []
    for sent in sentences:
        tokens = word_tokenize(sent)
        pos_tagged = nltk.pos_tag(tokens)
        tag_str = ' '.join([tag for word, tag in pos_tagged if tag not in ['.', ',']])
        word_list = [word for word, tag in pos_tagged if tag not in ['.', ',']]
        parsed.append((tag_str, word_list))
    return parsed

if __name__ == "__main__":
    # parsed = parse_speech(test_text)
    # for p in parsed:
    #     print(p)
    #print(generate_strings('i fell down. i have fallen'))
    main()