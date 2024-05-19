import sys

import sympy
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from sympy.parsing.sympy_parser import parse_expr


class KolcoWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/kolco.ui", self)
        self.setWindowTitle("Модель кольца")
        self.parent = parent  # атрибут с родительским классом

        self.objects = {
            "σ": self.sigma_var,
            "m": self.m_var,
            "l": self.l_var,
            "Fпн": self.Fpn_var,
            "Fтяж": self.Ft_var,
            "F": self.F_var,
            "lвнутр": self.lvnutr_var,
            "Rвнутр": self.Rvnutr_var,
            "dвнутр": self.dvnutr_var,
            "lвнеш": self.lvnesh_var,
            "Rвнеш": self.Rvnesh_var,
            "dвнеш": self.dvnesh_var,
        }  # Объекты текстовых полей по символам
        self.check_value = {
            "σ": [["Fпн", "l"], "Fpn/l"],
            "m": [["Fтяж"], "Ft/g"],
            "l": [["lвнутр", "lвнеш"], "lvnutr+lvnesh"],
            "Fпн": [["σ", "l"], "sigma*l"],
            "Fтяж": [["m"], "m*g"],
            "F": [["Fпн", "Fтяж"], "Fpn+Ft"],
            "lвнутр": [["Rвнутр"], "2*Pi*Rvnutr"],
            "Rвнутр": [["dвнутр"], "dvnutr/2"],
            "dвнутр": [["Rвнутр"], "Rvnutr*2"],
            "lвнеш": [["Rвнеш"], "2*Pi*Rvnesh"],
            "Rвнеш": [["dвнеш"], "dvnesh/2"],
            "dвнеш": [["Rвнеш"], "Rvnesh*2"],
        }  # Необходимые для вычисления значения и формула

        self.initUi()

    def initUi(self):
        self.calculate_btn.clicked.connect(self.calculate)

    def calculate(self):
        calc_value = self.find.currentText()  # Вычисляемое значение

        for value in self.check_value[calc_value][0]:
            object_text = self.objects[value].toPlainText()
            # Проверяется, указаны ли необходимые значения для вычисления
            if object_text == "":
                self.statusBar().showMessage(
                    f"Сначала вычислите: {value}!", self.parent.stbar_msecs
                )
                return
            # Проверяется, что указанные значения - числа
            try:
                float(object_text)
            except ValueError:
                self.statusBar().showMessage(
                    "Значения - только числа!", self.parent.stbar_msecs
                )
                return

        # expr - объект формулы
        expr = parse_expr(self.check_value[calc_value][1])
        # Далее создаются объекты символов в формуле
        (
            sigma,
            m,
            l,
            Fpn,
            Ft,
            F,
            lvnutr,
            Rvnutr,
            dvnutr,
            lvnesh,
            Rvnesh,
            dvnesh,
            Pi,
            g,
        ) = sympy.symbols(
            "sigma m l Fpn Ft F lvnutr Rvnutr dvnutr lvnesh Rvnesh dvnesh Pi g"
        )
        # val - результат вычислений по формуле
        val = float(
            expr.evalf(
                subs={
                    sigma: self.sigma_var.toPlainText(),
                    m: self.m_var.toPlainText(),
                    l: self.l_var.toPlainText(),
                    Fpn: self.Fpn_var.toPlainText(),
                    Ft: self.Ft_var.toPlainText(),
                    F: self.F_var.toPlainText(),
                    lvnutr: self.lvnutr_var.toPlainText(),
                    Rvnutr: self.Rvnutr_var.toPlainText(),
                    dvnutr: self.dvnutr_var.toPlainText(),
                    lvnesh: self.lvnesh_var.toPlainText(),
                    Rvnesh: self.Rvnesh_var.toPlainText(),
                    dvnesh: self.dvnesh_var.toPlainText(),
                    Pi: self.parent.pi_var,
                    g: self.parent.g_var,
                }
            )
        )
        # Вычисленный результат округляется и выводится пользователю
        self.answer.setText(str(round(val, self.round.value())))
        self.statusBar().showMessage(
            "Ответ успешно вычислен!", self.parent.stbar_msecs
        )


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    from __abstract import SurfaceTension

    app = QApplication(sys.argv)
    parent = SurfaceTension()
    form = KolcoWindow(parent)
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
