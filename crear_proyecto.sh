#!/bin/bash
salir=0

#COLORES PARA LOS MENSAJES

VERDE="\033[0;32m"
ROJO="\033[0;31m"
FONDO_AZUL="\e[44m"
AZUL="\033[1;34m"
VIOLETA="\e[0;35m"
SIN_COLOR="\033[0m"

echo_color() {
    color=$1
    mensaje=$2
    echo -e "${color}${mensaje}${SIN_COLOR}"
}

crear_entorno(){

 mkdir TPFINAL
  cd ./TPFINAL

  mkdir APIRESTFUL
   cd ./APIRESTFUL

	#Parte del backend
     mkdir api
      cd api

       mkdir db
       mkdir static
       touch app.py
      cd ..
	#Parte del Front End

     mkdir front_app
      cd front_app
       mkdir static
       mkdir templates
       touch app.py

	cd ./static
	mkdir css
	mkdir images
	mkdir js
       cd ..

	cd ./templates
	touch index.html

       cd .. #estoy en static y voy a front_app
      cd .. #estoy en front_app y voy a APIRESTFUL

#VUELVO AL INICIO PARA NO INSTALAR EL ENTRONO VIRTUAL ACÁ
echo_color $VERDE "Entorno creado correctamente"
}

instalar_pip(){

echo_color $AZUL "Se instalará PIP"

	if pip3 --version ; then
	echo "Pip instalado"
	else
	echo "Pip debe instalares"
	sudo apt install python3-pip
	fi 


echo_color $VERDE "Se instaló PIP correctamente"
}

instalar_python(){
echo_color $AZUL "Se instalará PYTHON"
	if python3 --version ;then
         echo "Python instalado"
         else
         echo "Python debe instalarse"
         sudo apt install python3
         fi
echo_color $VERDE "Se instaló PYTHON correctamente"
}

comprobacion(){
pwd #Compruebo
}

instala_venv(){

#Crea entorno virtual en la carpeta .venv
sudo apt install python3-venv
python3 -m venv .venv
echo_color $VERDE "Se creó el entorno virtual"
}

instala_flask(){
pip install Flask
pip install requests
echo_color $VERDE "Se intalo Flask"
}


instala_flaskcors(){
pip install flask_cors

echo_color $VERDE "Se intalo Flask cors"
}



instala_flaskMail(){
pip install Flask-Mail

echo_color $VERDE "Se intalo Flask MAIL"
}

instala_dotenv(){
pip3 install python-dotenv
echo_color $VERDE "Se intalo dotenv"
}

activar_entorno(){
source .venv/bin/activate
echo_color $VERDE "SE ACTIVO"
}

desactivar_entorno(){
deactivate
echo_color $ROJO "SE DESACTIVO"
 }

salir_menu() {
	salir=1
	echo_color $ROJO "Saliendo del programa"
}

crear_archivo_env(){
cd
cd TPFINAL/APIRESTFUL
cd front_app
touch .env
echo -e "MAIL_SERVER=smtp.gmail.com \nMAIL_PORT=587 \nMAIL_USE_TLS=True \nMAIL_USE_SSL=False \nMAIL_USERNAME=mtbrally51@gmail.com \nMAIL_PASSWORD=wwij bazm genv jlve \nMAIL_DEFAULT_SENDER=mtbrally51@gmail.com" > "$HOME/TPFINAL/APIRESTFUL/front_app/.env"
echo_color $VERDE "SE CREÓ EL ARCHIVO .env (Front)"

cd
cd TPFINAL/APIRESTFUL
cd front_app
touch .env
echo -e "DB_HOST=localhost \nDB_USER=root \nDB_PASSWORD= \nDB_NAME=hotel\n#Chicos pongan en DB_PASSWORD la contraseña que tienen para entrar a mysql (sudo mysql -u root -p)" > "$HOME/TPFINAL/APIRESTFUL/api/.env"
echo_color $VERDE "SE CREÓ EL ARCHIVO .env (Back)"

}

while [[ $salir == 0 ]];
do
echo " "
echo_color $FONDO_AZUL "Ingrese una opción para hacer con el trabajo"

echo_color $VIOLETA  "^^^^^^^^^^ < MENU > ^^^^^^^^^^\n"

echo "Porfavor ejecutá los comandos en orden(si ya tenés armado el repositorio pasá al segundo)"

echo " 1) Crea el entorno local"
echo " 2) Instaladores (Pip, Python)"
echo " 3) Intalar complementos del entrono virtual"
echo_color $AZUL ' Para estos siguientes pasos, salí del programa "8)" y volvé a ejecutar el programa con "-op" al final'
echo ' 4) Activar el entorno '

	if [ "$1" == "-op" ]; then
	echo " 5) Instala dependencias "
	echo " 6) Crear archivo para mail"
	echo " 7) Desactivar el entorno"
	fi

echo " 8) Salir"


echo_color $VIOLETA  "==============================="

read -p $'\e[44m OPCION\033[0m : ' opcion
case $opcion in

1)
	crear_entorno
	comprobacion
;;

2)
	instalar_pip
	instalar_python
;;

3)
	instala_venv
;;

4)

	activar_entorno
;;

5)
	instala_flask
	instala_flaskMail
	instala_dotenv
	instala_flaskcors
;;
6)
	crear_archivo_env
;;
7)
	desactivar_entorno
;;
8)
	salir_menu
;;
esac
done
