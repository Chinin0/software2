# LenguaStream AI.

## Introducción

LenguaStream AI, es un software SaaS, para la Transcripcion y/o Traducción de Conferencia Presencial, Videos y Audio con Inteligencia Artificial.

<hr/>

## Estructura del proyecto

software/
├── Proyecto/
├── config  
├── config 
├── config 
├── config 
├── config 
├── __init__.py            creador del proyecto                                         realizar tercero

│   ├── controllers/           controlleras

│   │   ├── auth.py

│   │   └── user.py

│   ├── models/                Modelos para migrar a gestor de base de datos Postgres       realizar cuarto

│   │   ├── __init__.py

│   │   └── user.py

│   ├── routers/

│   │   └── router.py          Rutas

│   ├── views/                 Vistas 

│       ├── static/

│       ├── templates/

│       ├── auth/

│       │   ├── login.html

│       │   └── register.html

│       └── base.html

│       └── user/

│           └── profile.html

├── .env                       variable de entorno donde estarán tus credenciales            realizar primero

├── config.py                  configuraciones, las cuales dependerán del archivo .env       realizar segundo

├── requirements.txt

└── run.py                     para iniciar el proyecto



myapp/  

├── config  
│   ├── config.cfg  
│   └── test.py  
├── static   
|   ├── css  
|   │   └── loquesea.css  
|   └── js  
|       └── loquesea.js  
├── __init__.py  
├── productos  
│   ├── __init__.py  
│   ├── routes.py  
│   ├── static   
│   └── templates  
│       ├── formulario-producto.html  
│       └── productos.html  
├── proveedores  
   ├── __init__.py  
   ├── models.py  
   ├── routes.py  
   └── templates  
        ├── Formulario.html  
        └── Proveedores.html 





----

## Entorno Virtual, en caso que no tenga instalado el virtual instalar con el comando: pip install virtualenv

`python -m virtualenv env`

`.\env\Scripts\activate.bat`

`pip install -r requirements.txt`

Paso no necesario hacerlo porque si ya instalaste los requirements.txt : pip install Flask Flask-SQLAlchemy Flask-Migrate psycopg2 python-dotenv


----

## Migrar a la base de datos Postgres


`flask db init`

`flask db migrate -m "Crea la tabla Usuarios"`

`flask db upgrade`


----

## Uso de Git y Github para subir sus cambios al repositorio

`git init`

`git status`

`git add .`


esto solo se hace la primera vez

git config --global user.email "aquituemail@algo.com"

git config --global user.name "aquitunombredesuario"


`git commit -m "comentario de lo que realizaste"`


subir a repositorio esto se hace la primera vez despues ya no.
git remote add origin https://nombredelrepositorio.git


subir a la rama master, esto se utiliza para subir los cambios al github, revisa la rama a la cual vas a enviar los cambios

`git push -u origin master`



----

## Ramas del Proyecto

`git branch`

crear una rama en el repositorio, nombre_rama
`git branch nombre_rama`

cambiar de la rama nombre
`git checkout nombre_rama`


----

Si queres ver los cambios de otra rama que se haya subido al github, hacer un commit antes si esque has modificado algo.
Traer los cambios sin tener ramas,cuando solo tenes la rama Master.   
`git pull` 

Traer los cambios de una rama especifica nombre_rama
`git pull origin nombre_rama`

Unir los cambios de tu rama con tu rama master para subir al github

`git checkout master`

`git merge nombre_rama`

Subir a la rama master 
`git push -u origin master`

Subir a la rama especifica nombre_rama
`git push -u origin nombre_rama`



----

Ver los registros de los cambios realizados
`git log`

Crear un archivo para ingonar archivos especificos pones el nombre ya se de las capetas o archivos dentro

.gitignore


Revertir cambios de los archivos realizado 

`git checkout --`

