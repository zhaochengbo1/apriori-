1.The 'file_path' that needs to be replaced:
data.py      line 4
Analsysis.py line 8
Apriori.pyi  line 136

2.建议在演示中增加这一部分内容:
2.1考虑到普通Apriori算法过于基础，以及其具有的显著缺点：当事务数据库很大时，候选频繁 k 项集数量巨大；在验证候选频繁 k 项集的时候，需要对整个数据库进行扫描，非常耗时。
我们考虑如下的改进方案：使用FP-Growth算法，引入一个特殊的数据结构用于临时存储数据，以减少i/o次数；使用Mapreduce框架对输入的原始数据集进行Map分块处理，主进程将这些数据分块分布到Hadoop集群中各节点上，然后各节点对这些数据块进行并行处理。
2.2补充演示说明：FP-tree数据结构，算法实现流程，部分代码展示；Mapreduce程序结构，各阶段任务，部分代码展示。（可对关键代码进行展示及说明，即除却信息导入与预处理部分的，仅作算法实现的部分代码，代码如附件）

附件：
Mapreduce code（map代码/combination代码/reduce代码/完整代码:MBAMapper.java/Combination.java/MBAReduce.java/MBADriver.java）
FPtree code(FPtree.java/TreeNode.java)

3.
FP-Tree算法全称是FrequentPattern Tree算法，就是频繁模式树算法，他与Apriori算法一样也是用来挖掘频繁项集的，不过不同的是，FP-Tree算法是Apriori算法的优化处理，他解决了Apriori算法在过程中会产生大量的候选集的问题，而FP-Tree算法则是发现频繁模式而不产生候选集。但是频繁模式挖掘出来后，产生关联规则的步骤还是和Apriori是一样的。

4.
mapper阶段任务:
maper阶段的map()函数根据购物篮子中的商品生成如下键-值对
[<crackers,icecream>,1]
[<crackers,coke.,1]
但是在程序自动分类过程中会和出现如下现象
购物篮T1：crackers,icecream,coke
购物篮T2：icecream,coke,crackers
根据关联规则，对于T1会生成如下规则
[(crackers,icecream),1]
[(crackers,coke),1]
[(icecream,coke),1]
对于T2则会生成如下规则
[(icecream,coke),1]
[(icecream,crackers),1]
[(coke,crackers),1]
从中我们可以看到，有六对规则，但是我们发现(crackers,icecream)和(icecream,crackers)是一样的，在这里会被分成不同的规则，所以在生成规则之前需要对商品按照字母顺序进行排序，就可以避免这个问题

map中的combinations是一个简单的工具，使用Combinations.generateCombinations(s1,s2,…,sn)方法可以生成给定的集合，假设购物篮为{a,b,c}，假设生成具有两个商品的规则，则分类结果如下所示：[a,b],[a,c],[b,c]

reduce阶段任务:
这个阶段就是对规则的支持度进行统计
