try:
    from tabulate import tabulate
except Exception:
    tabulate = None

def get_user_input():
    """
    Solicita al usuario los parámetros: departamento, municipio, cultivo, n (número de registros)
    y si desea aplicar el escalado automático. Devuelve una tupla.
    """
    departamento = input("Departamento: ").strip()
    municipio = input("Municipio: ").strip()
    cultivo = input("Cultivo: ").strip()

    n_raw = input("Número de registros a devolver (0 para todos): ").strip()
    try:
        n = int(n_raw)
        if n <= 0:
            n = None
    except Exception:
        n = None

    apply_scaling = input("Aplicar escalado automático? (s/n) [s]: ").strip().lower()
    if apply_scaling == 'n':
        apply_scaling = False
    else:
        apply_scaling = True

    return departamento, municipio, cultivo, n, apply_scaling

def print_results_table(departamento, municipio, cultivo, summary):
    """
    Imprime en terminal la tabla con Departamento, Municipio, Cultivo, Topografía,
    y medianas de pH, P y K. summary es el dict devuelto por calculate_medians().
    """
    headers = ['Departamento', 'Municipio', 'Cultivo', 'Topografia', 'pH (mediana)', 'P (mediana)', 'K (mediana)', 'P_factor', 'K_factor']
    row = [
        departamento or '',
        municipio or '',
        cultivo or '',
        summary.get('topografia', '') or '',
        round(summary.get('ph'), 3) if summary.get('ph') is not None else '',
        round(summary.get('P'), 3) if summary.get('P') is not None else '',
        round(summary.get('K'), 3) if summary.get('K') is not None else '',
        summary.get('p_factor', ''),
        summary.get('k_factor', '')
    ]
    if tabulate:
        print(tabulate([row], headers=headers, tablefmt='github'))
    else:
        # Fallback simple print
        print(" | ".join(headers))
        print(" | ".join(str(x) for x in row))
