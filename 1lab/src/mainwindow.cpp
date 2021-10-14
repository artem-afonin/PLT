#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->comboBox_direction->addItem("Левостороннее");
    ui->comboBox_direction->addItem("Правостороннее");
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_button_start_clicked()
{
    if (false == parse_nonTerminal())
        return;

    if (false == parse_Terminal())
        return;

    if (false == check_Reply())
        return;

    if (false == parse_Rules())
        return;

    if (false == parse_Start())
        return;

    if (false == check_Rules())
        return;

    if (listOutput.count() != 0)
    {
        listOutput.clear();
    }

    if (false == check_Direction())
        return;

    generation_chains();
}

bool MainWindow::check_Direction()
{
    if (ui->comboBox_direction->currentIndex() == 0)
    {
        intDirection = 0;
    }
    else if (ui->comboBox_direction->currentIndex() == 1)
    {
        intDirection = 1;
    }
    else
    {
        return false;
    }

    return true;
}

void MainWindow::create_StartCheckBox()
{
    ui->comboBox_start->clear();

    foreach (QString str, nonTerminal) {
        ui->comboBox_start->addItem(str);
    }
}

void MainWindow::generation_chains()
{
    QStringList currentRow = dictRules[strStart];

    foreach (QString str, currentRow) {
        queueRules.enqueue(str);
    }

    QStringList listAllVariants = QStringList();

    while (queueRules.count() > 0)
    {
        QString strCurrentRule = queueRules.dequeue();
        if (true == check_OnlyTerminal(strCurrentRule))
        {
            if (strCurrentRule.length() > 0 && strCurrentRule.length() <= maxLenght &&
                    !listOutput.contains(strCurrentRule))
            {
                listOutput.append(strCurrentRule);
                ui->textBrowser_output->append(strCurrentRule);
            }
            continue;
        }

        QStringList nonTermRules;
        int firstPos;

        if (0 == intDirection)
        {
            firstPos = maxLenght;
            foreach (QString nonTerm, nonTerminal) {
                if (strCurrentRule.indexOf(nonTerm) < firstPos &&
                        strCurrentRule.indexOf(nonTerm) != -1)
                {
                    firstPos = strCurrentRule.indexOf(nonTerm);
                    nonTermRules = dictRules[nonTerm];
                }
            }
        }
        else
        {
            firstPos = -1;
            foreach (QString nonTerm, nonTerminal) {
                if (strCurrentRule.lastIndexOf(nonTerm) > firstPos &&
                        strCurrentRule.lastIndexOf(nonTerm) != -1)
                {
                    firstPos = strCurrentRule.lastIndexOf(nonTerm);
                    nonTermRules = dictRules[nonTerm];
                }
            }
        }

        foreach(QString nonTermRule, nonTermRules)
        {
            QString tempCurrentRule = strCurrentRule;
            QString strToPush = tempCurrentRule.remove(firstPos, 1).insert(firstPos, nonTermRule);
            if (strToPush.length() <= maxLenght && !listAllVariants.contains(strToPush))
            {
                listAllVariants.append(strToPush);
                queueRules.enqueue(strToPush);
            }
        }
    }
    ui->textBrowser_output->clear();
    foreach (QString str, listOutput) {
        ui->textBrowser_output->append(str);
    }
}

bool MainWindow::check_OnlyTerminal(QString str)
{
    foreach (QString nonTerm, nonTerminal) {
        if (str.contains(nonTerm))
        {
            return false;
        }
    }
    return true;
}

bool MainWindow::check_Rules()
{
    QMap<QString, QStringList>::const_iterator i = dictRules.constBegin();
    while (i != dictRules.constEnd())
    {
        foreach (QString strRule, i.value())
        {
            QString tempRule = strRule;
            foreach (QString nonTerm, nonTerminal) {
                tempRule = tempRule.replace(nonTerm, "");
            }
            foreach (QString term, terminal) {
                tempRule = tempRule.replace(term, "");
            }
            if (false == tempRule.isEmpty())
            {
                QMessageBox::warning(this, "Error", "The rule contains an invalid character!");
                return false;
            }
        }
        i++;
    }

    return true;
}

bool MainWindow::parse_Length()
{
    int tempMaxLenght = ui->textEdit_length->toPlainText().toInt();
    if (tempMaxLenght > 0)
    {
        maxLenght = tempMaxLenght;
        return true;
    } else {
        return false;
    }
}

bool MainWindow::parse_Start()
{
    if (0 == nonTerminal.count())
    {
        return false;
    }
    strStart = ui->comboBox_start->currentText();
    return true;
}

bool MainWindow::parse_Rules()
{
    if (terminal.count() < 0 || nonTerminal.count() < 0)
    {
        return false;
    }

    if (ui->plainTextEdit_rules->toPlainText().length() == 0)
    {
        return false;
    }

    dictRules.clear();
    QStringList listRules = QStringList();
    listRules = ui->plainTextEdit_rules->toPlainText().split("\n");
    foreach (QString str, listRules) {
        QStringList listParam = QStringList();
        listParam = str.split("->");
        QString strGoal = listParam[0];
        QString strVariants = listParam[1];
        QStringList listVariants = QStringList();
        listVariants = strVariants.split("|");
        dictRules.insert(strGoal,listVariants);
    }

    return true;
}

bool MainWindow::check_Reply()
{
    if (nonTerminal.length() > 0 && terminal.length() > 0)
    {
        foreach (QString nonTermStr, nonTerminal)
        {
            foreach (QString termStr, terminal)
            {
                if (nonTermStr == termStr)
                {
                    QMessageBox::warning(this, "Error", "The alphabets have the same character!");
                    return false;
                }
            }
        }
    } else {
        return false;
    }
    return true;
}

bool MainWindow::parse_Terminal()
{
    if (terminal.length() > 0)
    {
        terminal.clear();
    }

    if (ui->textEdit_Terminal->toPlainText().length() == 0)
    {
        return false;
    }

    terminal = ui->textEdit_Terminal->toPlainText().split(",");

    if (terminal.length() <= 0)
    {
        return false;
    }

    return true;
}

bool MainWindow::parse_nonTerminal()
{
    if (nonTerminal.length() > 0)
    {
        nonTerminal.clear();
    }

    if (ui->textEdit_nonTerminal->toPlainText().length() == 0)
    {
        return false;
    }

    nonTerminal = ui->textEdit_nonTerminal->toPlainText().split(",");

    if (nonTerminal.length() <= 0)
    {
        return false;
    }

    return true;
}


void MainWindow::on_textEdit_nonTerminal_textChanged()
{
    if (false == parse_nonTerminal())
        return;
    create_StartCheckBox();
}

void MainWindow::on_textEdit_length_textChanged()
{
    if (false == parse_Length())
        return;
}

void MainWindow::on_pushButton_grammar_clicked()
{
    ui->textEdit_Terminal->setText("q,w,c,d");
    ui->textEdit_nonTerminal->setText("A,B");
    ui->comboBox_start->clear();
    ui->comboBox_start->addItem("A");
    ui->comboBox_start->addItem("B");
    ui->plainTextEdit_rules->clear();
    ui->plainTextEdit_rules->appendPlainText("A->BAw|d");
    ui->plainTextEdit_rules->appendPlainText("B->ABq|c");
    ui->textEdit_length->setText("10");
}
