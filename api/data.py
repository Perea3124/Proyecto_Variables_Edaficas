import pandas as pd
import numpy as np

def load_data(path_excel):
    """
    Carga los datos desde un archivo Excel.
    Args:
        path_excel (str): Ruta al archivo Excel.
    Returns:
        DataFrame: Datos cargados desde el archivo.
    """
    try:
        df = pd.read_excel(path_excel)
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {path_excel}")
        return None
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return None

def filter_data(df, departamento=None, municipio=None, cultivo=None, n=None):
    """
    Filtra el DataFrame según los parámetros dados.

    Args:
        df (DataFrame): Datos completos.
        departamento (str): Nombre del departamento a filtrar.
        municipio (str): Nombre del municipio a filtrar.
        cultivo (str): Nombre del cultivo a filtrar.
        n (int): Número máximo de registros a devolver.

    Returns:
        DataFrame: Datos filtrados.
    """
    # Filtrar por departamento
    if departamento:
        df = df[df['Departamento'].str.upper() == departamento.upper()]
    
    # Filtrar por municipio
    if municipio:
        df = df[df['Municipio'].str.upper() == municipio.upper()]
    
    # Filtrar por cultivo
    if cultivo:
        df = df[df['Cultivo'].str.upper() == cultivo.upper()]
    
    # Limitar el número de registros
    if n is not None:
        df = df.head(n)
    
    return df


def _to_numeric_clean(series):
    """
    Limpia una serie: reemplaza comas por puntos, quita espacios,
    transforma 'ND' u otros no numéricos a NaN y convierte a float.
    """
    # Convertir a str, limpiar tokens no numéricos comunes y reemplazar coma por punto
    s = series.astype(str).str.strip().replace({'ND': '', 'nd': '', 'NaN': ''})
    s = s.str.replace(',', '.', regex=False)
    return pd.to_numeric(s, errors='coerce')

def _choose_scaling_factor_for_variable(median_value, variable):
    """
    Elige un factor (1,1e3,1e6,1e9,1e12,1e15) para dividir la serie de una variable
    con el objetivo de que la mediana final quede en un rango razonable que depende
    de la variable (pH, P, K).
    """
    if pd.isna(median_value):
        return 1.0

    # Rango objetivo por variable
    targets = {
        'ph': (0.0, 14.0),       # pH natural 0-14 (no escalar normalmente)
        'P': (0.1, 200.0),       # Fósforo en mg/kg (rango amplio seguro)
        'K': (0.1, 10.0)         # Potasio en cmol(+)/kg (rango agronómico esperado)
    }

    low, high = targets.get(variable, (0.1, 1000.0))

    for f in [1.0, 1e3, 1e6, 1e9, 1e12, 1e15]:
        median_after = median_value / f
        if (abs(median_after) >= low) and (abs(median_after) <= high):
            return float(f)

    # fallback: devolver 1.0 si ningún factor encaja
    return 1.0


def calculate_medians(df, apply_scaling=True):
    """
    Calcula mediana de pH, Fósforo (P) y Potasio (K) en el DataFrame recibido.
    Si apply_scaling==True aplicará la heurística de escalado; si es False,
    devolverá las medianas sobre los valores limpiados sin aplicar factores.
    Devuelve dict con keys: ph, P, K, topografia, p_factor, k_factor.
    """
    result = {'ph': None, 'P': None, 'K': None, 'topografia': None, 'p_factor': 1.0, 'k_factor': 1.0}

    # Detectar columnas relevantes (insensible a mayúsculas)
    ph_col = next((c for c in df.columns if 'ph' in c.lower()), None)
    p_col = next((c for c in df.columns if 'fósforo' in c.lower() or 'fosforo' in c.lower() or 'bray' in c.lower()), None)
    k_col = next((c for c in df.columns if 'potasio' in c.lower() or '(k)' in c.lower()), None)

    # pH: limpiar y calcular mediana (no se escala pH)
    if ph_col and ph_col in df.columns:
        ph_clean = _to_numeric_clean(df[ph_col])
        result['ph'] = float(ph_clean.median(skipna=True)) if not ph_clean.dropna().empty else None

    # Fósforo: limpiar; si apply_scaling True, elegir factor y dividir; si False usar factor=1
    if p_col and p_col in df.columns:
        p_clean = _to_numeric_clean(df[p_col])
        p_median = p_clean.median(skipna=True)
        if apply_scaling:
            p_factor = _choose_scaling_factor_for_variable(p_median, 'P')
        else:
            p_factor = 1.0
        if p_factor != 1.0:
            p_clean = p_clean / p_factor
        result['P'] = float(p_clean.median(skipna=True)) if not p_clean.dropna().empty else None
        result['p_factor'] = float(p_factor)

    # Potasio: limpiar; aplicar escalado solo si apply_scaling True
    if k_col and k_col in df.columns:
        k_clean = _to_numeric_clean(df[k_col])
        k_median = k_clean.median(skipna=True)
        if apply_scaling:
            k_factor = _choose_scaling_factor_for_variable(k_median, 'K')
        else:
            k_factor = 1.0
        if k_factor != 1.0:
            k_clean = k_clean / k_factor
        result['K'] = float(k_clean.median(skipna=True)) if not k_clean.dropna().empty else None
        result['k_factor'] = float(k_factor)

    # Topografía más frecuente si existe columna
    top_col = next((c for c in df.columns if 'topograf' in c.lower()), None)
    if top_col and top_col in df.columns:
        mode_series = df[top_col].dropna()
        result['topografia'] = mode_series.mode().iat[0] if not mode_series.empty else None

    return result
