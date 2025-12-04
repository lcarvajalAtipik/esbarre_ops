#!/usr/bin/env python3
"""
Script principal para descargar clases con asistencia de clientes de Mindbody.

Uso:
    python descargar_clases.py

Antes de ejecutar, configura tus credenciales en config.py
"""

from datetime import datetime, timedelta
from mindbody_client import MindbodyClient, save_to_json, save_to_csv

# Importar configuración
try:
    from config import API_KEY, SITE_ID, STAFF_USERNAME, STAFF_PASSWORD
except ImportError:
    print("❌ Error: No se encontró el archivo config.py")
    print("   Crea el archivo config.py con tus credenciales")
    exit(1)


def main():
    print("=" * 60)
    print("🏋️ MINDBODY - Descarga de Clases con Asistencia")
    print("=" * 60)
    
    # Verificar que se configuró el API Key
    if API_KEY == "TU_API_KEY_AQUI":
        print("\n❌ Error: Debes configurar tu API Key en config.py")
        print("   1. Ve a: https://developers.mindbodyonline.com/")
        print("   2. Inicia sesión y ve a Account > API Credentials")
        print("   3. Crea una API Key y cópiala en config.py")
        exit(1)
    
    # Crear cliente
    print(f"\n🔧 Conectando a Mindbody (Site ID: {SITE_ID})...")
    client = MindbodyClient(api_key=API_KEY, site_id=SITE_ID)
    
    # Autenticar
    print(f"🔐 Autenticando como: {STAFF_USERNAME}")
    if not client.authenticate(STAFF_USERNAME, STAFF_PASSWORD):
        print("\n❌ No se pudo autenticar. Verifica tus credenciales en config.py")
        exit(1)
    
    # Configurar rango de fechas
    # Por defecto: últimos 90 días
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    print(f"\n📅 Rango de búsqueda:")
    print(f"   Desde: {start_date.strftime('%Y-%m-%d')}")
    print(f"   Hasta: {end_date.strftime('%Y-%m-%d')}")
    
    # Obtener clases con asistencia
    classes_data = client.get_all_classes_with_attendance(
        start_date=start_date,
        end_date=end_date
    )
    
    # Guardar resultados
    if classes_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar en JSON (estructura completa)
        json_file = f"clases_asistencia_{timestamp}.json"
        save_to_json(classes_data, json_file)
        
        # Guardar en CSV (formato tabular)
        csv_file = f"clases_asistencia_{timestamp}.csv"
        save_to_csv(classes_data, csv_file)
        
        # Calcular estadísticas
        total_classes = len(classes_data)
        total_attendees = sum(len(c["attendees"]) for c in classes_data)
        unique_clients = set()
        for c in classes_data:
            for a in c["attendees"]:
                if a["client_id"]:
                    unique_clients.add(a["client_id"])
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("📊 RESUMEN")
        print("=" * 60)
        print(f"   📚 Total de clases: {total_classes}")
        print(f"   👥 Total de asistencias: {total_attendees}")
        print(f"   🧑 Clientes únicos: {len(unique_clients)}")
        print(f"\n   📁 Archivos generados:")
        print(f"      • {json_file}")
        print(f"      • {csv_file}")
        
        # Mostrar muestra de datos
        if classes_data and classes_data[0]["attendees"]:
            print("\n" + "-" * 60)
            print("📋 Muestra de datos (primera clase con asistentes):")
            print("-" * 60)
            sample = classes_data[0]
            print(f"   Clase: {sample['class_name']}")
            print(f"   Fecha: {sample['start_datetime'][:10] if sample['start_datetime'] else 'N/A'}")
            print(f"   Instructor: {sample['staff_name']}")
            print(f"   Asistentes ({len(sample['attendees'])}):")
            for att in sample["attendees"][:5]:  # Mostrar máximo 5
                print(f"      • ID: {att['client_id']} - {att['client_name']}")
            if len(sample["attendees"]) > 5:
                print(f"      ... y {len(sample['attendees']) - 5} más")
    else:
        print("\n⚠️ No se encontraron clases en el rango especificado")
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado")
    print("=" * 60)


if __name__ == "__main__":
    main()

