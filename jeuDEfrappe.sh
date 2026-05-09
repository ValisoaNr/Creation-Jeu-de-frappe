#!/bin/bash

# Les couleurs sur terminal bash
rouge="\033[31m"
bleu="\033[34m"
vert="\033[32m"
neutre="\033[0m"
fondBlanc="\033[47m"
fondJaune="\033[43m"
clinote="\033[5m"

# Pour le joueur
Niveau=0
Mode=0
Mot=""

bienvenue()
{
	#affichage d'une message de bienvenue
	clear
	echo -e "${bleu}"
	cat jeuDEfrappe.ascii
	echo -e "${neutre}"

	echo -e "\t\t\tBIENVENUE DANS LE JEU ! \n\n\t\t --> apprennez votre en jouant ce jeu ;\n"
	echo -e "${vert}"
	read -sp "Entrez pour continuer ..."
	echo -e "${neutre}"
	echo -e "\n"
	clear
}
choix_niveau()
{
	# afficher le choix de niveau et attend un seul caractere
	clear
	echo -e "${vert}\t\tVEUILLEZ CHOISIR UN NIVEAU${neutre}\n"
	echo -e "${clinote}${fondJaune}1 - Facile   \n2 - Normal   \n3 - Difficile\n${neutre}"
	read -sn 1 niv
	case "$niv" in
		1|2|3)
			Niveau=$niv
			;;
		*)
			echo -e "${rouge}Appuyer sur 1 ou 2 ou 3 ...${neutre}";
			sleep 0.5
			choix_niveau
			;;
	esac
	clear
}
choix_mode()
{
	# demande le mode ; c'est a dire le caractere à frapper : lettre , chiffre , melange
	clear
	echo -e "${vert}\t\tVEUILLEZ CHOISIR LE MODE DU JEU DE FRAPPE${neutre}\n"
	echo -e "${clinote}${fondJaune}1 - Lettre \n2 - chiffre\n3 - melange\n${neutre}"
	read -sn 1 mod
	case "$mod" in
		1|2|3)
			Mode=$mod
			;;
		*)
			echo -e "${rouge}Appuyer sur 1 ou 2 ou 3 ...${neutre}";
			sleep 0.5
			choix_niveau
			;;
	esac
	clear
}
generer_mot()
{
	# Generer un mot / chiffre aleatoire
	if [ $# -gt 0 ]
	then
		case $1 in
			1)
				nLigne=$(($RANDOM % $(cat exemple.lettre | tr ' ' '\n' | wc -l) + 1))
				Mot=$(cat exemple.lettre | tr ' ' '\n' | awk NR==$nLigne)
				;;
			2)
				Mot=$RANDOM
				;;
			3)
				rando=$(($RANDOM % 2 + 1))
				generer_mot $rando
				;;
			*)
				choix_mode
				generer_mot $Mode
			;;
		esac
	else
		generer_mot $Mode
	fi
}
affiche_mot()
{
	echo -e "${bleu}${fondBlanc}"
	echo -e "Taper : ${clinote}\" $Mot \""
	echo -e "${neutre}\n"
}
jeu_de_frappe()
{
	# Fonction qui est le coeur du jeu , generer le mot aleatoire et demander de la frapper

	# Le delai pour le frapper suit le niveau choisit
	tps=10 # Normal
	case "$Niveau" in
		1)
			tps=15
			;;
		2)
			tps=10
			;;
		3)
			tps=5
			;;
	esac

	nbTour=10
	i=0
	trouver=0
	while [ $i -ne $nbTour ]
	do
		clear
		generer_mot $Mode
		affiche_mot

		read -t "$tps" -p "  >> " entree
		if [ "$entree" = "$Mot" ]
		then
			trouver=$(($trouver + 1))
		fi
		i=$(($i + 1))
		clear
	done
	echo "Votre precision est de $trouver sur $nbTour . \n"
}

bienvenue
choix_niveau
choix_mode
jeu_de_frappe
