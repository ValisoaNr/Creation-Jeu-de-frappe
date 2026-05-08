#!/bin/bash

rouge="\033[31m"
bleu="\033[34m"
vert="\033[32m"
neutre="\033[0m"

clear
echo -e "${bleu}"
cat jeuDEfrappe.ascii
echo -e "${neutre}"

echo -e "\tBIENVENUE DANS LE JEU ! \n\n --> apprennez votre en jouant ce jeu ;\n"
echo -e "${vert}"
read -sp "Entrez pour continuer ..."
echo -e "${neutre}"
echo -e "\n"
