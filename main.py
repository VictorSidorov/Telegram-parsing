from data import *
from telethon.sync import TelegramClient
from telethon import functions
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

KeywordFlag = str(input("Do you want to enter keywords yourself? n/y: "))
if KeywordFlag == 'n':                                  
    keyword = input("Enter the keyword: ")
    keyword_parsed = morph.parse(keyword)
    forms = set()
    for parsed_word in keyword_parsed:
        for case in ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']:
            form = parsed_word.inflect({case}).word
            if form:
                forms.add(form)
    print(forms)
if KeywordFlag == 'y':
    words = input("Enter the keywords: ")
    forms = set(words.split())
    print(forms)
    

select = str(input("create a new file? n/y: "))
if select== 'n':
    fileName = "results"
    f = open('results.txt', 'w')
    f.close()
if select== 'y':
    fileName = input("Enter the name of the file to save: ")

limit = 300

with TelegramClient(phone, api_id, api_hash, system_version="4.16.30-vxCUSTOM") as client:
    cur_id = 0
    count = 0
    while True:
        result = client(functions.messages.GetHistoryRequest(
            peer=name_account, offset_id=cur_id, offset_date=0,
            add_offset=0, limit=limit, max_id=0, min_id=0, hash=0,
        ))
        result = result.messages
        if not result:
            break

        for message in result:
            try:
                message_text = message.message.lower()
                for form in forms:
                    if form in message_text:
                        count += 1
                        print(f"{count}-------------------------\n\n{message.message}\n\n-----------------------")
                        with open(str(fileName)+'.txt', 'a', encoding='utf-8') as f:
                            f.write(f"{str(count)}\n Time:{str(message.date)}\n Message: {message.message}\n\n")
            except AttributeError:
                pass
        cur_id = result[-1].id
