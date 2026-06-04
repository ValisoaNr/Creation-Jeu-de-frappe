#include "Jeudefrappe.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Jeudefrappe w;
    w.show();
    return QCoreApplication::exec();
}
