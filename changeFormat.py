import os

spam_folder = 'spam'
normal_folder = 'normal'
output_file = 'chineseoutput.txt'


# 定义函数：遍历文件夹，提取汉字内容
def extract_chinese_content(file_path):
    with open(file_path, 'r', encoding='gbk') as file:
        content = file.read()
        # print(content)
        chinese_content = ''.join(c for c in content if '\u4e00' <= c <= '\u9fa5')  # 提取汉字内容
        # print(chinese_content)
        return chinese_content


def main():
    spam_contents = []
    # print(len(os.listdir(spam_folder)))
    for filename in os.listdir(spam_folder):
        file_path = os.path.join(spam_folder, filename)
        chinese_content = extract_chinese_content(file_path)
        spam_contents.append(chinese_content)

    # 将spam内容写入文本文件
    with open(output_file, 'w', encoding='gbk') as file:
        for content in spam_contents:
            file.write('0	' + content)
            file.write('\n')

    # 添加换行符
    with open(output_file, 'a', encoding='gbk') as file:
        file.write('\n')

    normal_files = sorted(os.listdir(normal_folder))
    normal_contents = []
    for filename in normal_files:
        file_path = os.path.join(normal_folder, filename)
        chinese_content = extract_chinese_content(file_path)
        normal_contents.append(chinese_content)

    # 将normal内容写入文本文件
    with open(output_file, 'a', encoding='gbk') as file:
        for content in normal_contents:
            file.write('1	' + content)
            file.write('\n')


if __name__ == "__main__":
    main()
