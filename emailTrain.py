import pickle
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

# train_data = pd.read_csv('chineseoutput.txt', sep='\t', names=['label', 'content'], encoding='gbk').astype(str)
train_data = pd.read_csv('chineseoutput2.txt', sep='\t', names=['label', 'content'], encoding='gbk').astype(str)
# test_data = pd.read_csv('email_test_input.txt', sep='\t', names=['content'], encoding='gbk').astype(str)
test_data = pd.read_csv('testset2306.txt', sep='\t', names=['content'], encoding='utf-8').astype(str)

train_data.info()


def read_category(y_train):
    categories = ['0', '1']
    categories = [x for x in categories]
    cat_to_id = dict(zip(categories, range(len(categories))))
    label_id = []
    for i in range(len(y_train)):
        label_id.append(cat_to_id[y_train[i]])
    return label_id


train_target = train_data['label']
y_label = read_category(train_target)


def chinese_word_cut(myText):
    return " ".join(jieba.cut(myText))


train_content = train_data['content'].apply(chinese_word_cut)
test_content = test_data['content'].apply(chinese_word_cut)

f_all = pd.concat(objs=[train_data['content'], test_data['content']], axis=0)
tfidf_vect = TfidfVectorizer(max_df=0.5, min_df=1, token_pattern=r"(?u)\b\w+\b")
tfidf_vect.fit(f_all)
X_train = tfidf_vect.fit_transform(train_data['content'])
X_test = tfidf_vect.fit_transform(test_data['content'])

data = (X_train, y_label, X_test)
fp = open('data_tfidf.pkl', 'wb')
pickle.dump(data, fp)
fp.close()
