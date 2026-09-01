# Paso 1: Entorno de ejecución 
FROM python:3.12-slim

# Paso 2: Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Paso 3: Copiar el archivo de dependencias 
COPY requirements.txt ./

# Paso 4: Instalar dependencias 
RUN pip install --no-cache-dir -r requirements.txt

# Paso 5: Copiar el resto del código
COPY . .

# Paso 6: Exponer el puerto 
EXPOSE 8000

# Paso 7: Comando para arrancar la app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]