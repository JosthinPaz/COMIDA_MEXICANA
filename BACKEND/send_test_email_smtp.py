#!/usr/bin/env python3
"""
Script para usar SMTP directo (fallback funcional mientras se verifica SendGrid)
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from utils.email_utils import _send_email_message, HTML_EMAIL_TEMPLATE

print("=" * 60)
print("PRUEBA DE ENVÍO DE EMAIL VIA SMTP (FALLBACK)")
print("=" * 60)

# Email de prueba
test_email = input("\n📧 Ingresa tu email para enviar una prueba: ").strip()

if not test_email:
    print("❌ Email vacío. Abortando.")
    exit(1)

print(f"\n📤 Enviando email de prueba a: {test_email}")

try:
    # Usar función con force_smtp=True para ignorar SendGrid
    asunto = "Prueba de Email - JosniShop"
    texto = "Este es un email de prueba."
    
    html = HTML_EMAIL_TEMPLATE.format(
        title="Prueba de Email",
        intro="Este es un email de prueba desde JosniShop",
        content="<p>Si recibes este email, ¡tu configuración SMTP funciona correctamente!</p>",
        footer="Esto es solo una prueba.",
        button_html=""
    )
    
    result = _send_email_message(test_email, asunto, texto, html, purpose='test_smtp', force_smtp=True)
    if result:
        print("✅ Email enviado exitosamente via SMTP!")
        print("\nVerifica tu bandeja de entrada. Si usas Gmail, revisa también Spam.")
    else:
        print("❌ Falló el envío. Revisa los logs anteriores para más detalles.")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

