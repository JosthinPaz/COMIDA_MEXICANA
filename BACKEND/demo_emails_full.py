#!/usr/bin/env python3
"""
Script de demostración completa del sistema de emails
Prueba todos los tipos de email disponibles
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from utils.email_utils import (
    send_registration_email,
    enviar_alerta_stock,
    enviar_cambio_estado_pedido,
    enviar_recuperacion_contrasena,
)

print("=" * 70)
print("DEMO COMPLETA - SISTEMA DE EMAILS JOSNISHOP")
print("=" * 70)

test_email = input("\n📧 Ingresa tu email para la demostración: ").strip()

if not test_email:
    print("❌ Email vacío. Abortando.")
    exit(1)

print("\n" + "=" * 70)
print("Enviando diferentes tipos de emails...")
print("=" * 70)

tests = [
    {
        "nombre": "Email de Registro",
        "funcion": lambda: send_registration_email(test_email),
    },
    {
        "nombre": "Alerta de Stock Bajo",
        "funcion": lambda: enviar_alerta_stock(test_email, "Laptop Dell", 3),
    },
    {
        "nombre": "Cambio de Estado de Pedido",
        "funcion": lambda: enviar_cambio_estado_pedido(test_email, "PED-12345", "En Tránsito"),
    },
    {
        "nombre": "Recuperación de Contraseña",
        "funcion": lambda: enviar_recuperacion_contrasena(test_email, "Temp123456!"),
    },
]

results = []

for i, test in enumerate(tests, 1):
    print(f"\n[{i}/{len(tests)}] Enviando: {test['nombre']}")
    try:
        resultado = test['funcion']()
        status = "✅ ÉXITO" if resultado else "⚠️  CON FALLBACK"
        results.append((test['nombre'], status))
        print(f"    {status}")
    except Exception as e:
        print(f"    ❌ ERROR: {e}")
        results.append((test['nombre'], "❌ ERROR"))

print("\n" + "=" * 70)
print("RESUMEN DE RESULTADOS")
print("=" * 70)

for nombre, status in results:
    print(f"  {status} - {nombre}")

total_success = sum(1 for _, status in results if "✅" in status or "⚠️" in status)
print(f"\n  Total: {total_success}/{len(results)} emails procesados")

print("\n" + "=" * 70)
print("PRÓXIMOS PASOS:")
print("=" * 70)
print("""
1. Verifica tu bandeja de entrada (y SPAM) en: {email}
2. Deberías recibir 4 emails de diferentes tipos
3. Confirma que el contenido está correctamente formateado
4. Para usar SendGrid en producción:
   - Ve a https://sendgrid.com/
   - Verifica josnishop@gmail.com como Sender Identity
   - El sistema automáticamente usará SendGrid

NOTAS:
  • Si algún email llegó a SPAM, es normal en desarrollo
  • SMTP funciona siempre, SendGrid requiere verificación
  • Todos los emails tienen fallback automático
""".format(email=test_email))

print("=" * 70)
