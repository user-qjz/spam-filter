import pickle

import jieba


def chinese_word_cut(myText):
    return " ".join(jieba.cut(myText))


postingList = []
postingList2 = []

with open('chineseoutput2.txt', 'r', encoding='gbk', errors='ignore') as file:
    information = file.readline()
    while information:
        count = 0
        result_of_segment_sentence = chinese_word_cut(information)
        temp = ""
        result_of_segment_word = []
        for char in result_of_segment_sentence:
            if count <= 3:
                count += 1
                continue
            if '\u4e00' <= char <= '\u9fff':
                temp += char
            elif char == ' ' and temp != '':
                result_of_segment_word.append(temp)
                temp = ''
        postingList.append(result_of_segment_word)
        # print(result_of_segment_word)
        information = file.readline()
    print(postingList)

fp = open('data_input.pkl', 'wb')
pickle.dump(postingList, fp)
fp.close()

print("NEXT")

#with open('email_test_input.txt', 'r', encoding='gbk', errors='ignore') as file2:
with open('testset2306.txt', 'r', encoding='utf-8', errors='ignore') as file2:
    information = file2.readline()
    print(information)
    #print(information[0])
    label = []
    while information:

        count = 0
        result_of_segment_sentence = chinese_word_cut(information)
        temp = ""
        result_of_segment_word = []
        result_of_segment_word.append(information[0])
        for char in result_of_segment_sentence:
            if count <= 3:
                count += 1
                continue
            if '\u4e00' <= char <= '\u9fff':
                temp += char
            elif char == ' ' and temp != '':
                result_of_segment_word.append(temp)
                temp = ''
        postingList2.append(result_of_segment_word)
        # print(result_of_segment_word)
        information = file2.readline()
        print(information)
        #print(information[0])

fp = open('data_test.pkl', 'wb')
pickle.dump(postingList2, fp)
fp.close()
