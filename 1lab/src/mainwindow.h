#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTextEdit>
#include <QMessageBox>
#include <QMap>
#include <QQueue>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_button_start_clicked();

    void on_textEdit_nonTerminal_textChanged();

    void on_textEdit_length_textChanged();

    void on_pushButton_grammar_clicked();

private:
    Ui::MainWindow *ui;

    QStringList nonTerminal = QStringList();
//    QStringList nonTerminal ={"A", "B"};
    QStringList terminal = QStringList();
//    QStringList terminal = {"c", "d"};
    QMap<QString, QStringList> dictRules;
    QString strStart;
    QStringList listOutput;
    QQueue<QString> queueRules;
    int maxLenght = 0;
    int intDirection;

    bool parse_nonTerminal();
    bool parse_Terminal();
    bool check_Reply();
    bool parse_Rules();
    bool parse_Start();
    bool check_Rules();
    bool check_OnlyTerminal(QString);
    void generation_chains();
    bool parse_Length();
    void create_StartCheckBox();
    bool check_Direction();
};
#endif // MAINWINDOW_H
