#ifndef JEUDEFRAPPE_H
#define JEUDEFRAPPE_H

#include <QMainWindow>
#include <QTimer>
#include <QStringList>

QT_BEGIN_NAMESPACE
namespace Ui
{
    class Jeudefrappe;
}
QT_END_NAMESPACE

class Jeudefrappe : public QMainWindow
{
    Q_OBJECT

public:
    explicit Jeudefrappe(QWidget *parent = nullptr);
    ~Jeudefrappe();

private slots:
    void demarrer();
    void editer(const QString &text);
    void temps();

private:
    Ui::Jeudefrappe *ui;
    QTimer *tempsJeu;
    QStringList dictionaire;
    QString motC;
    int score , max , tempRst , motRst , total , correcte;

    void chargeMot();
    QString genererMot();
    void afficheResultat();
};

#endif