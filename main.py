"""
write: terence
create date :2023/11/7
"""


# 银行家算法
# 定义三个二维数组
# 需要避免死锁 将new arr = 用户输入的临时分配的数组 - self.Available 对应的位置的数组 是否还能满足任意一个未完成进程的需要
class Bank:
    def __init__(self):
        self.Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]  # 最大矩阵
        self.Available = [3, 3, 2]  # 可分配
        self.Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]  # 已分配
        self.Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]  # 还需要
        # 标记当前进程是否完成 如果完成了就变成1 并把所有的资源还回available
        self.finish = [0, 0, 0, 0, 0]
        self.char_alphabet = ['A', 'B', 'C']

    def print_all_info(self):
        is_show_available = True
        print("进程名\t\tMax\t\t\tAllocation\t\t\tneed\t\t\tfinish\t\t\tavailable\t\t\t")
        for i in range(len(self.Max)):
            print(f"p{i + 1}\t\t\t", end="")
            for j in range(len(self.Max[i])):
                print(f"{self.Max[i][j]}", end=" ")
            print("\t\t\t", end="")
            for j in range(len(self.Max[i])):
                print(f"{self.Allocation[i][j]}", end=" ")
            print("\t\t\t", end="")
            for j in range(len(self.Max[i])):
                print(f"{self.Need[i][j]}", end=" ")
            print("\t\t\t", end="")
            # 输出进程完成信息
            if self.finish[i] == 0:
                print(f"False", end=" ")
                print("\t\t\t", end="")
            else:
                print(f"True", end=" ")
                print("\t\t\t", end="")
            if is_show_available:
                for j in range(len(self.Available)):
                    print(f"{self.Available[j]}", end=" ")
                print("\t\t\t", end="")
                is_show_available = False
            print("")

    def will_do_available(self, input_num: int):  # 对可分配数值进行分配
        temp_available: list[int] = []  # 当前输入的
        char_alphabet = ['A', 'B', 'C']
        index = 0
        # 输入三个值
        while index < 3:
            num = input(f"请输入{char_alphabet[index]}资源的值:")
            num = int(num)
            if self.Available[index] >= num:
                if num <= self.Need[input_num][index]:
                    temp_available.append(num)
                    index = index + 1
                else:
                    print("输入的资源大于实际需要的资源，请重新输入")
            else:
                print("输入的值大于可分配值,请重新输入")
        temp_arr = []  # 临时数组 存放临时可分配的数值 (剩余可分配的
        for i in range(len(self.Available)):
            # 用实际可分配的减去临时分配的 得出临时剩余可分配的
            temp_arr.append(self.Available[i] - temp_available[i])
        # 对需求表操作 生成临时剩余需要
        for k in range(len(self.Need[input_num])):
            self.Need[input_num][k] = self.Need[input_num][k] - temp_available[k]  # 生成新的Need表 如果不满足需要退回
            self.Allocation[input_num][k] = self.Allocation[input_num][k] + temp_available[k]
        # how to do determine make it 死锁 ？
        # 当前剩余可分配的加上目前已分配的能够满足任意一个最大需求量 那么就不会造成死锁
        # 剩余可分配的是否满足任意一个需要的 若不满足就会死锁 error don't to do way
        # define a variable determine current temporary available yes or no meet need-list  requre of any one
        is_meet = False
        for n in range(len(self.Need)):
            count = 0
            for k in range(len(self.Need[n])):
                # 只要任意一个可分配的值不完全满足任意一个需求列表的值 那么就会造成死锁
                # 还需要判断当前进程是否完成，如果是完成进程的话 ，统计没意义
                if self.finish[n] == 0:
                    if temp_arr[k] >= self.Need[n][k]:
                        # release need delete
                        count += 1
            # print(f"count = {count}")
            if count >= 3:
                # 满足需求
                is_meet = True
                break

        if is_meet:
            # 如果满足
            for i in range(len(self.Available)):  # 修改可分配数值
                self.Available[i] = self.Available[i] - temp_available[i]

        else:
            for k in range(len(self.Need[input_num])):
                self.Need[input_num][k] = self.Need[input_num][k] + temp_available[k]  # 不满足 退回
                self.Allocation[input_num][k] = self.Allocation[input_num][k] - temp_available[k]
            print("不满足,会造成死锁，进程挂起，资源分配失败")
        # 如果need表中存在3个值都为0的那么就需要 把已分配的资源返回
        return_resources = 0
        for k in range(len(self.Need[input_num])):
            if self.Need[input_num][k] == 0:
                return_resources += 1
        if return_resources >= 3:
            for i in range(len(self.Available)):
                self.Available[i] = self.Available[i] + self.Allocation[input_num][i]
            print(f"p{input_num + 1}进程完成，资源归还")
            self.finish[input_num] = 1
            for j in range(len(self.Allocation[input_num])):
                self.Allocation[input_num][j] = 0
        # 缺个进程结束标识符
        finish_count = 0
        for item in self.finish:
            if item == 1:
                finish_count = finish_count + 1
        if finish_count == len(self.finish):
            self.print_all_info()
            print("所有进程已完成")
            exit(0)
        self.print_all_info()

    def user_input(self):
        while True:
            n = input("请输入你要分配的进程(如分配p1则输入p1):")
            if n == 'p1':
                if self.finish[0] != 1:
                    self.will_do_available(0)
                else:
                    print("当前进程已完成，不可再分配资源")
            elif n == 'p2':
                if self.finish[1] != 1:
                    self.will_do_available(1)
                else:
                    print("当前进程已完成，不可再分配资源")
            elif n == 'p3':
                if self.finish[2] != 1:
                    self.will_do_available(2)
                else:
                    print("当前进程已完成，不可再分配资源")
            elif n == 'p4':
                if self.finish[3] != 1:
                    self.will_do_available(3)
                else:
                    print("当前进程已完成，不可再分配资源")
            elif n == 'p5':
                if self.finish[4] != 1:
                    self.will_do_available(4)
                else:
                    print("当前进程已完成，不可再分配资源")
            else:
                print("输入有误,退出程序.")
                break


bank = Bank()
bank.print_all_info()
bank.user_input()
