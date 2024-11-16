# 学生管理系统
import json

# PS: 可以仅以 “姓名” / “学号” 来代指学生信息
# example:
# 姓名：帅otto       学号：20241111     学院：哇奥！      成绩：哈里路

class StuSystem:
    def __init__(self):
        self.case = "main"
        self.STU_FILE = "student_file.json"
        self.STU_LIST = {}
        self.First_Level_Menu = ["add"]
        self.Second_Level_Menu = ["sel", "del", "mod"]

    def stu_init(self):
        """此函数用于, 从文件中, 初始化学生信息"""
        with open(self.STU_FILE, 'r', encoding='utf-8') as f:
            if f.read(1):
                f.seek(0, 0)
                self.STU_LIST = json.load(f)

    def menu(self):
        """此函数用于, 在命令行里, 打印出菜单"""
        match self.case:
            case "main":
                print("\n学生管理系统 ver0.0.1\n"
                      "1：查询学生信息\n"
                      "2：修改学生信息\n"
                      "3：添加学生信息\n"
                      "4：删除学生信息\n"
                      "0：保存并退出\n"
                      "请输入相应数字来进行您希望进行的操作：")
            case "sel":
                print("1：查询全部学生\n"
                      "2：查询一位学生\n"
                      "3：取消\n"
                      "请输入相应数字来进行您希望进行的操作：")
            case "mod":
                print("1：修改学生姓名\n"
                      "2：修改学生学号\n"
                      "3：修改学生学院\n"
                      "4：修改学生成绩\n"
                      "5：取消\n"
                      "请输入相应数字来进行您希望进行的操作：")
            case "del":
                print("1：删除此学生\n"
                      "2：删除学生姓名\n"
                      "3：删除学生学号\n"
                      "4：删除学生学院\n"
                      "5：删除学生成绩\n"
                      "6：取消\n"
                      "请输入相应数字来进行您希望进行的操作：")
            case "add":
                pass

    def get_choice(self) -> int:
        """此函数用于, 在命令行里, 获取用户输入的选项"""
        while 1:
            a = input()
            try:
                int(a)
            except (TypeError, ValueError):
                print("请输入正确的数字！")
            else:
                break
        return int(a)

    def exec(self, user_choice):
        """此函数用于, 根据用户输入的选项, 执行相应的功能"""
        match self.case:
            case "main":
                match user_choice:
                    case 1:
                        self.case = "sel"
                        # self.menu()
                    case 2:
                        self.case = "mod"
                        # self.menu()
                    case 3:
                        self.case = "add"
                        # self.menu()
                    case 4:
                        self.case = "del"
                        # self.menu()
                    case 0:
                        self.stu_save()
                    case _:
                        print("未知操作！")
                        return
            case "sel":
                self.stu_sel(user_choice)
            case "mod":
                self.stu_mod(user_choice)
            case "add":
                self.stu_add()
            case "del":
                self.stu_del(user_choice)

    def stu_add(self):
        """此函数用于, 添加学生信息"""
        name = input("姓名：")
        id = input("学号：")
        college = input("学院：")
        score = input("分数：")
        self.STU_LIST[id + name] = [name, id, college, score]
        print("添加成功！")
        self.case = "main"

    def stu_del(self, user_choice):
        """此函数用于, 删除学生信息"""
        keyword = input("请输入学生姓名或学号:")
        for k in list(self.STU_LIST.keys()):
            if keyword in k:
                match user_choice:
                    case 1:
                        del self.STU_LIST[k]
                        self.case = "main"
                        print("删除成功！")
                        return
                    case 2 | 3 | 4 | 5:
                        self.STU_LIST[k][user_choice - 2] = "无"
                        self.case = "main"
                        print("删除成功！")
                        return
                    case 6:
                        self.case = "main"
                        print("删除成功！")
                        return
                    case _:
                        print("未知操作！")
                        self.case = "del"
                        return
        print("未找到此学生！")
        self.case = "main"

    def stu_mod(self, user_choice):
        """此函数用于, 修改学生信息"""
        if user_choice == 5:
            self.case = "main"
            return
        keyword = input("请输入要进行修改的学生姓名或学号:")
        for k in list(self.STU_LIST.keys()):
            if keyword in k:
                match user_choice:
                    case 1:
                        name = input("姓名：")
                        self.STU_LIST[k][0] = name
                        id = self.STU_LIST[k][1]
                        self.STU_LIST[str(id) + name] = self.STU_LIST[k]
                        del self.STU_LIST[k]
                        self.case = "main"
                        print("修改成功！")
                        return
                    case 2:
                        id = input("学号：")
                        self.STU_LIST[k][1] = id
                        name = self.STU_LIST[k][0]
                        self.STU_LIST[str(id) + name] = self.STU_LIST[k]
                        del self.STU_LIST[k]
                        self.case = "main"
                        print("修改成功！")
                        return
                    case 3:
                        self.STU_LIST[k][2] = input("学院：")
                        self.case = "main"
                        print("修改成功！")
                        return
                    case 4:
                        self.STU_LIST[k][3] = input("分数：")
                        self.case = "main"
                        print("修改成功！")
                        return
                    case _:
                        print("未知操作！")
                        self.case = "mod"
                        return
        print("未找到此学生！")
        self.case = "main"

    def stu_sel(self, user_choice):
        """此函数用于, 查询学生信息"""
        match user_choice:
            case 1:
                if self.STU_LIST:
                    for keyword in list(self.STU_LIST.keys()):
                        print(f"姓名：{self.STU_LIST[keyword][0]}\t"
                              f"学号：{self.STU_LIST[keyword][1]}\t"
                              f"学院：{self.STU_LIST[keyword][2]}\t"
                              f"成绩：{self.STU_LIST[keyword][3]}\t")
                    self.case = "main"
                    return
                else:
                    print("暂无数据！")
                    self.case = "main"
                    return
            case 2:
                keyword = input("请输入学生姓名或学号:")
                for k in list(self.STU_LIST.keys()):
                    if keyword in k:
                        print(f"姓名：{self.STU_LIST[k][0]}\t"
                              f"学号：{self.STU_LIST[k][1]}\t"
                              f"学院：{self.STU_LIST[k][2]}\t"
                              f"成绩：{self.STU_LIST[k][3]}\t")
                        self.case = "main"
                        return
                print("未找到此学生！\n")
                self.case = "main"
            case 3:
                self.case = "main"
            case _:
                print("未知操作！")
                self.case = "sel"

    def stu_save(self):
        """此函数用于, 将学生信息保存到文件中"""
        with open(self.STU_FILE, 'w+', encoding='utf-8') as f:
            json.dump(self.STU_LIST, f, ensure_ascii=False)
            f.seek(0, 0)
            if f.read(1):
                print("保存成功！")


def main():
    """尽量不要修改此函数的代码, 此函数用于全局调用"""
    """Do not edit this code unless you know what you are doing"""

    stu_system0 = StuSystem()
    stu_system0.stu_init()

    stu_system0.menu()
    user_choice = stu_system0.get_choice()
    stu_system0.exec(user_choice)

    while user_choice != 0:
        stu_system0.menu()
        if stu_system0.case not in stu_system0.First_Level_Menu:
            user_choice = stu_system0.get_choice()
        stu_system0.exec(user_choice)


if __name__ == '__main__':
    main()
