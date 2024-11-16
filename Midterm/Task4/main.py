import random
import dataset
import init
import wtf

"""
写一个计数器，用来记录迭代次数
"""


def counter():
    a = 0
    while 1:
        a += 1
        yield a


if __name__ == '__main__':
    counter0 = counter()
    w = 1000   # 迭代次数

    group = {}
    f = next(counter0)
    group[f"第{f}代"] = init.randomly_generate_initial_population()

    for i in range(w):
        f_generation = group[f"第{f}代"]
        f = next(counter0)
        group[f"第{f}代"], minimum_mileage, the_best_individual_of_the_previous_generation = wtf.wtf(f_generation)
        print(f"第{f-1}代：{minimum_mileage}, 路线：{the_best_individual_of_the_previous_generation}")

# 按照论文，最佳个体应为
# 67.5km
# 04769285310 或 01358294760

