import numpy as np
import networkx as nx      # 用于图的操作和算法

# the max free dimensions you can tolerate
# 阈值定义
threshold = 12


# 距离函数
def seed_distance(a, b):
    return len(np.argwhere(a != b))


# 异常检测
def OutlierDetect(arrs):
    # 如果地址数组长度小于等于1，返回空模式和异常
    if len(arrs) <= 1:
        return [], [arrs]

    # init the egde weight
    # 计算所有地址对之间的距离，并将距离小于等于阈值的对添加到列表中
    dis = []
    for i in range(len(arrs)):
        for j in range(i + 1, len(arrs)):
            w = seed_distance(arrs[i], arrs[j])
            if w > threshold:
                continue
            dis.append((i, j, w))

    dis = sorted(dis, key=lambda x: x[2])

    # Kruskal alg build the mst
    # 使用Kruskal算法构建最小生成树，MST的一种
    G = nx.Graph()
    G.add_nodes_from(range(len(arrs)))
    for i, j, w in dis:
        # 返回 i j 所有可达节点
        idescendants = nx.algorithms.descendants(G, i)
        jdescendants = nx.algorithms.descendants(G, j)
        idescendants.add(i)
        jdescendants.add(j)
        if (i in jdescendants):
            # 同一个联通分量 不加
            continue
        if density(arrs[list(idescendants | jdescendants)]) > density(
                arrs[list(idescendants)]) and density(
                    arrs[list(idescendants | jdescendants)]) > density(
                        arrs[list(jdescendants)]):
            # 计算两个联通分量的密度

            G.add_edge(i, j, len=w)
    patterns = []
    outliers = []
    # 遍历所有连接分量，构建模式和异常列表
    for l in list(nx.connected_components(G)):
        l = list(l)
        if len(l) > 1:
            patterns.append(arrs[l])
        else:
            outliers.append(arrs[l[0]])

    # 返回模式和异常
    return patterns, outliers


# 计算地址数组的密度
def density(arrs):
    if len(arrs) == 1:
        return 0

    Tarrs = arrs.T

    xi = np.count_nonzero([
        np.count_nonzero(np.bincount(Tarrs[i], minlength=16)) - 1
        for i in range(32)
    ])

    return len(arrs) / xi


# for test
def showPatternAndOutliers(patterns, outliers):
    print("********PatternAndOutliers**********")
    for p in patterns:
        address_space = []
        Tarrs = p.T
        for i in range(32):
            splits = np.bincount(Tarrs[i], minlength=16)
            if len(splits[splits > 0]) == 1:

                address_space.append(format(
                    np.argwhere(splits > 0)[0][0], "x"))
            else:
                address_space.append("*")
        print("".join(address_space))
        for i in range(len(p)):
            print("".join([format(x, "x") for x in p[i]]))

        print()

    print("********out**********")
    for o in outliers:
        print("".join([format(x, "x") for x in o]))
    print()

