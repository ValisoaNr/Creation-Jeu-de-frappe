#include "Jeudefrappe.h"
#include "ui_Jeudefrappe.h"
#include <fstream>
#include <QRandomGenerator>
#include <QMessageBox>

using namespace std;

Jeudefrappe::Jeudefrappe(QWidget *parent)
: QMainWindow(parent) , ui(new Ui::Jeudefrappe)
{
    ui->setupUi(this);
    tempsJeu = new QTimer(this);
    score = 0;
    tempRst = 0 ;
    total = 0;
    correcte = 0;
    motRst = 0;
    max = 15;
    motC = "";
    chargeMot();

    connect(ui->demarrer , &QPushButton::clicked , this , &Jeudefrappe::demarrer);
    connect(ui->entre , &QLineEdit::textChanged , this , &Jeudefrappe::editer);
    connect(tempsJeu , &QTimer::timeout , this , &Jeudefrappe::temps);
}
Jeudefrappe::~Jeudefrappe()
{
    delete ui;
}
void Jeudefrappe::chargeMot()
{
    ifstream file;
    string line;

    file.open("../exemple.lettre");

    if(file)
    {
        while(getline(file , line))
        {
            dictionaire.append(QString::fromStdString(line).trimmed());
        }
        file.close();
    }
    else
    {
        dictionaire << "chat" << "chien" << "maison" << "arbre" << "soleil" << "lune" << "oiseau" << "fleur" << "table" << "chaise" << "livre" << "crayon" << "porte" << "fenetre" << "escalier";
    }
}
QString Jeudefrappe::genererMot()
{
    int mode , indexe , nombre , choix;

    mode = ui->mode->currentIndex();
    if(mode == 0)
    {
        if(!dictionaire.isEmpty())
        {
            indexe = QRandomGenerator::global()->bounded(dictionaire.size());
            return dictionaire.at(indexe);
        }
        return "mot";
    }
    else if(mode == 1)
    {
        nombre = QRandomGenerator::global()->bounded(1 , 32768);
        return QString::number(nombre);
    }
    else
    {
        choix = QRandomGenerator::global()->bounded(2);
        if((choix == 0) && (!dictionaire.isEmpty()))
        {
            indexe = QRandomGenerator::global()->bounded(dictionaire.size());
            return dictionaire.at(indexe);
        }
        nombre = QRandomGenerator::global()->bounded(1 , 32768);
        return QString::number(nombre);
    }
}
void Jeudefrappe::demarrer()
{
    int difficulite ;

    difficulite = ui->dificulite->currentIndex();
    score = 0;
    total = 0;
    correcte = 0;
    motRst = 10;

    if(difficulite == 0)
    {
        max = 150;
    }
    else if(difficulite == 1)
    {
        max = 100;
    }
    else
    {
        max = 50;
    }

    tempRst = max;
    ui->entre->setEnabled(true);
    ui->entre->clear();
    ui->entre->setFocus();
    ui->demarrer->setEnabled(false);
    ui->dificulite->setEnabled(false);
    ui->mode->setEnabled(false);

    motC = genererMot();
    ui->mot->setText(motC);
    ui->score->setText("Score : 0/10");
    ui->temps->setText(QString("Temps : %1s").arg(tempRst));
    ui->progressBar->setValue(100);

    tempsJeu->start(1000);
}
void Jeudefrappe::editer(const QString &text)
{
    QString entre , lemot;

    entre = text.trimmed();
    lemot = motC.trimmed();
    if((entre == lemot) && (!entre.isEmpty()))
    {
        total++;
        correcte++;
        score++;
        motRst--;

        ui->entre->clear();
        ui->score->setText(QString("Score : %1/10").arg(score));
        if(motRst <= 0)
        {
            tempsJeu->stop();
            afficheResultat();
        }
        else
        {
            motC = genererMot();
            ui->mot->setText(motC);
        }
    }
}
void Jeudefrappe::temps()
{
    int pourcent;

    tempRst--;
    ui->temps->setText(QString("Temps : %1s").arg(tempRst));
    pourcent = (tempRst * 100) / max;
    if(pourcent < 0)
    {
        pourcent = 0;
    }
    ui->progressBar->setValue(pourcent);

    if(tempRst <= 0) {
        tempsJeu->stop();
        afficheResultat();
    }
}
void Jeudefrappe::afficheResultat()
{
    int moyenne;
    QString message;

    ui->entre->setEnabled(false);
    ui->demarrer->setEnabled(true);
    ui->dificulite->setEnabled(true);
    ui->mode->setEnabled(true);

    moyenne = 0;
    if(total > 0)
    {
        moyenne = (correcte * 100) / total;
    }
    ui->moyenne->setText(QString("Précision : %1%").arg(moyenne));
    message = QString("Partie terminé ! \n Score : %1/10 \n Tentatives : %2 \n Précision : %3%").arg(score).arg(total).arg(moyenne);
    QMessageBox::information(this , "Fin de la partie" , message);
}