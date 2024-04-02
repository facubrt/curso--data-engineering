# Selección de lenguaje y versión
FROM python:3.10.5-slim-buster
#
# Se crea carpeta /app donde estará la aplicación
RUN mkdir /app
# Se copia la aplicación dentro de la carpeta app creada
COPY pre-entregable /app
# Se establece espacio de trabajo
WORKDIR /app
# Instalación de dependencias desde archivo de requerimientos
RUN pip install -r requirements.txt
#
# CMD
CMD ["python", "pre-entregable.py"]