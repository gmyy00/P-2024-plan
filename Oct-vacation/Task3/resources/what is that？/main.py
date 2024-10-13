import re
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtCore
from calc_ui import Ui_calculator


class Calculator:
    def __init__(self):
        self.Precedence = {"+": 1, "-": 1, "×": 2, "÷": 2, "^": 3}
        self.expression = ""
        self.tokens = []
        self.number_stack = []
        self.operator_stack = []
        self.addition = lambda a, b: a + b
        self.subtraction = lambda a, b: a - b
        self.multiplication = lambda a, b: a * b
        self.division = lambda a, b: a / b
        self.power = lambda a, b: a ** b

    def apply_operator(self, operator, first, second):
        match operator:
            case '+':
                return self.addition(second, first)
            case '-':
                return self.subtraction(second, first)
            case '×':
                return self.multiplication(second, first)
            case '÷':
                return self.division(second, first)
            case '^':
                return self.power(second, first)

    def greater_precedence(self, op1, op2):
        return self.Precedence[op1] >= self.Precedence[op2]

    def evaluate(self):
        while len(self.operator_stack) > 0:
            first = self.number_stack.pop()
            second = self.number_stack.pop()
            operator = self.operator_stack.pop()
            self.number_stack.append(self.apply_operator(operator, first, second))
        return self.number_stack.pop()

    def token_operate(self):
        # 正则没加配对负号的部分，把负号看成计算符号
        # 前面加个0来保证是完整的表达式
        if self.expression[0] in '+-':
            self.expression = '0' + self.expression
        self.tokens = re.findall(r'(\d+\.\d*|\d+|[+\-×÷^])', self.expression)
        for token in self.tokens:
            # 把tokens里面的str数字转化为float
            try:
                token = float(token)
            except ValueError:
                pass
            if isinstance(token, float):
                self.number_stack.append(token)
            elif token in self.Precedence:
                while (len(self.operator_stack) > 0
                       and self.greater_precedence(self.operator_stack[len(self.operator_stack) - 1], token)):
                    self.number_stack.append(
                        self.apply_operator(
                            self.operator_stack.pop(),
                            self.number_stack.pop(),
                            self.number_stack.pop(),
                        )
                    )
                self.operator_stack.append(token)

    def run(self, expression):
        self.expression = expression
        self.token_operate()
        return self.evaluate()


class MainWindow(QMainWindow, Calculator):
    def __init__(self):
        super().__init__()
        # 创建ui类并设置ui
        self.ui = Ui_calculator()
        self.ui.setupUi(self)
        # 绑定按钮
        self.ui.pushButton_0.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_0))
        self.ui.pushButton_1.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_1))
        self.ui.pushButton_2.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_2))
        self.ui.pushButton_3.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_3))
        self.ui.pushButton_4.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_4))
        self.ui.pushButton_5.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_5))
        self.ui.pushButton_6.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_6))
        self.ui.pushButton_7.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_7))
        self.ui.pushButton_8.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_8))
        self.ui.pushButton_9.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_9))
        self.ui.pushButton_point.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_point))
        self.ui.pushButton_ac.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_ac))
        self.ui.pushButton_addition.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_addition))
        self.ui.pushButton_subtraction.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_subtraction))
        self.ui.pushButton_multiplication.clicked.connect(
            lambda: self.expression_edit(self.ui.pushButton_multiplication))
        self.ui.pushButton_division.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_division))
        self.ui.pushButton_power.clicked.connect(lambda: self.expression_edit(self.ui.pushButton_power))
        self.ui.pushButton_ac.clicked.connect(self.ac)
        self.ui.pushButton_equal_to.clicked.connect(self.calculate)
        self.calculate0 = Calculator()
        # 我是历史学家，这就是史☝️🤓

    def expression_edit(self, button):
        # 每点击按钮，就在expression后面添加字符
        button_text = button.text()
        self.expression = self.expression + button_text
        # 刷新label
        _translate = QtCore.QCoreApplication.translate
        self.ui.label_2.setText(_translate("calculator", f"{self.expression}"))

    def ac(self):
        # 清除表达式
        _translate = QtCore.QCoreApplication.translate
        self.expression = ''
        # 刷新label
        self.ui.label_2.setText(_translate("calculator", "Waiting..."))
        self.ui.label.setText(_translate("calculator", "Waiting..."))

    def calculate(self):
        # 计算
        result = self.calculate0.run(self.expression.strip())
        # 刷新label
        _translate = QtCore.QCoreApplication.translate
        self.ui.label.setText(_translate("calculator", f"{result}"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

# back和括号的部分还没做🫡，还有一堆bug没修😨
# 注释和js那里的差不多，可以看那里
