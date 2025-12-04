"""
Cliente para la API de Mindbody
Descarga clases con asistencia de clientes
"""

import requests
from datetime import datetime, timedelta
from typing import Optional
import json
import csv


class MindbodyClient:
    """Cliente para interactuar con la API pública de Mindbody."""
    
    BASE_URL = "https://api.mindbodyonline.com/public/v6"
    
    def __init__(self, api_key: str, site_id: str = "-99"):
        self.api_key = api_key
        self.site_id = site_id
        self.user_token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            "API-Key": self.api_key,
            "SiteId": self.site_id,
            "Content-Type": "application/json"
        })
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Obtiene un token de usuario para operaciones autenticadas.
        
        Args:
            username: Email o username del staff/owner
            password: Contraseña del staff/owner
            
        Returns:
            True si la autenticación fue exitosa
        """
        url = f"{self.BASE_URL}/usertoken/issue"
        payload = {
            "Username": username,
            "Password": password
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            self.user_token = data.get("AccessToken")
            if self.user_token:
                self.session.headers["Authorization"] = f"Bearer {self.user_token}"
                print("✅ Autenticación exitosa")
                return True
            else:
                print("❌ No se recibió token de acceso")
                return False
                
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error de autenticación: {e}")
            print(f"   Respuesta: {response.text}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def get_classes(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        class_ids: Optional[list] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list:
        """
        Obtiene las clases programadas.
        
        Args:
            start_date: Fecha de inicio (default: hoy - 30 días)
            end_date: Fecha de fin (default: hoy)
            class_ids: IDs específicos de clases
            limit: Máximo de resultados por página
            offset: Desplazamiento para paginación
            
        Returns:
            Lista de clases
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()
        
        url = f"{self.BASE_URL}/class/classes"
        params = {
            "StartDateTime": start_date.strftime("%Y-%m-%dT00:00:00"),
            "EndDateTime": end_date.strftime("%Y-%m-%dT23:59:59"),
            "Limit": limit,
            "Offset": offset
        }
        
        if class_ids:
            params["ClassIds"] = ",".join(map(str, class_ids))
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("Classes", [])
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error obteniendo clases: {e}")
            print(f"   Respuesta: {response.text}")
            return []
    
    def get_class_visits(
        self,
        class_id: int
    ) -> list:
        """
        Obtiene las visitas/asistencias de una clase específica.
        
        Args:
            class_id: ID de la clase
            
        Returns:
            Lista de visitas con información de clientes
        """
        url = f"{self.BASE_URL}/class/classvisits"
        params = {
            "ClassId": class_id
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("Visits", []) or data.get("Class", {}).get("Visits", []) or []
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error obteniendo visitas para clase {class_id}: {e}")
            return []
    
    def get_all_classes_with_attendance(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list:
        """
        Obtiene todas las clases con su asistencia de clientes.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            Lista de clases con asistencia
        """
        all_classes = []
        offset = 0
        limit = 100
        
        print(f"\n📅 Buscando clases desde {start_date or 'hace 30 días'} hasta {end_date or 'hoy'}...")
        
        # Obtener todas las clases con paginación
        while True:
            classes = self.get_classes(
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                offset=offset
            )
            
            if not classes:
                break
                
            all_classes.extend(classes)
            print(f"   📦 Obtenidas {len(all_classes)} clases...")
            
            if len(classes) < limit:
                break
            offset += limit
        
        print(f"\n✅ Total de clases encontradas: {len(all_classes)}")
        
        # Obtener asistencia para cada clase
        classes_with_attendance = []
        
        for i, cls in enumerate(all_classes, 1):
            class_id = cls.get("Id")
            class_name = cls.get("ClassDescription", {}).get("Name", "Sin nombre")
            start_time = cls.get("StartDateTime", "")
            
            print(f"   🔍 [{i}/{len(all_classes)}] Obteniendo asistencia de: {class_name} ({start_time[:10] if start_time else 'N/A'})")
            
            visits = self.get_class_visits(class_id)
            
            class_data = {
                "class_id": class_id,
                "class_name": class_name,
                "start_datetime": start_time,
                "end_datetime": cls.get("EndDateTime", ""),
                "staff_name": cls.get("Staff", {}).get("Name", ""),
                "location": cls.get("Location", {}).get("Name", ""),
                "total_booked": cls.get("TotalBooked", 0),
                "max_capacity": cls.get("MaxCapacity", 0),
                "is_canceled": cls.get("IsCanceled", False),
                "attendees": []
            }
            
            for visit in visits:
                client = visit.get("Client", {}) or {}
                attendee = {
                    "client_id": client.get("Id") or visit.get("ClientId"),
                    "client_name": f"{client.get('FirstName', '')} {client.get('LastName', '')}".strip(),
                    "email": client.get("Email", ""),
                    "signed_in": visit.get("SignedIn", False),
                    "late_cancelled": visit.get("LateCancelled", False),
                    "make_up": visit.get("MakeUp", False),
                    "visit_id": visit.get("Id")
                }
                class_data["attendees"].append(attendee)
            
            classes_with_attendance.append(class_data)
        
        return classes_with_attendance
    
    def get_clients(self, limit: int = 100, offset: int = 0, search_text: str = None) -> list:
        """
        Obtiene la lista de clientes.
        
        Args:
            limit: Máximo de resultados
            offset: Desplazamiento para paginación
            search_text: Texto para buscar clientes
            
        Returns:
            Lista de clientes
        """
        url = f"{self.BASE_URL}/client/clients"
        params = {
            "Limit": limit,
            "Offset": offset
        }
        
        if search_text:
            params["SearchText"] = search_text
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("Clients", [])
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error obteniendo clientes: {e}")
            return []
    
    def get_client_visits(
        self,
        client_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list:
        """
        Obtiene el historial de visitas de un cliente específico.
        
        Args:
            client_id: ID del cliente
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            Lista de visitas del cliente
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        url = f"{self.BASE_URL}/client/clientvisits"
        params = {
            "ClientId": client_id,
            "StartDate": start_date.strftime("%Y-%m-%d"),
            "EndDate": end_date.strftime("%Y-%m-%d")
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("Visits", [])
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error obteniendo visitas del cliente {client_id}: {e}")
            return []


def save_to_json(data: list, filename: str):
    """Guarda los datos en formato JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"💾 Datos guardados en: {filename}")


def save_to_csv(data: list, filename: str):
    """Guarda los datos en formato CSV (una fila por asistente)."""
    rows = []
    
    for cls in data:
        if cls["attendees"]:
            for attendee in cls["attendees"]:
                rows.append({
                    "class_id": cls["class_id"],
                    "class_name": cls["class_name"],
                    "start_datetime": cls["start_datetime"],
                    "end_datetime": cls["end_datetime"],
                    "staff_name": cls["staff_name"],
                    "location": cls["location"],
                    "client_id": attendee["client_id"],
                    "client_name": attendee["client_name"],
                    "email": attendee["email"],
                    "signed_in": attendee["signed_in"],
                    "late_cancelled": attendee["late_cancelled"]
                })
        else:
            # Incluir clases sin asistentes también
            rows.append({
                "class_id": cls["class_id"],
                "class_name": cls["class_name"],
                "start_datetime": cls["start_datetime"],
                "end_datetime": cls["end_datetime"],
                "staff_name": cls["staff_name"],
                "location": cls["location"],
                "client_id": "",
                "client_name": "",
                "email": "",
                "signed_in": "",
                "late_cancelled": ""
            })
    
    if rows:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"💾 Datos guardados en: {filename}")
    else:
        print("⚠️ No hay datos para guardar")


if __name__ == "__main__":
    # ═══════════════════════════════════════════════════════════════
    # CONFIGURACIÓN - Modifica estos valores con tus credenciales
    # ═══════════════════════════════════════════════════════════════
    
    API_KEY = "TU_API_KEY_AQUI"  # Obtén tu API key del portal de desarrolladores
    SITE_ID = "-99"  # -99 para sandbox, o tu Site ID real
    
    # Credenciales del staff/owner para autenticación
    STAFF_USERNAME = "mindbodysandbox99@gmail.com"
    STAFF_PASSWORD = "Apitest1234"
    
    # Rango de fechas (None = últimos 30 días)
    START_DATE = None  # O usa: datetime(2024, 1, 1)
    END_DATE = None    # O usa: datetime(2024, 12, 31)
    
    # ═══════════════════════════════════════════════════════════════
    
    print("=" * 60)
    print("🏋️ MINDBODY - Descarga de Clases con Asistencia")
    print("=" * 60)
    
    # Crear cliente
    client = MindbodyClient(api_key=API_KEY, site_id=SITE_ID)
    
    # Autenticar
    if not client.authenticate(STAFF_USERNAME, STAFF_PASSWORD):
        print("\n❌ No se pudo autenticar. Verifica tus credenciales.")
        exit(1)
    
    # Obtener clases con asistencia
    classes_data = client.get_all_classes_with_attendance(
        start_date=START_DATE,
        end_date=END_DATE
    )
    
    # Guardar resultados
    if classes_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar en JSON (estructura completa)
        save_to_json(classes_data, f"clases_asistencia_{timestamp}.json")
        
        # Guardar en CSV (formato tabular)
        save_to_csv(classes_data, f"clases_asistencia_{timestamp}.csv")
        
        # Resumen
        total_attendees = sum(len(c["attendees"]) for c in classes_data)
        print(f"\n📊 RESUMEN:")
        print(f"   • Total de clases: {len(classes_data)}")
        print(f"   • Total de asistencias: {total_attendees}")
        print(f"   • Clientes únicos: {len(set(a['client_id'] for c in classes_data for a in c['attendees'] if a['client_id']))}")
    else:
        print("\n⚠️ No se encontraron clases en el rango especificado")
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado")
    print("=" * 60)

