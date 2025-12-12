#!/usr/bin/env python3
"""
Script para enviar un email de prueba usando SendGrid
"""
import os
import ssl
from pathlib import Path
from dotenv import load_dotenv

# Desactivar advertencias SSL (importante para desarrollo)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Crear contexto SSL permisivo
import certifi
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Cargar .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from utils.email_utils import send_registration_email

print("=" * 60)
print("PRUEBA DE ENVÍO DE EMAIL CON SENDGRID")
print("=" * 60)

# Email de prueba
test_email = input("\n📧 Ingresa tu email para enviar una prueba: ").strip()

if not test_email:
    print("❌ Email vacío. Abortando.")
    exit(1)

print(f"\n📤 Enviando email de prueba a: {test_email}")

try:
    result = send_registration_email(test_email)
    if result:
        print("✅ Email enviado exitosamente!")
        print("\nVerifica tu bandeja de entrada. Si usas Gmail, revisa también Spam.")
    else:
        print("❌ Falló el envío. Revisa los logs anteriores para más detalles.")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
