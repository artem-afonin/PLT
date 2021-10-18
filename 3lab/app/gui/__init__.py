import os
import re
import sys
from typing import Optional

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from dfa.DFA import DFAGlobalState, DFA
from gui.mainwindow import Ui_MainWindow

script_path = os.path.abspath(sys.argv[0])
script_dir = os.path.dirname(script_path)
resources_dir = os.path.join(script_dir, 'resources')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_gui_data()
        self.connect_button_signals()

        self.dfa: Optional[DFA] = None

    def connect_button_signals(self):
        self.reset_button.clicked.connect(self.reset_button_clicked)
        self.step_button.clicked.connect(self.step_button_clicked)
        self.process_button.clicked.connect(self.process_button_clicked)

    def reset_button_clicked(self):
        self.dfa.reset()
        self.dfa_output_textedit.clear()
        self.error_lineedit.clear()
        self.dfa_state_lineedit.setText(DFAGlobalState.RESET.name)

    def step_button_clicked(self):
        if not self.dfa or self.dfa.get_global_state() == DFAGlobalState.RESET:
            self.start_dfa()
        elif self.dfa.get_global_state() == DFAGlobalState.HALT:
            if self.dfa.get_logging_list().has_error():
                QMessageBox.about(self, 'error', 'Can not make step while DFA halted! Reset required!')
                return
            else:
                QMessageBox.about(self, 'success', 'This line belongs to DFA grammar')
                return
        self.dfa.step()
        self.after_dfa_step()

    def process_button_clicked(self):
        if not self.dfa or self.dfa.get_global_state() == DFAGlobalState.RESET:
            self.start_dfa()
        elif self.dfa.get_global_state() == DFAGlobalState.HALT:
            if self.dfa.get_logging_list().has_error():
                QMessageBox.about(self, 'error', 'Can not make step while DFA halted! Reset required!')
                return
            else:
                QMessageBox.about(self, 'success', 'This line belongs to DFA grammar')
                return

        while self.dfa.get_global_state() != DFAGlobalState.HALT:
            self.dfa.step()
            self.after_dfa_step()

    def after_dfa_step(self):
        self.dfa_state_lineedit.setText(self.dfa.get_global_state().name)

        if self.dfa.get_logging_list().has_error():
            self.error_lineedit.setText(self.dfa.get_logging_list().get_error())

        self.dfa_output_textedit.clear()
        for log in self.dfa.get_logging_list():
            self.dfa_output_textedit.appendPlainText(f'{log.from_state} - {log.symbol} > {log.to_state}')

    def init_gui_data(self):
        self.states_lineedit.setText('A B C')
        self.symbols_lineedit.setText('0 1')
        self.start_state_lineedit.setText('A')
        self.end_states_lineedit.setText('A')
        self.transitions_textedit.setPlainText('A - 0 1 > B\n'
                                               'B - 0 1 > C\n'
                                               'C - 0 > A\n')
        self.dfa_state_lineedit.setText(DFAGlobalState.RESET.name)

    def start_dfa(self):
        states = self.states_lineedit.text().split()
        if '-' in self.states_lineedit.text() or '>' in self.states_lineedit.text():
            QMessageBox.about(self, 'error', 'please remove "-" or ">" from states input')
            return

        symbols = self.symbols_lineedit.text().split()
        if '-' in self.symbols_lineedit.text() or '>' in self.symbols_lineedit.text():
            QMessageBox.about(self, 'error', 'please remove "-" or ">" from symbols input')
            return

        start_state = self.start_state_lineedit.text()
        if '-' in self.start_state_lineedit.text() or '>' in self.start_state_lineedit.text():
            QMessageBox.about(self, 'error', 'please remove "-" or ">" from start states input')
            return

        end_states = self.end_states_lineedit.text().split()
        if '-' in self.end_states_lineedit.text() or '>' in self.end_states_lineedit.text():
            QMessageBox.about(self, 'error', 'please remove "-" or ">" from end states input')
            return

        transitions = []
        for line in self.transitions_textedit.toPlainText().split('\n'):
            if len(line.strip()) == 0:
                continue
            match = re.match(r'([^\s]+)\s*-\s*(.*)\s*>\s*([^\s]+)', line)
            if match:
                from_state = match.group(1)
                symbols_group = match.group(2).split()
                to_state = match.group(3)
                transitions.append({
                    'from': from_state,
                    'symbols': symbols_group,
                    'to': to_state
                })
            else:
                QMessageBox.about(self, 'error', f'wrong transition line format: {line}')
                return

        dfa_dict = {
            'states': states,
            'symbols': symbols,
            'start_state': start_state,
            'end_states': end_states,
            'transitions': transitions
        }

        try:
            self.dfa = DFA(dfa_dict)
        except ValueError as error:
            QMessageBox.about(self, 'error', str(error))

        input_line = self.input_lineedit.text()
        self.dfa.start(input_line)
        self.dfa_state_lineedit.setText(self.dfa.get_global_state().name)


def gui_main(args):
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
