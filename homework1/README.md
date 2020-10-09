# 实验一：Inverted index and Boolean  Retrieval Model
<br/>   
（注：文件夹下，tweets.txt是初始文本数据信息，dict.txt是中间生成的倒排索引表，ex1.py是本实验源码）

<br/>

## 1.读取、整理文本数据信息
本次实验的数据信息是以一种类json的格式给出的，但其整体格式并非json，需要按行以json读取处理，主要保存两个字段信息：text与id。
从tweets.txt文本文件中读取数据，对数据按行遍历，每一行就是一条文本，分别记录其text与id，存入text_set与id_set字典中。   

<br/>
 
## 2.建立倒排索引
倒排索引是以词项作为索引的key值，对应的value是包含该词的文档编号，这些文档都被存储在一个数组（集合）中，这样对于一个查询，只需找到查询query里的词项，根据倒排索引去找到对应的文档即可。
对于1中得到的text_set，遍历其中的元素，对于每一篇文档，首先进行预处理，将text去除标点，分词、词项还原，生成一个个标准化的词项，再将每个词项与当前文档对应的id一一对应，添加到dict中。

```python
dic = {}
for j in range(1,len(text_set)+1):
    content = text_set[j]
    content = content.lower()
    content = re.sub(re_punctuation, "", content)
    words = word_tokenize(content)
    w_list = []
    for w in words:
        #w1 = WordNetLemmatizer().lemmatize(w, pos="n")
        w2 = WordNetLemmatizer().lemmatize(w, pos="v")
        w3 = WordNetLemmatizer().lemmatize(w2, pos="a")
        w_list.append(w3)
    for w in w_list:
        if w not in dic:
            #当前索引字典中不存在这个词项
            tmp = set()
            tmp.add(id_set[j])
            dic[w] = tmp
        else:
            dic[w].add(id_set[j])
```
在这个过程中，去除标点使用的是python自带的正则表达式去符号，分词、词项还原使用nltk函数完成。
存在的问题是：正则表达式去符号过程中，可能会将一些以符号连接的词组直接划分成一个词，对最后结果造成干扰，而这种词的频率一般很低，不会超过3，因此在记录时，对这些词频过低的词直接选择忽略，可以一定程度上避免冗余信息；而本次实验的数据集并不大，因此对于那些过高词频的词不需要忽略，加以记录即可。
此外，在词项标准化过程中，忽略的名词形式的复原，因为这会错误划分某些特定名词（如将us视作复数而变成u），影响最后查询结果。
最后将倒排索引表的内容，写入dict.txt文本文件中，之后查询时，直接读取该文件即可。

<br/>

## 3.查询
首先读取dict文本信息，获取倒排索引表，然后输入查询query，对于输入的query，需要进行和2中一样的预处理，将查询划分成统一形式的词项，其中and，or，not作为三个关系连接词，不在可查询的范围内，它们仅作为连接词，表达查询关系。
对于查询query，如果是词组，以空格分割，实际上就是以and连接的多个词的查询情况，对于and，直接求交，or求并，	not求集合减法，python中的set类型提供了这三种操作方式，直接使用即可，当有多组关系词查询时，按照从左到右的顺序查询即可。
```python
    for j in q_list:
        if j == "and":
            flag = 1
        elif j == "or":
            flag = 2
        elif j == "not":
            flag = 3
        else:
            if j in dic:
                now = dic[j]
            else:
                now = set()
            if flag == 0:
                ans = ans | now
                flag = 4
            elif flag == 2 :
                ans = ans | now
            elif flag == 3:
                ans = ans - now
            else:
                ans = ans & now
```
这种查询方式的问题就在于：它并没有优先级，都是按照从左到右最近原则查询的，当连接词过多时，查询结果可能与预期有差别。

<br/>

## 4.测试结果
![image text](https://github.com/ly1172088975/IR_201818130206_ly/blob/main/homework1/1.jpg)
经过在原tweets文件和dict文件中检索，以上查询结果无误。

<br/>

## 5.总结
建立倒排索引的关键是将文本合理的划分为不同的词项并做好预处理，将词项处理标准，查询起来就会很方便；另一方面，对于多元查询，如何调整关系词的优先级也是影响查询效率与效果的一个关键。
在本实验中，我对于以上两点完成的还不是很到位，词项处理可能存在将不同词合并为一个词的情况，也没有实现更优化的查询方案，只是按照基本的自然语言逻辑进行查询，仍有改进空间。
