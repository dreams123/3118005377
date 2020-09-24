import jieba
import re
import numpy as np
import sys


# 对文本进行预处理，使文本仅保留中文
def yuchuli(line):
    repl = re.compile(u"[^\u4e00-\u9fa5]")
    line = repl.sub('', line)
    return line


def get_vector(str1, str2):

    # 分词并分别构建源文本和查重文本的词表
    cut1 = jieba.cut(str1)
    cut2 = jieba.cut(str2)
    list1 = (','.join(cut1)).split(',')
    list2 = (','.join(cut2)).split(',')

    # 构建总词表，包括了源文本和查重文本的所有词
    list_all = list(set(list1 + list2))

    # 生成两个用0填充的数组，方便后续存储向量
    word_vec1 = np.zeros(len(list_all))
    word_vec2 = np.zeros(len(list_all))

    for i in range(len(list_all)):

        # 遍历list_all中每个词在两篇文章的出现次数，文本转化为向量
        for j in range(len(list1)):
            if list_all[i] == list1[j]:
                word_vec1[i] += 1

        for k in range(len(list2)):
            if list_all[i] == list2[k]:
                word_vec2[i] += 1

    # 输出向量
    return word_vec1, word_vec2


# 余弦函数计算
def consin(vec1, vec2):
    dis = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return dis


if __name__ == '__main__':
    # 输入论文原文路径以及查重论文路径
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]


# 对源文本以及查重文本进行预处理
with open(file1_path, 'r', encoding='UTF-8') as file1:
    s1 = file1.read()
    s1 = yuchuli(s1)
with open(file2_path, 'r', encoding='UTF-8') as file2:
    s2 = file2.read()
    s2 = yuchuli(s2)

# 进行文本向量和余弦计算
v1, v2 = get_vector(s1, s2)
a = consin(v1, v2)
b = round(a, 2)
print("文章重复率运算结果为:", b)

result_path = sys.argv[3]  # 新创建的答案文件文件的存放路径
file = open(result_path, 'w')
file.write(str(b))
file.close()

try:
    file1_path == ' '
except IndexError:
    print("输入路径中不存在指定源文本")

try:
    file2_path == ' '
except IndexError:
    print("输入路径中不存在指定查重文本")

try:
    result_path == ' '
except IndexError:
    print("输出文件中未查到指定答案文本")
