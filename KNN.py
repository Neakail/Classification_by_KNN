# -*- coding:utf-8 -*-
import xlrd
from sklearn.neighbors import KNeighborsClassifier

# 构建等级(字母)-等级(数字)词典
chara_number = {
    u'A':1,
    u'B':2,
    u'C':3,
    u'D':4,
    u'E':5,
    u'F':6,
    u'G':7
}


# 训练KNN分类器,其中N为4
def knn_classifier(train_x, train_y):
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(train_x, train_y)
    return model


# 读取xlsx文件
def read_data(fname):
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    sh = bk.sheet_by_name("Sheet1")
    nrows = sh.nrows
    ncols = sh.ncols
    return sh,nrows,ncols

# 生成训练集特征矩阵x与结果向量y
def create_vectors(sh,nrows):
    data = []
    sex = []
    for i in range(nrows):
        row_data = sh.row_values(i)
        if row_data.pop() == u'女':
            sex.append(1)
        else:
            sex.append(0)
        data.append(row_data)
    trans(data)
    return data,sex

# 生成测试集特征矩阵x
def create_test_vectors(sh,nrows):
    data = []
    for i in range(nrows):
        row_data = sh.row_values(i)
        data.append(row_data)
    trans(data)
    return data

# 将等级(字母)转换成等级(数字)
def trans(data):
    length = len(data)
    height = len(data[0])
    for i in xrange(length):
        for j in xrange(height):
            for each_chara_number in chara_number:
                if data[i][j] == each_chara_number:
                    data[i][j] = chara_number[each_chara_number]
            data[i][j] = int(data[i][j])
    return data

if __name__ == '__main__':
    # 读取训练集
    fname = 'Students-Train.xlsx'
    sh,nrows,ncols = read_data(fname)
    data,sex = create_vectors(sh,nrows)

    # 训练KNN分类模型
    model = knn_classifier(data,sex)

    # 读取测试集
    test_frame = 'Students-Test.xlsx'
    test_sh,test_nrows,test_ncols = read_data(test_frame)
    test_data = create_test_vectors(test_sh,test_nrows)

    # 使用模型预测测试集
    result = model.predict(test_data)
    print '使用模型预测测试集'
    print '测试集结果为:'
    print result
    print '(0为男性,1为女性)'
    print '--------------------'

    # 使用原训练集检测模型效果
    result = model.predict(data)
    true_answer = 0
    for i in xrange(len(sex)):
        if sex[i] == result[i]:
            true_answer += 1
    pre = true_answer*1.0/(len(sex))
    print '使用原训练集检测模型'
    print '训练集的个数为:' + str(len(sex))
    print '准确预测的个数为:' + str(true_answer)
    print '准确率为:' + str(pre)



