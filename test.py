import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import tkinter as tk
from tkinter import ttk, Listbox, Scrollbar, messagebox
# 读取训练数据
with open('data_tfidf.pkl', 'rb') as fp:
    loaded_data = pickle.load(fp)
X_train, y_label, X_test = loaded_data

# 读取训练集
with open('data_input.pkl', 'rb') as train:
    List = pickle.load(train)

# 读取测试集
with open('data_test.pkl', 'rb') as test:
    testList = pickle.load(test)


def loadDataSet():
    return List, y_label


def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


# 计算条件概率和先验概率
def trainNB(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    numClasses = max(trainCategory) + 1  # 多类别问题

    pNum = [np.ones(numWords) for _ in range(numClasses)]
    pDenom = [2.0 * np.ones(numWords) for _ in range(numClasses)]
    pPrior = [0.0] * numClasses

    for i in range(numTrainDocs):
        category = trainCategory[i - 1]
        pPrior[category] += 1
        pNum[category] += trainMatrix[i - 1]
        pDenom[category] += sum(trainMatrix[i - 1])

    totalSamples = sum(pPrior)
    pPrior = [count / totalSamples for count in pPrior]

    pVect = [np.log((pNum[i] + 1) / (pDenom[i] + numWords)) for i in range(numClasses)]

    return pVect, pPrior


# 多类别分类
def classifyNB(vec2Classify, pVect, pPrior):
    p = np.dot(vec2Classify, pVect.T) + np.log(pPrior)
    return np.argmax(p)


def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []

    for postinDoc in listOPosts:
        trainMat.append(bagOfWords2VecMN(myVocabList, postinDoc))

    pVect, pPrior = trainNB(np.array(trainMat), np.array(listClasses))
    fOpen = open("testResult.txt", 'w')
    y_pred = []
    y_true = []
    for testEntry in testList:
        result = classifyNB(bagOfWords2VecMN(myVocabList, testEntry), np.array(pVect).reshape(2, -1), pPrior)
        categories = ['0', '1']
        fOpen.write(list_to_string(categories[result]) + ' ' + list_to_string(testEntry) + '\n')
        y_pred.append(result)
        # print(testEntry)
        y_true.append(eval(testEntry[0]))

    # print(y_pred)
    # print(y_true)
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    print('Accuracy: %.2f%%' % (accuracy * 100))
    print('precision: %.2f%%' % (precision * 100))
    print('recall: %.2f%%' % (recall * 100))
    print('f1: %.2f%%' % (f1 * 100))
    print(cm)


def list_to_string(input_list):
    return ''.join(map(str, input_list))


def bagOfWords2VecMN(vocabSet, inputSet):
    returnDict = {}
    for word in inputSet:
        if word in vocabSet:
            returnDict.setdefault(word, 0)
            returnDict[word] += 1
    returnVec = [returnDict.get(word, 0) for word in vocabSet]
    # print(1)
    return returnVec


# testingNB()
# 图形界面

class SpamFilterApp:
    def __init__(self, master):
        self.result_listbox = None
        self.master = master
        master.title("垃圾邮件过滤")

        # 获取屏幕宽度和高度
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # 计算窗口位置
        self.x_position = (screen_width - 500) // 2  # 500 是窗口宽度
        self.y_position = (screen_height - 300) // 2  # 300 是窗口高度

        # 设置窗口大小和位置
        master.geometry(f"500x300+{self.x_position}+{self.y_position}")

        # 主框架
        main_frame = ttk.Frame(master)
        main_frame.pack(padx=20, pady=20)

        # 欢迎标签
        welcome_label = ttk.Label(main_frame, text="欢迎使用垃圾邮件过滤程序\n点击下方按钮查看过滤结果",
                                  font=("Helvetica", 16))
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # 查看结果按钮
        show_results_button = ttk.Button(main_frame, text="查看结果", command=self.show_results)
        show_results_button.grid(row=1, column=0, columnspan=2, pady=(20, 40))

        # 展示结果页码
        self.page_index = 0

        # 导入结果文件
        try:
            with open("testResult.txt", "r") as file:
                self.results = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "testResult.txt not found.")
            return

        # 分类
        self.r = {'0': "垃圾邮件", '1': "正常邮件"}

    def show_results(self):
        # 创建一个新窗口展示结果
        result_window = tk.Toplevel(self.master)
        result_window.title("过滤结果")

        # 设置窗口大小和位置
        result_window.geometry(f"500x400+{self.x_position}+{self.y_position}")

        # 添加上一页下一页按钮
        next_button = ttk.Button(result_window, text="下一页", command=lambda: self.show_page(result_window, 1))
        next_button.place(x=350, y=350)
        prev_button = ttk.Button(result_window, text="上一页", command=lambda: self.show_page(result_window, -1))
        prev_button.place(x=50, y=350)

        # 创建框架
        frame = ttk.Frame(result_window)
        frame.pack()

        # 创建listbox
        self.result_listbox = Listbox(frame, height=15, width=50)
        self.result_listbox.pack(side="left", padx=10)

        # 展示结果
        self.display_results()

    def display_results(self):
        # 清除listbox
        self.result_listbox.delete(0, tk.END)

        # 展示结果范围
        start_index = self.page_index * 10
        end_index = start_index + 10 if start_index + 10 <= len(self.results) else len(self.results)

        for i, result in enumerate(self.results[start_index:end_index], start=start_index + 1):
            classification = result.strip().split(' ')[0]

            # 创建包含按钮和标签的框架
            item_frame = ttk.Frame(self.result_listbox)
            item_frame.pack(anchor="w", pady=5)

            # 展示邮件信息按钮
            button = ttk.Button(item_frame, text=f"邮件 {i}", command=lambda j=i: self.show_detail(j))
            button.grid(row=0, column=0, padx=10)

            # Label to display classification result
            label = ttk.Label(item_frame, text=f"{self.r[classification]}")
            label.grid(row=0, column=1)

    def show_detail(self, mail_id):
        # 在新窗口展示邮件详情
        mail_content = self.results[mail_id - 1].strip().split(' ', 1)[1]

        detail_window = tk.Toplevel(self.master)
        detail_window.title("邮件内容")

        # 设置窗口大小和位置
        detail_window.geometry(f"500x400+{self.x_position}+{self.y_position}")

        # 展示邮件内容
        frame = ttk.LabelFrame(detail_window, text=f"邮件{mail_id}内容", height=300, width=500)
        frame.pack(padx=10, pady=10)

        text_widget = tk.Text(frame, wrap="word", height=25, width=60)
        text_widget.pack(side="left", padx=10)

        scrollbar = Scrollbar(frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")

        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.insert(tk.END, mail_content)

    def show_page(self, result_window, direction):
        # 删除上个窗口
        result_window.destroy()

        self.page_index += direction

        if self.page_index < 0:
            self.page_index = 0

        # 每个界面最多展示10个邮件
        max_pages = (len(self.results) + 9) // 10 - 1
        if self.page_index > max_pages:
            self.page_index = max_pages

        # 创建新窗口
        self.show_results()


if __name__ == "__main__":
    testingNB()
    root = tk.Tk()
    app = SpamFilterApp(root)
    root.mainloop()
