#! /usr/bin/env python

try:
    import tkinter as tk
    from tkinter import ttk

except ImportError:
    # Python 2
    import Tkinter as tk
    import ttk

import parser
import base64
from icons import icon_string
import RPi.GPIO as GPIO
import sys
from mfrc522 import SimpleMFRC522
import requests


class TkGUI(tk.Tk):
    FONT_LARGE = ("Calibri", 12)  	# selects the font of the text inside buttons
    FONT_MED = ("Calibri", 10)
    WIDTH = ('3')
    HEIGHT = ('2')
    BD = ('0')

    # Max rows and columns in the GUI
    MAX_ROW = 5
    MAX_COLUMN = 5
    i = 0
    NEW_OPERATION = False
    VISOR_DISPLAY = False
    CONTA1 = ''
    CONTA2 = ''
    NUMBER = 0

    def __init__(self):
        try:
            super(TkGUI, self).__init__()
        except TypeError:
            # Python 2
            tk.Tk.__init__(self)

        self.title('Calculator')
        self.resizable(width=False, height=False)

        # Configure default theme
        style = ttk.Style(self)
        style.theme_use('clam')
        self.configure(bg='#FFFFFF', highlightthickness='0')

        # Configure icon
        icon_data = base64.b64decode(icon_string)
        self.icon = tk.PhotoImage(data=icon_data)
        self.tk.call('wm', 'iconphoto', self._w, self.icon)

        for row in range(self.MAX_ROW):
            self.columnconfigure(row,pad=0)

        for column in range(self.MAX_COLUMN):
            self.rowconfigure(column,pad=0)

        self.visor = tk.Text(self, font=self.FONT_LARGE, width=35, height='5', bd=0, highlightthickness=0)
        self.visor.grid(row=1, columnspan=6)
        self.display = tk.Entry(self, font=("Calibri", 40), relief='flat', bd='0', width='10', selectbackground='#FFFFFF', justify='right', highlightthickness=0)
        self.display.grid(row=2, columnspan=6, sticky=tk.W + tk.E)

        self._init_ui()
#comment
    def _init_ui(self):
        one = tk.Button(
            self, text="1", command=lambda: self.get_variables(1), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        one.grid(row=3, column=0)
        two = tk.Button(
            self, text="2", command=lambda: self.get_variables(2), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        two.grid(row=3, column=1)
        three = tk.Button(
            self, text="3", command=lambda: self.get_variables(3), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        three.grid(row=3, column=2)

        four = tk.Button(
            self, text="4", command=lambda: self.get_variables(4), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        four.grid(row=4, column=0)
        five = tk.Button(
            self, text="5", command=lambda: self.get_variables(5), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        five.grid(row=4, column=1)
        six = tk.Button(
            self, text="6", command=lambda: self.get_variables(6), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        six.grid(row=4, column=2)

        seven = tk.Button(
            self, text="7", command=lambda: self.get_variables(7), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        seven.grid(row=5, column=0)
        eight = tk.Button(
            self, text="8", command=lambda: self.get_variables(8), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        eight.grid(row=5, column=1)
        nine = tk.Button(
            self, text="9", command=lambda: self.get_variables(9), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        nine.grid(row=5, column=2)

        cls = tk.Button(self, text="AC", command=self.clear_all, font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        cls.grid(row=6, column=0)
        zero = tk.Button(
            self, text="0", command=lambda: self.get_variables(0), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        zero.grid(row=6, column=1)
        result = tk.Button(self, text="=", command=self.calculate, font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        result.grid(row=6, column=2)

        plus = tk.Button(self, text="Transfer", command=lambda: self.credit(self.display.get()), font=self.FONT_MED, width='6', height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        plus.grid(row=3, column=3)
        minus = tk.Button(self, text="Titulos", command=lambda: self.get_operation("-"), font=self.FONT_MED, width='6', height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        minus.grid(row=4, column=3)
        multiply = tk.Button(
            self, text="*", command=lambda: self.get_operation("Hipoteca"), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        multiply.grid(row=5, column=3)
        divide = tk.Button(
            self, text="Confirm", command=lambda:  self.confirm(), font=self.FONT_LARGE, width=self.WIDTH, height=self.HEIGHT, bd=self.BD, fg='#000000', bg='#FFFFFF', activebackground='#e6f3ff')
        divide.grid(row=6, column=3)

        # adding new operations
        pi = tk.Button(self, text="pi", command=lambda: self.get_operation("*3.14"), font=self.FONT_LARGE)
        pi.grid(row=3, column=4)
        modulo = tk.Button(self, text="%", command=lambda:  self.get_operation("*"), font=self.FONT_LARGE)
        modulo.grid(row=4, column=4)
        left_bracket = tk.Button(self, text="(", command=lambda: self.get_operation("("), font=self.FONT_LARGE)
        left_bracket.grid(row=5, column=4)
        exp = tk.Button(self, text="exp", command=lambda: self.get_operation("**"), font=self.FONT_MED)
        exp.grid(row=6, column=4)

        # To be added :
        # sin, cos, log, ln
        undo_button = tk.Button(self, text="<-", command=self.undo, font=self.FONT_LARGE, foreground="red")
        undo_button.grid(row=3, column=5)
        fact = tk.Button(self, text="x!", command=lambda: self.factorial("!"), font=self.FONT_LARGE)
        fact.grid(row=4, column=5)
        right_bracket = tk.Button(self, text=")", command=lambda: self.get_operation(")"), font=self.FONT_LARGE)
        right_bracket.grid(row=5, column=5)
        square = tk.Button(self, text="^2", command=lambda: self.get_operation("**2"), font=self.FONT_MED)
        square.grid(row=6, column=5)


    def read_card(self):
        reader = SimpleMFRC522()
        id, text = reader.read()
        return id

    def confirm(self):
        update_account=self.CONTA1
        dest_account=self.CONTA2
        API_ENDPOINT = "http://34.95.207.226/api/transaction/"
        if dest_account != update_account:
            data = {'transaction': 'W', 'update_account': update_account, 'dest_account': dest_account, 'value': self.NUMBER}
            r = requests.post(url=API_ENDPOINT, data=data)
            if r.status_code == 201:
                self.CONTA1 = ''
                self.CONTA2 = ''
                self.NUMBER = 0
                self.print_visor("Transferencia efetuada!")
            else:
                self.CONTA1 = ''
                self.CONTA2 = ''
                self.NUMBER = 0
                self.print_visor("Nao foi possivel transferir")
        else:
            self.CONTA1 = ''
            self.CONTA2 = ''
            self.NUMBER = 0
            self.print_visor("Nao foi possivel transferir")


    def print_visor(self, msg):
        numlines = self.visor.index('end - 1 line').split('.')[0]
        if numlines == 5:
            self.visor.delete(1.0, 2.0)
        if self.visor.index('end-1c') != '1.0':
            self.visor.insert('end', '\n')
        self.visor.insert('end', msg)

    def credit(self, value):
        if self.display.get():
            self.visor.delete('1.0', '2.0')
            self.NUMBER = int(self.display.get())
            if self.CONTA1 != '':
                self.print_visor("Cartao 2 lido")
                self.CONTA2 = self.read_card()
                self.print_visor(self.CONTA2)
            else:
                self.print_visor("Cartao 1 lido, passe o segundo")
                self.CONTA1 = self.read_card()
                self.print_visor(self.CONTA1)
        else:
            self.visor.delete('1.0', '2.0')
            self.visor.insert('1.0', 'Insira o valor')

    def factorial(self, operator):
        """Calculates the factorial of the number entered."""
        number = int(self.display.get())
        fact = 1
        try:
            while number > 0:
                fact = fact*number
                number -= 1
            self.clear_all()
            self.display.insert(0, fact)
        except Exception:
            self.clear_all()
            self.display.insert(0, "Error")

    def clear_all(self, new_operation=True):
        """clears all the content in the Entry widget."""
        self.visor.delete('1.0', '2.0')
        self.display.delete(0, tk.END)
        self.NEW_OPERATION = new_operation

    def get_variables(self, num):
        """Gets the user input for operands and puts it inside the entry widget.

        If a new operation is being carried out, then the display is cleared.
        """
        if self.display.get() == 'Insira o valor':
            self.clear_all(new_operation=False)
        elif self.NEW_OPERATION:
            self.clear_all(new_operation=False)
        self.display.insert(self.i, num)
        self.i += 1

    def get_operation(self, operator):
        """Gets the operand the user wants to apply on the functions."""
        length = len(operator)
        self.display.insert(self.i, operator)
        self.i += length

    def undo(self):
        """removes the last entered operator/variable from entry widget."""
        whole_string = self.display.get()
        if len(whole_string):        ## repeats until
            ## now just decrement the string by one index
            new_string = whole_string[:-1]
            self.clear_all(new_operation=False)
            self.display.insert(0, new_string)
        else:
            self.clear_all()
            self.display.insert(0, "Error, press AC")

    def calculate(self):
        """Evaluates the expression.

        ref : http://stackoverflow.com/questions/594266/equation-parsing-in-python
        """
        whole_string = self.display.get()
        try:
            formulae = parser.expr(whole_string).compile()
            result = eval(formulae)
            self.clear_all()
            self.display.insert(0, result)
        except Exception:
            self.clear_all()
            self.display.insert(0, "Error!")
            GPIO.cleanup()

    def run(self):
        """Initiate event loop."""
        self.mainloop()
