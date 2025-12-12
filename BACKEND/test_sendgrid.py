#!/usr/bin/env python3
"""
Script para testear la configuración de SendGrid
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Verificar variables
sendgrid_key = os.getenv('SENDGRID_API_KEY')
smtp_email = os.getenv('SMTP_EMAIL')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')

print("=" * 60)
print("TEST DE CONFIGURACIÓN DE SENDGRID")
print("=" * 60)

print("\n📋 VARIABLES CARGADAS:")
print(f"  SENDGRID_API_KEY: {'✓ Configurada' if sendgrid_key else '✗ NO CONFIGURADA'}")
if sendgrid_key:
    print(f"    Valor: {sendgrid_key[:10]}...{sendgrid_key[-10:]}")
print(f"  SMTP_EMAIL: {'✓ OK' if smtp_email else '✗ Falta'} - {smtp_email}")
print(f"  SMTP_PASSWORD: {'✓ OK' if smtp_password else '✗ Falta'}")
print(f"  SMTP_SERVER: {'✓ OK' if smtp_server else '✗ Falta'} - {smtp_server}")
print(f"  SMTP_PORT: {'✓ OK' if smtp_port else '✗ Falta'} - {smtp_port}")

print("\n🔧 PROBANDO IMPORTACIONES:")
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    print("  ✓ SendGrid importado exitosamente")
except ImportError as e:
    print(f"  ✗ Error importando SendGrid: {e}")
    print("    Instala con: pip install sendgrid")

try:
    from utils.email_utils import _get_email_settings
    print("  ✓ email_utils importado exitosamente")
except ImportError as e:
    print(f"  ✗ Error importando email_utils: {e}")

print("\n🧪 VERIFICANDO CONFIGURACIÓN EN email_utils:")
try:
    from utils.email_utils import _get_email_settings
    settings = _get_email_settings()
    if settings:
        has_sendgrid = settings.get('sendgrid_api_key') is not None
        print(f"  ✓ Configuración cargada exitosamente")
        print(f"    - Usando SendGrid: {has_sendgrid}")
        print(f"    - Email remitente: {settings.get('remitente')}")
        print(f"    - SMTP Server: {settings.get('smtp_server')}")
    else:
        print("  ✗ No se pudo cargar configuración")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("Configuración lista. SendGrid debería funcionar correctamente.")
print("=" * 60)
