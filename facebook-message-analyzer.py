import os
import json
import numpy as np
import pylab as pl
import datetime

CURRENT_DIRECTORY = os.getcwd()
NUMBER_TO_ANALYZE = 10000
MESSAGE_THRESHOLD = 100

def get_json_data(chat):
    try:
        json_location = CURRENT_DIRECTORY + "/messages/inbox/" + chat + "/message.json"
        with open(json_location) as json_file:
            json_data = json.load(json_file)
            return json_data
    except IOError:
        pass # some things the directory aren't messages (DS_Store, stickers_used, etc.)

chats = os.listdir(CURRENT_DIRECTORY + "/messages/inbox")[:NUMBER_TO_ANALYZE]
sorted_chats = []
final_data_messages = {}
final_data_times = {}
final_data_words = {}
final_data_sent = {}
invalid_message_count = 0

print('Analyzing ' + str(min(NUMBER_TO_ANALYZE, len(chats))) + ' chats...')

for chat in chats:
    json_data = get_json_data(chat)
    if json_data != None:
        messages = json_data["messages"]
        if len(messages) >= MESSAGE_THRESHOLD:
            sorted_chats.append((len(messages), chat, messages))

sorted_chats.sort(reverse=True)
print(sorted_chats[1])
print('Finished processing chats...')

for i, (messages, chat, messages) in enumerate(sorted_chats):
    number_messages = {}
    person_to_times = {}
    number_words = {}
    message_sent = {}

    print(str(i) + " - " + str(len(messages)) + " messages - " + str(chat))

    for message in messages:
        try:
            name = message["sender_name"]
            time = message["timestamp_ms"]
            message_content = message["content"]

            number_messages[name] = number_messages.get(name, 0)
            number_messages[name] += 1

            person_to_times[name] = person_to_times.get(name, [])
            person_to_times[name].append(datetime.datetime.fromtimestamp(time/1000.0))

            number_words[name] = number_words.get(name, [])
            number_words[name].append(len(message_content.split()))

            message_sent[name] = message_content

        except KeyError:
            # happens for special cases like users who deactivated, unfriended, blocked
            invalid_message_count += 1
    
    final_data_messages[i] = number_messages
    final_data_times[i] = person_to_times
    final_data_words[i] = number_words
    final_data_sent[i] = message_sent

print('Found ' + str(invalid_message_count) + ' invalid messages...')
print('Found ' + str(len(sorted_chats)) + ' chats with ' + str(MESSAGE_THRESHOLD) + ' messages or more')

def plot_num_messages(chat_number):
    plotted_data = final_data_messages[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Number of Messages Sent')
    pl.tight_layout()
    pl.show()

#Toba's Code Starts Here

def plot_active_times(chat_number):
    times = [0]*12
    for person in final_data_times[chat_number]:
        len_person = len(final_data_times[chat_number][person])
        for message in range(len_person):
            index = int((final_data_times[chat_number][person][message].hour - 1)/2)
            times[index] += 1
    categories = ["1-3AM","3-5AM","5-7AM","7-9AM","9-11AM","11AM-1PM","1-3PM","3-5PM","5-7PM","7-9PM","9-11PM","11PM-1AM"]
    pl.bar(categories, times)
    pl.xticks(categories)
    pl.title("Chat Activity by Time of Day")
    pl.xlabel("Time")
    pl.ylabel("Number of Texts")
    pl.show()

def get_messages_by_person(chat_number):
    mess_words = []
    sortings = sorted_chats[chat_number][2]
    print(sortings[0])
    person = input("Type a person in the chat's name: ")
    for xx in sortings:
        if xx['sender_name'] == person:
            mess_words.append(xx['content'])
    for sents in mess_words:
        print(sents)


def plot(chat_number):
    get_messages_by_person(chat_number)
    plot_active_times(chat_number)
    plot_num_messages(chat_number)

plot(1)
