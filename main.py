import argparse
from api.data import load_data, filter_data, calculate_medians
from ui.console import get_user_input, print_results_table

DEFAULT_FILE = "resultado_laboratorio_suelo.xlsx"

def run(departamento, municipio, cultivo, n, apply_scaling, file_path):
    df = load_data(file_path)
    if df is None:
        print("Error: no se pudo cargar el archivo Excel. Verifica la ruta y nombre del archivo.")
        return 1

    df_filtered = filter_data(df, departamento=departamento, municipio=municipio, cultivo=cultivo, n=n)
    if df_filtered is None or df_filtered.empty:
        print("No se encontraron registros con los filtros especificados.")
        return 1

    # Si la API calcula medianas usando escalado por defecto internamente,
    # le pasamos el resultado ya sea aplicando o no el escalado en la API
    # (la API actual toma auto_scale en el constructor; aquí asumimos que calculará en base a lo que existe)
    summary = calculate_medians(df_filtered, apply_scaling=apply_scaling)
    print_results_table(departamento, municipio, cultivo, summary)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Consulta medianas de variables edáficas desde Excel")
    parser.add_argument("--departamento", type=str, help="Departamento a consultar")
    parser.add_argument("--municipio", type=str, help="Municipio a consultar")
    parser.add_argument("--cultivo", type=str, help="Cultivo a consultar")
    parser.add_argument("--n", type=int, default=0, help="Número de registros a devolver (0 = todos)")
    parser.add_argument("--no-scale", action="store_true", help="Desactivar escalado automático")
    parser.add_argument("--file", type=str, default=DEFAULT_FILE, help="Ruta al archivo Excel")
    args = parser.parse_args()

    departamento = args.departamento
    municipio = args.municipio
    cultivo = args.cultivo
    n = args.n if args.n and args.n > 0 else None
    apply_scaling = not args.no_scale
    file_path = args.file

    # Si faltan parámetros, pedirlos por consola
    if not (departamento and municipio and cultivo):
        departamento, municipio, cultivo, n_input, apply_scaling_input = get_user_input()
        if departamento:
            departamento = departamento
        if municipio:
            municipio = municipio
        if cultivo:
            cultivo = cultivo
        # Si get_user_input devolvió un n válido, usarlo
        if n_input is not None:
            n = n_input
        # Si get_user_input devolvió algo explícito para apply_scaling, respetarlo
        apply_scaling = apply_scaling_input

    # Nota: la API `load_data` y `calculate_medians` deben estar implementadas previamente
    # y `calculate_medians` debe usar las columnas limpias/extras generadas en `api/data.py`.
    return_code = run(departamento, municipio, cultivo, n, apply_scaling, file_path)
    exit(return_code)

if __name__ == "__main__":
    main()
