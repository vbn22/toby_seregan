# -*- coding: utf-8 -*-
from math import sqrt



def pearson(v1,v2):
    # Простые суммы
    sum1=sum(v1)
    sum2=sum(v2)
    # Суммы квадратов
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])
    # Суммы произведений
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
    # Вычисляем r (коэффициент Пирсона)
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 0
    return 1.0-num/den


def printclust(clust,labels=None,n=0):
    # отступ для визуализации иерархии
    for i in range(n):
        print ' ',
        if clust.id<0:
            # отрицательный id означает, что это внутренний узел
            print '-'
        else:
            # положительный id означает, что это листовый узел
            if labels==None: print clust.id
            else: print labels[clust.id]
    # теперь печатаем правую и левую ветви
    if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)


def hcluster(rows,distance=pearson):
    distances={}
    currentclustid=-1
    # В начале кластеры совпадают со строками
    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]
    while len(clust)>1:
        lowestpair=(0,1)
        closest=distance(clust[0].vec,clust[1].vec)
        # в цикле рассматриваются все пары и ищется пара с минимальным
        # расстоянием
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                # вычисленные расстояния запоминаются в кэше
                if (clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)
                    d=distances[(clust[i].id,clust[j].id)]
            if d<closest:
                closest=d
                lowestpair=(i,j)
        # вычислить среднее для двух кластеров
        mergevec=[(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]
        # создать новый кластер
        newcluster=bicluster(mergevec,left=clust[lowestpair[0]],
        right=clust[lowestpair[1]],
        distance=closest,id=currentclustid)
        # идентификаторы кластеров, которых не было в исходном наборе,
        # отрицательны
        currentclustid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    return clust[0]

class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance



def readfile(filename='blogdata.txt'):
    lines=[line for line in file(filename)]
    # Первая строка содержит названия столбцов
    colnames=lines[0].strip( ).split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip( ).split('\t')
        # Первый столбец в каждой строке содержит название строки
        rownames.append(p[0])
        # Остальные ячейки содержат данные этой строки
        data.append([float(x) for x in p[1:]])
    return rownames,colnames,data


if __name__ == "__main__":
    readfile()