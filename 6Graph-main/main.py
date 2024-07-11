from SpacePartition import *
from PatternMining import *


if __name__ == "__main__":

    # 加载数据
    data = np.load("./seeds.npy")
    patterns = []
    outliers = []
    # 进行地址空间划分，得到结果
    results = DHC(data)

    # 对每个结果进行异常检测，得到模式和异常
    for r in results:
        p, o = OutlierDetect(r)
        patterns += p
        outliers += o

    # your can seed the number of iter, usually < 5
    # 继续对异常进行递归划分和检测
    for _ in range(3):
        results = DHC(np.vstack(outliers))
        outliers = []
        for r in results:
            p, o = OutlierDetect(r)
            patterns += p
            outliers += o

    # display or directly use for yourself
    # 打印每个模式的地址区域及值
    for index, p in zip(list(range(len(patterns))), patterns):
        Tarrs = p.T

        address_space = []

        for i in range(32):
            splits = np.bincount(Tarrs[i], minlength=16)
            if len(splits[splits > 0]) == 1:
                address_space.append(format(
                    np.argwhere(splits > 0)[0][0], "x"))
            else:
                address_space.append("*")
        print("No.", index, "address pattern")
        print("".join(address_space))
        print("-"*32)
        for iparr in p:
            print("".join([format(x, "x") for x in iparr]))
        print()
