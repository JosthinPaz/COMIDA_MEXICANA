import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path
# No es necesario base64 ni sendgrid imports
# import base64 
# try: ... except ImportError: ...
# _HAS_SENDGRID = False # Eliminado

# =========================================================================
# 1. PLANTILLA HTML
# =========================================================================

# Reusable HTML email template. The left colored stripe is red (#d32f2f).
# Uses simple inline styles for better email client compatibility.
HTML_EMAIL_TEMPLATE = """<!doctype html>
<html>
    <head>
        <meta charset=\"utf-8\"> 
        <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
    </head>
    <body style=\"margin:0;padding:0;font-family:Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;background:#f3f4f6;color:#111827;\">
        <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"padding:24px;\">
            <tr>
                <td align=\"center\"> 
                    <table role=\"presentation\" width=\"680\" cellspacing=\"0\" cellpadding=\"0\" style=\"background:#fff;border-radius:12px;overflow:hidden;border:1px solid #e5e7eb;box-shadow:0 6px 18px rgba(15,23,42,0.06);\">
                        <tr>
                            <td style=\"width:10px;background:#d32f2f;vertical-align:top;\">&nbsp;</td>
                            <td style=\"padding:28px 36px;\">

                                <h1 style=\"margin:6px 0 14px 0;font-size:22px;color:#0f1724;\">{title}</h1>
                                <p style=\"margin:0 0 18px 0;color:#374151;font-size:15px;\">{intro}</p>

                                <div style=\"background:#fafafa;border-radius:8px;padding:18px;margin:12px 0;border:1px solid #eef2f3;color:#1f2937;\">{content}</div>

                                <div style=\"margin:20px 0; text-align:center;\">{button_html}</div>
                                <div style=\"margin:10px 0 18px 0;color:#6b7280;font-size:14px;\">{footer}</div>

                                <div style=\"border-top:1px solid #eef2f6;margin-top:20px;padding-top:18px;text-align:center;color:#9ca3af;font-size:13px;\">
                                    <div>¿Necesitas ayuda? Contáctanos en <a href=\"mailto:soporte@josnishop.com\" style=\"color:#d32f2f;text-decoration:none;\">soporte@josnishop.com</a></div>
                                    <div style=\"margin-top:8px;font-weight:600;color:#374151;\">¡Gracias por confiar en nosotros! &nbsp; <span style=\"display:block;font-size:12px;color:#9ca3af;\">JOSNISHOP</span></div>
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>"""


# =========================================================================
# 2. UTILITIES DE BAJO NIVEL (Solo SMTP)
# =========================================================================

def _send_message_smtp(remitente, username, password, smtp_server, smtp_port, msg):
    """Try sending via SMTP_SSL first, then fallback to STARTTLS on port 587.
    Returns True on success, False on failure. Prints detailed errors for debugging.
    """
    # Try SSL (commonly port 465)
    try:
        # Nota: Usamos smtp_port que debe ser 465 para SSL
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20) as server:
            if username:
                server.login(username, password)
            else:
                server.login(remitente, password)
            server.send_message(msg)
        return True
    except Exception as e_ssl:
        print(f"[SMTP_SSL] fallo: {e_ssl} (server={smtp_server}:{smtp_port})")

    # Fallback to STARTTLS (commonly port 587)
    try:
        with smtplib.SMTP(smtp_server, 587, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            if username:
                server.login(username, password)
            else:
                server.login(remitente, password)
            server.send_message(msg)
        return True
    except Exception as e_tls:
        # Si fallan ambos, se imprime el error de STARTTLS y retorna False
        print(f"[SMTP_STARTTLS] fallo: {e_tls} (server={smtp_server}:587)")

    return False

# Eliminada la función _send_via_sendgrid

def _dump_email_to_file(msg, purpose='email'):
    """Guarda el contenido de un EmailMessage a un archivo .eml para debugging."""
    try:
        # Busca el directorio 'static/email_dump' dos niveles arriba del archivo actual
        base = Path(__file__).resolve().parents[1] / 'static' / 'email_dump'
        base.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        filename = base / f"{purpose}_{timestamp}.eml"
        with open(filename, 'wb') as f:
            f.write(msg.as_bytes())
        print(f"[EMAIL_DUMP] Guardado en {filename}")
        return True
    except Exception as e:
        print(f"[EMAIL_DUMP] Error guardando email: {e}")
        return False

# =========================================================================
# 3. OBTENCIÓN CENTRALIZADA DE VARIABLES
# =========================================================================

def _get_email_settings():
    """Obtiene las variables de entorno necesarias. Devuelve None si faltan críticas."""
    settings = {
        'remitente': os.getenv('SMTP_EMAIL'),
        'password': os.getenv('SMTP_PASSWORD'),
        'smtp_server': os.getenv('SMTP_SERVER'),
        'smtp_port': int(os.getenv('SMTP_PORT', '465')), # Puerto 465 por defecto para SSL
        # SMTP_USERNAME puede ser el mismo que SMTP_EMAIL si no se especifica.
        'smtp_username': os.getenv('SMTP_USERNAME', os.getenv('SMTP_EMAIL', '')),
        # 'sendgrid_api_key': os.getenv('SENDGRID_API_KEY') # ELIMINADA
    }
    
    # Chequeo mínimo: Solo necesitamos credenciales SMTP completas.
    has_smtp_creds = settings['remitente'] and settings['password'] and settings['smtp_server']
    
    if not has_smtp_creds:
        print("[EMAIL_SETUP] Faltan variables críticas (SMTP_EMAIL/PASSWORD/SERVER).")
        return None
        
    return settings

# =========================================================================
# 4. FUNCIONES DE ALTO NIVEL (USO) - Lógica de envío simplificada
# =========================================================================

def _send_email_message(destinatario, asunto, texto, html, attachments=None, purpose='general'):
    """Helper para crear y enviar el EmailMessage, ahora el único método de envío."""
    settings = _get_email_settings()
    if not settings: return False

    msg = EmailMessage()
    msg.set_content(texto)
    msg.add_alternative(html, subtype='html')
    msg['Subject'] = asunto
    msg['From'] = settings['remitente']
    msg['To'] = destinatario
    
    # Manejar adjuntos para SMTP
    if attachments:
        for attachment_info in attachments:
            try:
                # Los bytes del archivo ya están en pdf_bytes
                msg.add_attachment(
                    attachment_info['file_bytes'], 
                    maintype=attachment_info['file_type'].split('/')[0], 
                    subtype=attachment_info['file_type'].split('/')[1], 
                    filename=attachment_info['filename']
                )
            except Exception as e:
                print(f'[{purpose.upper()}] Error adjuntando archivo a EmaiMessage: {e}')

    sent = _send_message_smtp(
        settings['remitente'], 
        settings['smtp_username'], 
        settings['password'], 
        settings['smtp_server'], 
        settings['smtp_port'], 
        msg
    )
    
    if sent:
        print(f"[{purpose.upper()}] Enviado OK a {destinatario}")
    else:
        print(f"[{purpose.upper()}] Error enviando correo a {destinatario} - volcando a disco")
        _dump_email_to_file(msg, purpose=purpose)
        
    return sent


# --- Funciones de uso modificadas ---

def enviar_alerta_stock(destinatario, producto, cantidad):
    asunto = "¡Atención! Stock bajo en JosniShop"
    texto = f"Producto: {producto}\nQuedan {cantidad} unidades."

    html = HTML_EMAIL_TEMPLATE.format(
        title="¡Atención! Stock bajo",
        intro=f"El producto <strong>{producto}</strong> está por agotarse.",
        content=f"<p>Actualmente solo quedan <strong>{cantidad}</strong> unidades disponibles.</p>",
        footer="Revisa el inventario en tu panel de control.",
        button_html=""
    )
    return _send_email_message(destinatario, asunto, texto, html, purpose='alerta_stock')


def enviar_confirmacion_compra(correo, pedido_id, pdf_bytes=None, filename=None):
    asunto = "¡Gracias por tu compra en JosniShop!"
    texto = f"Tu compra ha sido confirmada. Pedido: {pedido_id}.\nDescarga la factura adjunta para tener un respaldo de tu compra."

    pdf_info = "<p><strong>📎 Factura adjunta:</strong> Hemos incluido tu comprobante de compra en formato PDF. Descárgalo y guárdalo como respaldo.</p>" if pdf_bytes else ""

    html = HTML_EMAIL_TEMPLATE.format(
        title="¡Gracias por tu compra!",
        intro=f"Hemos confirmado tu compra. <strong>Pedido #{pedido_id}</strong>",
        content=f"<p>Tu compra ha sido procesada exitosamente.</p>{pdf_info}<p>En breve recibirás actualizaciones sobre el estado de tu pedido.</p>",
        footer="Puedes consultar el estado de tu pedido en tu panel de usuario. Gracias por confiar en JosniShop.",
        button_html=""
    )
    
    attachments = None
    if pdf_bytes:
        if not filename: filename = f'factura_pedido_{pedido_id}.pdf'
        attachments = [{
            'filename': filename,
            'file_bytes': pdf_bytes,
            'file_type': 'application/pdf'
        }]
        print(f'[CONFIRMACION_COMPRA] PDF adjuntado: {filename} ({len(pdf_bytes)} bytes)')

    return _send_email_message(correo, asunto, texto, html, attachments=attachments, purpose='confirmacion_compra')


def send_registration_email(to_email):
    subject = "Registro exitoso en JosniShop"
    texto = "Te has registrado exitosamente en JosniShop."

    html = HTML_EMAIL_TEMPLATE.format(
        title="¡Bienvenido!",
        intro="Has registrado tu cuenta en JosniShop.",
        content="<p>Gracias por confiar en nosotros.</p>",
        footer="Disfruta de la experiencia de compra.",
        button_html=""
    )
    return _send_email_message(to_email, subject, texto, html, purpose='registration')


def enviar_alerta_resena(destinatario, producto, comentario, calificacion):
    asunto = "¡Nueva reseña en tu producto JosniShop!"
    texto = f"Nueva reseña en {producto}: {calificacion} estrellas."

    html = HTML_EMAIL_TEMPLATE.format(
        title="Nueva reseña recibida",
        intro=f"Tu producto <strong>{producto}</strong> recibió una nueva reseña.",
        content=f"<p><strong>Calificación:</strong> {calificacion} estrellas</p><p><strong>Comentario:</strong> {comentario}</p>",
        footer="Revisa tu panel para responder o gestionar la reseña.",
        button_html=""
    )
    return _send_email_message(destinatario, asunto, texto, html, purpose='alerta_resena')


def enviar_respuesta_resena(destinatario, producto, respuesta_vendedor):
    asunto = "Tu reseña ha recibido una respuesta en JosniShop"
    texto = f"Tu reseña sobre {producto} ha sido respondida."

    html = HTML_EMAIL_TEMPLATE.format(
        title="Respuesta a tu reseña",
        intro=f"Tu reseña sobre <strong>{producto}</strong> ha sido respondida.",
        content=f"<p>{respuesta_vendedor}</p>",
        footer="Puedes ver la conversación en tu panel de usuario.",
        button_html=""
    )
    return _send_email_message(destinatario, asunto, texto, html, purpose='respuesta_resena')


def enviar_cambio_estado_pedido(correo, pedido_id, nuevo_estado):
    asunto = f"Actualización de estado del pedido #{pedido_id}"
    texto = f"El estado de tu pedido #{pedido_id} ha cambiado a: {nuevo_estado}."

    html = HTML_EMAIL_TEMPLATE.format(
        title="Cambio de estado de pedido",
        intro=f"Tu pedido <strong>#{pedido_id}</strong> cambió de estado.",
        content=f"<p>Nuevo estado: <strong>{nuevo_estado}</strong></p>",
        footer="Consulta más detalles en tu panel de usuario.",
        button_html=""
    )
    return _send_email_message(correo, asunto, texto, html, purpose='estado_pedido')


def enviar_recuperacion_contrasena(destinatario, nueva_contrasena):
    settings = _get_email_settings()
    if not settings: return False

    asunto = "Recuperación de contraseña - JosniShop"
    texto = f"Tu nueva contraseña temporal es: {nueva_contrasena}"

    frontend_url = os.getenv('FRONTEND_URL', '')
    if frontend_url:
        button = f"<a href=\"{frontend_url}\" style=\"display:inline-block;padding:12px 18px;background:#d32f2f;color:#fff;border-radius:6px;text-decoration:none;font-weight:600;\">Ir a JosniShop</a>"
    else:
        button = ""

    # Password highlighted block
    pwd_block = f"<div style=\"font-family:monospace;background:#0f1724;color:#fff;display:inline-block;padding:10px 14px;border-radius:6px;font-size:18px;letter-spacing:1px;\">{nueva_contrasena}</div>"

    html = HTML_EMAIL_TEMPLATE.format(
        title="Recuperación de contraseña",
        intro="Hemos recibido una solicitud para recuperar tu contraseña.",
        content=(
            f"<p>Tu nueva contraseña temporal es:</p>"
            f"<div style='margin:12px 0'>{pwd_block}</div>"
            "<h3 style='margin-top:18px;color:#374151;'>Instrucciones:</h3>"
            "<ol style='color:#6b7280;margin-left:18px;'>"
            "<li>Inicia sesión con tu correo y esta contraseña temporal</li>"
            "<li>Dirígete a tu panel de control</li>"
            "<li>Cambia esta contraseña temporal por una que recuerdes fácilmente</li>"
            "</ol>"
            "<p style='margin-top:12px;'><strong>Importante:</strong> Esta contraseña temporal es válida por un acceso. Por favor, cámbiala inmediatamente después de iniciar sesión.</p>"
        ),
        footer="",
        button_html=button
    )

    print(f"[ENVIAR_RECUPERACION] Para={destinatario} | Asunto={asunto} | SMTP={settings['smtp_server']}:{settings['smtp_port']}")
    
    return _send_email_message(destinatario, asunto, texto, html, purpose='recuperacion')
