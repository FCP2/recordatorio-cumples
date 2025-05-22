# app.py
import streamlit as st
import pandas as pd
import datetime

st.title("🎂 Recordatorio de Cumpleaños")

# Subir archivo Excel
archivo = st.file_uploader("Sube el archivo de cumpleaños (.xlsx)", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)

        hoy = datetime.datetime.now()
        tres_dias_despues = hoy + datetime.timedelta(days=3)

        st.write("📅 Hoy es:", hoy.strftime("%d/%m/%Y"))

        cumples_proximos = []
        for _, row in df.iterrows():
            nombre = row.get("Nombre", "").strip()
            dependencia = row.get("Dependencia", "").strip()
            fecha_raw = row.get("Fecha", "")

            try:
                fecha_dt = pd.to_datetime(fecha_raw, errors="coerce")
                if pd.isna(fecha_dt):
                    raise ValueError()
                cumple = datetime.datetime(year=tres_dias_despues.year, month=fecha_dt.month, day=fecha_dt.day)
                if cumple.day == tres_dias_despues.day and cumple.month == tres_dias_despues.month:
                    cumples_proximos.append((nombre, dependencia, cumple.strftime("%d/%m")))
            except:
                continue

        if cumples_proximos:
            st.success("🎉 Cumpleaños dentro de 3 días:")
            for nombre, dependencia, fecha in cumples_proximos:
                st.write(f"- **{nombre}** ({dependencia}) cumple el {fecha}")
        else:
            st.info("No hay cumpleaños en 3 días.")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")