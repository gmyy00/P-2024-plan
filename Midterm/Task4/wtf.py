import random
import dataset
import init
import main

# 最优解67.5km，其对应的配送路径方案为：路径1：0－4－7－6－0；路径2：0－2－8－5－3－1－0。
# 最终的个体为 04769285310 或 01358294760

# p = []
# for n in range(0, 10):
#     p.append([])
#     for m in range(0, 10):
#         p[n].append(dataset.d.pop(0))

"""
我设置的p有两个标p[n][m]
n和m是节点，其中0和9是出发点，1~8是需求物资点
这样的话我们就可以用 p[n][m] 来表示从 n 走到 m 的距离
"""

"""
得到：
    p[0][m] p[1][m] p[2][m] p[3][m] p[4][m] p[5][m] p[6][m] p[7][m] p[8][m] p[9][m]
——————————————————————————————————————————————————————————————————————————————————————
p=[ [0,     4.0,    6.0,    7.5,    9.0,    20.0,   10.0,   16.0,   8.0,    0],     |  p[n][0]
    [4.0,   0,      6.5,    4.0,    10.0,   5.0,    7.5,    11.0,   10.0,   4.0],   |  p[n][1]
    [6.0,   6.5,    0,      7.5,    10.0,   10.0,   7.5,    7.5,    7.5,    6.0],   |  p[n][2]
    [7.5,   4.0,    7.5,    0,      10.0,   5.0,    9.0,    9.0,    15.0,   7.5],   |  p[n][3]
    [9.0,   10.0,   10.0,   10.0,   0,      10.0,   7.5,    7.5,    10.0,   9.0],   |  p[n][4]
    [20.0,  5.0,    10.0,   5.0,    10.0,   0,      7.0,    9.0,    7.5,    20.0],  |  p[n][5]
    [10.0,  7.5,    7.5,    9.0,    7.5,    7.0,    0,      7.0,    10.0,   10.0],  |  p[n][6]
    [16.0,  11.0,   7.5,    9.0,    7.5,    9.0,    7.0,    0,      10.0,   16.0],  |  p[n][7]
    [8.0,   10.0,   7.5,    15.0,   10.0,   7.5,    10.0,   10.0,   0,      8.0],   |  p[n][8]
    [0,     4.0,    6.0,    7.5,    9.0,    20.0,   10.0,   16.0,   8.0,    0]    ] |  p[n][9]
"""

"""
第一步：编码

按照论文，我们可以给每个路径来编号
如编号：06498253170，表示路径一：0->6->4->9(0),路径2：9(0)->8->2->5->3->1->7->0
可以看到，路径编号的开头和结尾都是0
所以我们只需要对中间的部分进行交叉互换和变异操作
"""

# 例：
# 路线：04712986530
# 9 + 7.5 + 11 + 6.5 + 6 = 40       8 + 10 + 7 + 5 + 7.5 = 37.5     共 67.5
# 2 + 2 + 1 + 2 = 7                 2 + 4 + 1 + 1 = 8

"""
第二步： 初始群体生成

随机生成一个初始群体，按照论文，群体规模 N = 20
代码在 init.py 里面
"""

# 例：
# group["第1代"] = [ '04258316970', '04719586230', '06748593120', '02617359480', '07931245860',
#                 '03654281970', '07956341280', '08479235610', '06891274530', '02738641590',
#                 '05826713940', '02645189730', '03479816520', '02415983760', '04961532870',
#                 '09584321760', '08265917430', '07265931840', '02713589640', '02475638910']


"""
第三步：适应度计算

计算每次汽车运货的总里程数
并依此计算适应度
通过适应度来决定交叉与变异的比例
"""


# 在这个大函数中，我希望输出三个对象
# 第一个是 f+1_generation (尽管我仍然用 f_generation 来表示)
# 第二个是 最少里程数
# 第三个是 最佳个体的路线

def wtf(f_generation):
    p = init.get_map()

    mileage = []
    total_mileage = []
    load_limit = []
    infeasible_paths = []
    individual_fitness = []

    """
    每开始计算一个个体的适应度时，在  mileage  total_mileage  load_limit  infeasible_paths  这四个列表里新添加一个元素
    分别为  D(40)  0  Q(8)  0
    每移动到下一个节点时，total_mileage -= this_mileage ，如果节点为1~8，load_limit -= this_unloading
    然后检测 mileage 和 load_limit
    如果其中有一个为0，则 infeasible_paths +1，
    如果均不为0，则检测当前节点是否为9或0
    如果是，则重置 mileage 和 load_limit
    计算完成该个体的 total_mileage 与 infeasible_paths 后，计算该个体的 individual_fitness 
    按照论文，F_j = 1 / (Z_j + M_j * G)
    但是我已经把 惩罚里程数(G) 加到 total_mileage 里面
    所以可以直接 F_j = 1 / Z_j
    """

    for individual_serial_number in range(len(f_generation)):
        mileage.append(40)
        total_mileage.append(0)
        load_limit.append(dataset.Q)
        infeasible_paths.append(0)
        route = [int(i) for i in list(f_generation[individual_serial_number])]

        for i in range(1, len(route)):
            # 例：route = [0, 7, 9, 4, 5, 1, 3, 6, 8, 2, 0], len(route) = 11
            this_mileage = p[route[i - 1]][route[i]]
            if route[i] != 0 and route[i] != 9:
                this_unloading = dataset.q[route[i] - 1]
                load_limit[individual_serial_number] -= this_unloading * 1000
            mileage[individual_serial_number] -= this_mileage
            total_mileage[individual_serial_number] += this_mileage
            """检测 mileage 和 load_limit 是否小于0"""
            """如果是，infeasible_paths +1"""
            """并将 惩罚里程数(G) 加到 total_mileage 里面"""
            if mileage[individual_serial_number] < 0 or load_limit[individual_serial_number] < 0:
                infeasible_paths[individual_serial_number] += 1
                total_mileage[individual_serial_number] += dataset.G
            """检测当前节点是否为9或0"""
            """如果是，就重置 mileage 和 load_limit"""
            if route[i] == 9 or route[i] == 0:
                mileage[individual_serial_number] = dataset.D
                load_limit[individual_serial_number] = dataset.Q
        """将惩罚里程数加到总里程数里面"""

        """我们得到了该个体的 total_mileage 与 infeasible_paths"""
        """按照论文，接下来计算该个体的 适应度 """
        individual_fitness.append(1 / (total_mileage[individual_serial_number]))

    """
    第四步：选择操作
    
    我们需要依照个体适应度从大到小来对这一代群体进行排列
    使得最佳个体排在首位
    从 f_generation 中挑出 the_best_individual_of_the_previous_generation
    """

    combination = sorted(zip(individual_fitness, f_generation), reverse=True, key=lambda x: x[0])
    f_generation = [pair[1] for pair in combination]
    individual_fitness.sort(reverse=True)


    the_best_individual_of_the_previous_generation = f_generation.pop(0)

    """之后的 f_generation 只有19个个体"""

    """接下来计算每个个体的适应度所占的比例"""

    individual_fitness.pop(0)
    # 从列表中去除最佳个体的个体适应度，因为已经不参与接下来的交换和变异操作

    minimum_mileage = min(total_mileage)

    sum_of_fitness = sum(individual_fitness)
    proportion_of_individual_fitness = []
    for i in individual_fitness:
        proportion_of_individual_fitness.append(i / sum_of_fitness)

    """
    第五步：交叉操作
    
    按照论文，交叉的概率是0.95，去除最佳个体后，剩余19个
    这些需要使用 轮盘赌选择 来进行选择
    """

    """在两个字符串中随机选取长度为1到8的字串进行交换"""

    def exchange(str1, str2):
        str1 = str1[1:-1]
        str2 = str2[1:-1]

        length = random.randint(1, len(str1) - 1)
        start = random.randint(0, len(str1) - length)
        end = start + length

        slice_str1 = str1[start:end]
        slice_str2 = str2[start:end]

        k_str1 = "".join([i for i in str1 if i not in slice_str1])
        k_str2 = "".join([i for i in str2 if i not in slice_str2])

        str1 = "0" + slice_str1 + k_str1 + "0"
        str2 = "0" + slice_str2 + k_str2 + "0"

        return str1, str2

    """下面部分为 轮盘赌选择 并 对换 的代码"""
    cumulative_probability = 0
    list_of_cumulative_probability = [0]
    for i in proportion_of_individual_fitness:
        cumulative_probability += i
        list_of_cumulative_probability.append(cumulative_probability)

    temp = random.random()
    while temp <= 0.95:
        temp = random.random()
        temp1 = []
        for i in range(2):
            a = random.random()
            k = 0
            while 1:
                if a < list_of_cumulative_probability[k]:
                    k -= 1
                elif list_of_cumulative_probability[k] <= a < list_of_cumulative_probability[k + 1]:
                    temp1.append(k)
                    break
                elif list_of_cumulative_probability[k + 1] <= a:
                    k += 1
        f_generation[temp1[0]], f_generation[temp1[1]] \
            = exchange(f_generation[temp1[0]], f_generation[temp1[1]])

    """
    第六步：变异操作
    
    按照论文，变异概率为0.05，
    依照这个概率，随机寻找一个个体，进行对换操作    
    """
    temp2 = random.random()
    while temp2 <= 0.05:
        temp2 = random.random()
        temp3 = random.randint(0, len(f_generation) - 1)
        list_of_selected_individuals = list(f_generation[temp3])[1:-1]
        idx1, idx2 = random.sample(range(len(list_of_selected_individuals)), 2)
        list_of_selected_individuals[idx1], list_of_selected_individuals[idx2] = list_of_selected_individuals[idx2], \
            list_of_selected_individuals[idx1]
        f_generation[temp3] = "0"+"".join(list_of_selected_individuals)+"0"

    """
    第七步：生成下一代
    
    将之前挑出来的上一代最佳再放入经过交叉互换和变异操作后的群体里
    交换和变异后的19个,和上一代最佳的1个,共20个
    共同组成下一代
    """
    f_generation.append(the_best_individual_of_the_previous_generation)

    return f_generation, minimum_mileage, the_best_individual_of_the_previous_generation
