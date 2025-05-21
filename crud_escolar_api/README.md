PIK - API
====================

## Requerimientos

* Python 3.5+
* Pip 3  

- - -

## Ambientación

1. Install Python 3.5+

2. Install Pip 3

3. Install virtualenv  
Se usa para crear ambientes virtuales y ejecutar la versión de Python requerida

4. Clonar el proyecto  

5. Activar el ambiente virtual  
$ source env/bin/activate
  Windows:
C:/path_to_the_folder/> env/Project_name/Scripts/activate.bat

6. Instalar las librerías requeridas por el proyecto  
$ pip3 install -r requirements.txt

7. Configurar conexión a base de datos (MySQL)  
/crud_escolar_api/my.cnf

8. Crear la base de datos y aplicar las migraciones  
$ python3 manage.py makemigrations crud_escolar_api  
$ python3 manage.py migrate  


9. Cargar todos los fixtures en el orden en que están numerados. Ejemplo:  
$ ./manage.py loaddata fixtures/1initial_data.json
$ ./manage.py loaddata fixtures/2authgroup.json
$ ./manage.py loaddata fixtures/3user.json
etc..

10. Crear un django administrator (IMPORTANTE)  
$ python3 manage.py createsuperuser --email admin@admin.com --username admin  
(Console input) PASSWORD: XXXXXX

11. Correr el servidor  
 python3 manage.py runserver  

IMPORTANT: Initial data, requiered for the project. Run once the database was created.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  -

## API Contract (postman)

https://www.getpostman.com/collections/######################

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  -

## Despliegue en producción - Google App Engine

1. Generar los archivos estáticos de django (Solo se requiere en el primer deploy)  
$ python3 manage.py collectstatic

2. Conectarse a la BD de prod mediante un proxy (Previamente instalar sdk de google cloud)    
$ ./cloud_sql_proxy -instances="whatsoporte:us-west2:stgwhatsoport-mysql"=tcp:3307

3. Configurar en el archivo my.cnf la conexión hacia esta BD  

4. Aplicar las migraciones del proyecto

5. Configurar en el archivo settings.py la conexión a la BD de google cloud (esta comentada)  

6. Ejecutar el comando de publicación  
$ gcloud app deploy -v {ULTIMA_VERSION_DESPLEGADA}  

7. En caso de haber desplegado el API en un nuevo App Engine, se requiere actualizar la URL del API en el servicio de Chat API  
Este paso se requiere para que chat api pueda enviar los nuevos mensajes al web hook (link del nuevo API)
