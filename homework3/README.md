#  实验三：IR Evaluation

##  1.文件说明

对于老师所给予的55个测试样例，我使用实验二代码得出结果并且将结果输出，保存为文件query-res.txt。并且将循环测试55个query的代码更新为ex3.py。

通过query.txt文件，将其中的编号和query文本摘出来，保存为query1.txt便于后序使用。

通过老师所给的网站，将各个query的查询结果的gain保存为gain.txt，其中第一列为query编号，第二列忽略，第三列为docu_id，第四列是一个{0，1，2}的数，将此作为gain，0或者没有出现在文件中作为不相关，1作为部分相关，2作为很相关。

最后结果保存为result.txt。在此取K=10，此参数可以在ex3.py文件中修改（并没有进行交互），此文档示例使用query：l、t、n；document：l、n、c的方法，其他方法可通过ex3.py交互进行修改。

ex3.py是实验二代码的改进，可以循环将55个query进行查询并且进行储存。

result.py是进行评价的代码，可以得到最后的result结果文件

##  2.三种方法介绍以及实现

###  MAP

该方法以本例（K=10）来说，是将每一个相关检索到的文件的Precision取一个平均值，并且将所有结果进行一个平均操作，可以看到在本例中，55个query的MAP值为：0.26889847454133164

该操作的实现如下：

```python
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
```

注意，readline函数会将该行最后的换行符也录下来，并且有换行符，doid就不会和answer中的匹配。

###  MRR

MRR取每个query的结果中第一个相关文档的顺序，对他们先取倒数随后求和。

这里55个query的结果为：0.7306277056277057

实现如下：

```python
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
```

###  NDCG

NDCG是一个比较流行的方法，对于每一个结果先取CG值，这个值是该结果之前的所有gain之和。

随后去DCG，该值是对于此结果及之前的结果，按顺序将gain/log2（n）求和。

随后进行IDCG的求值，IDCG就是立项查询结果下的值，对于此值，计算过程如下：

```python
    for k in range(1, 11):
        print(gain2)
        print(gain1)
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
```

接下来将每一个DCG除以对应的IDCG值得到该结果的NDCG值。部分结果示例如下：完整结果见result.txt

```python
Sotomayor prosecutor racial comments

306094610072088576 : NDCG: 1.0
306238453740359680 : NDCG: 1.0
306117963956768768 : NDCG: 1.0
306238197887803392 : NDCG: 1.0
306830999831056384 : NDCG: 1.0
306137941439303680 : NDCG: 1.0
34921291089711104 : NDCG: 0.9172509175420708
306433698578964480 : NDCG: 0.9231980994375002
306214390988935168 : NDCG: 0.9280892825718658
306212163826106369 : NDCG: 0.9888608889264011
```
