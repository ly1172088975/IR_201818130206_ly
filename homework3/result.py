# -*- coding: utf-8 -*-
import json
import re
import codecs
import math

'''读取文件'''

f = open(r"C:\\Users\\11720\\Desktop\\IR&DM\\EX\\E3\\query-res.txt", "r")
f1 = open(r"C:\\Users\\11720\\Desktop\\IR&DM\\EX\\E3\\qrels.txt", "r")
path1 = "C:\\Users\\11720\\Desktop\\IR&DM\\EX\\E3\\result.txt"
f2=codecs.open(path1, 'w', encoding='utf-8')
querylist=dict()
'''载入结果'''
result=dict()
for i in range(1,56):
    result[i]=dict()
for i in range(1,56):
    line=f.readline()
    querylist[i]=line
    for k in range(1,11):
        ff=f.readline()
        ff=ff.replace('\n','')
        result[i][k]=ff
print("load result finished")


'''建立相关系数数组'''
answer=dict()
for i in range(1,56):
    answer[i]=dict()
linee=f1.readline()
while linee :
    ele=linee.split()
    keyy=int(ele[0])-170
    docc=ele[2]
    gain=ele[3]
    answer[keyy][docc]=gain
    linee=f1.readline()
print("set gain finished")



'''进行结果评估'''
endd=dict()
'''MAP'''
apq = dict()
for i in range(1, 56):
    sum = 0
    num=0
    for j in range(1, 11):
        k = 0
        doid = result[i][j]
        #print(doid)
        if doid in answer[i]:
            if answer[i][doid] != 0:
                k = k + 1
                num=num+1
                sum = sum + k / j
    if num==0:
        apq[i]=0
    else:
        apq[i] = sum/num
sum = 0
for i in range(1, 56):
    sum = sum + apq[i]
endd[1] = sum / 55
print("MAP finished")
'''MRR'''
rrs = dict()
for i in range(1, 56):
    rrs[i] = 0
    for j in range(1, 11):
        doid = result[i][j]
        if doid in answer[i]:
            if answer[i][doid] != 0:
                rrs[i] = 1 / j
                break
sum = 0
for i in range(1, 56):
    sum = sum + rrs[i]
endd[2] = sum / 55
print("MRR finished")
'''NDCG'''
ndcg=dict()
for i in range(1, 56):
    ndcg[i] = dict()
for i in range(1, 56):
    f2.write(querylist[i]+'\n')
    cg = dict()
    gain = dict()
    log = dict()
    log[1] = 1
    dcg = dict()
    idcg = dict()
    gain1 = 0
    gain2 = 0
    '''计算dcg'''

    for j in range(1, 11):
        doid = result[i][j]
        if doid in answer[i]:
            gain[j] = float(answer[i][doid])
            if gain[j] == 1:
                gain1 = gain1 + 1
            elif gain[j] == 2:
                gain2 = gain2 + 1
        else:
            gain[j] = 0
        if j == 1:
            cg[j] = gain[j]
        else:
            cg[j] = cg[j-1] + gain[j]
        if j >1:
            log[j] = math.log2(j)
        if j == 1:
            dcg[j] = gain[j]
        else:
            dcg[j ] = dcg[j-1] + gain[j] / log[j ]
    '''计算IDCG'''
    for k in range(1, 11):
        #print(gain2)
        #print(gain1)
        if gain2 > 0:
            gain2 = gain2 - 1
            if k == 1:
                idcg[k] = 2
            else:
                idcg[k] = idcg[k - 1] + 2 / math.log2(k)
        elif gain1 > 0:
            gain1 = gain1 - 1
            if k == 1:
                idcg[k] = 1
            else:
                idcg[k] = idcg[k - 1] + 1 / math.log2(k)
        else:
            if k == 1:
                idcg[k] = 0
            else:
                idcg[k] = idcg[k - 1] + 0 / math.log2(k)

    '''计算NDCG'''
    for k in range(1, 11):
        if idcg[k] == 0:
            ndcg[i][k] = 0
        else:
            ndcg[i][k] = dcg[k] / idcg[k]
        doid=result[i][k]
        f2.write(str(doid) + ' ' + ':' + ' ' + 'NDCG:' + ' ' + str(ndcg[i][k]) + '\n')
f2.write('\n'+'MAP_result:'+' '+str(endd[1])+'\n')
f2.write('\n'+'MRR_result:'+' '+str(endd[2])+'\n')
f1.close()
f2.close()