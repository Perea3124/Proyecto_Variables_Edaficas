# Proyecto Fundamentos Básicos de Python – Variables Edáficas

## Descripción
Este proyecto implementa una aplicación en Python para el análisis de datos de variables edáficas a partir de un archivo Excel.  
Permite filtrar información por **departamento**, **municipio** y **cultivo**, y calcular la mediana de pH, Fósforo (P) y Potasio (K), aplicando o no un factor de escala.

## Estructura del Proyecto
```
Proyecto_Variables_Edaficas/
│
├── api/                  # Módulo de manejo de datos
│   ├── __init__.py
│   └── data.py
│
├── ui/                   # Módulo de interacción con el usuario
│   ├── __init__.py
│   └── console.py
│
├── utils/                # Funciones auxiliares
│   ├── __init__.py
│   └── cleaning.py
│
├── main.py               # Punto de entrada principal
├── run_demo.py           # Script de prueba rápida
├── requirements.txt      # Dependencias del proyecto
├── tests/                # Pruebas automatizadas con pytest
└── README.md             # Este archivo
```

## Instalación y Uso
1. **Clonar el repositorio**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Proyecto_Variables_Edaficas
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   - Windows (PowerShell):
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar el programa**
   ```bash
   python main.py --departamento "CUNDINAMARCA" --municipio "FUNZA" --cultivo "Uchuva" --n 10
   ```

6. **Ejecutar sin factores de escala**
   ```bash
   python main.py --departamento "CUNDINAMARCA" --municipio "FUNZA" --cultivo "Uchuva" --n 10 --no-scale
   ```

7. **Ejecutar pruebas**
   ```bash
   pytest -q
   ```

## Ejemplo de salida
```
| Departamento   | Municipio   | Cultivo   | Topografia   |   pH (mediana) |   P (mediana) |   K (mediana) |   P_factor |   K_factor |
|----------------|-------------|-----------|--------------|----------------|---------------|---------------|------------|------------|
| CUNDINAMARCA   | FUNZA       | Uchuva    | Ondulado     |           5.61 |          6.53 |         0.728 |      1e+15 |      1e+09 |
```

## Pruebas Automatizadas
El proyecto incluye pruebas con **pytest** ubicadas en la carpeta `tests/`.  
Estas validan el cálculo de medianas y el correcto filtrado de datos.

## Licencia
Este proyecto es de uso académico y no tiene fines comerciales.
