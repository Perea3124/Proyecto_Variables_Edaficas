from api.data import load_data, filter_data, calculate_medians

RUTA_EXCEL = r"C:\Users\Perea\Documents\Programación 4\Proyecto_Variables_Edaficas\resultado_laboratorio_suelo.xlsx"

def main():
    df = load_data(RUTA_EXCEL)
    if df is None:
        print("Fallo al cargar el Excel.")
        return

    df_filtrado = filter_data(df, departamento="CUNDINAMARCA", municipio="FUNZA", cultivo="Uchuva", n=100)
    med = calculate_medians(df_filtrado)
    print("Medianas calculadas sobre el subconjunto filtrado:")
    print(med)

if __name__ == "__main__":
    main()
