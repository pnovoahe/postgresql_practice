# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos (si tienes uno)
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de tu aplicación en el contenedor
COPY . .

# Expone el puerto 5000 para Flask
EXPOSE 5000

# Ejecuta el comando de Flask y el script para inicializar la base de datos
CMD ["flask", "run", "--host=0.0.0.0"]
