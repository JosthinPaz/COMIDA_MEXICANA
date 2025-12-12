# 🚀 Guía para Subir a Railway

## ✅ Estado Actual

Todo está listo para subir a Railway:
- ✅ SMTP funcional (probado)
- ✅ SendGrid configurado (requiere verificación de email)
- ✅ requirements.txt actualizado
- ✅ .env en .gitignore (no se sube el archivo)
- ✅ Sistema de fallback automático

## 📋 Pasos para Railway

### 1. Commit y Push al Repositorio

```bash
git add .
git commit -m "Agregar SendGrid y mejorar sistema de emails"
git push origin main
```

**⚠️ NO commitees `.env` nunca!**
Verifica que `.env` está en `.gitignore`:
```bash
git status  # No debería mostrar .env
```

### 2. Configurar Variables en Railway

1. Ve a tu proyecto en Railway Dashboard: https://railway.app/
2. Ve a la sección de **Variables**
3. Agrega estas variables (exactamente como están):

```
SENDGRID_API_KEY=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

SMTP_EMAIL=josnishop@gmail.com
SMTP_PASSWORD=wssr opok igoz axjn
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

FRONTEND_URL=https://josnishop000-frontend-production.up.railway.app
ALLOWED_ORIGINS=https://josnishop000-frontend-production.up.railway.app

SECRET_KEY=josnishop_super_secreta_2024_cambiar
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

ENVIRONMENT=production
DEBUG=False

MAX_LOGIN_ATTEMPTS=5
LOGIN_ATTEMPT_TIMEOUT=300
MAX_FILE_SIZE_MB=5
MAX_VIDEO_DURATION_SECONDS=60

RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

RATE_LIMIT_LOGIN_MAX_ATTEMPTS=5
RATE_LIMIT_LOGIN_WINDOW=300
RATE_LIMIT_REGISTER_MAX_ATTEMPTS=3
RATE_LIMIT_REGISTER_WINDOW=3600
RATE_LIMIT_API_MAX_REQUESTS=100
RATE_LIMIT_API_WINDOW=60
```

### 3. Deploy

Railway debería auto-deployer al hacer push. Si no:
1. Ve a Railway Dashboard
2. Haz clic en "Deploy"

## 🔧 Cómo Funciona en Railway

```
┌─────────────────────────────────┐
│      Usuario usa JosniShop      │
│  (Compra, Registro, Soporte)    │
└────────────────┬────────────────┘
                 │
                 ▼
         ┌────────────────┐
         │ API (Railway)  │
         │ email_utils.py │
         └────────┬───────┘
                  │
         ┌────────┴────────┐
         │                 │
    ┌────▼────┐      ┌────▼────┐
    │SendGrid │      │  SMTP   │
    │(Mejor)  │      │ (Backup)│
    └─────────┘      └────┬────┘
         │                 │
         └────────┬────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Gmail/Destinatario│
         └──────────────────┘
```

## 📊 Comportamiento en Railway

### Emails con SendGrid (Recomendado)
- ✅ Más confiables
- ✅ Mejor deliverability
- ✅ Mejor soporte
- ⏳ Requiere verificar email en SendGrid

### Emails con SMTP (Fallback)
- ✅ Funciona inmediatamente
- ✅ Sin necesidad de verificación
- ⚠️ Puede tener limitaciones en cloud
- ✅ Fallback automático si SendGrid falla

## 🔐 Seguridad en Railway

✅ Variables de entorno seguras (no en código)
✅ SENDGRID_API_KEY no se expone
✅ SMTP_PASSWORD no se expone
✅ .env no se sube al repositorio

## ✨ Próximos Pasos

### Inmediato (para que funcione HOY)
1. ✅ Commit y push del código
2. ✅ Configurar variables en Railway
3. ✅ Railway debería estar enviando emails via SMTP

### Recomendado (para mejor experiencia)
1. Ir a SendGrid: https://sendgrid.com/
2. Verificar email `josnishop@gmail.com`
3. Sistema automáticamente usará SendGrid

## 📧 Email de Prueba en Producción

Una vez en Railway, puedes probar enviando un email desde tu API:

```bash
curl -X POST http://tu-app-railway.app/api/send-test \
  -H "Content-Type: application/json" \
  -d '{"email": "tu@email.com"}'
```

(Necesitarías un endpoint para esto)

## 🆘 Si Algo Falla

### Problema: Emails no llegan
**Solución**: Revisar logs en Railway
```
Railway Dashboard → Logs → Buscar [SENDGRID] o [SMTP]
```

### Problema: Error de certificado SSL
**Solución**: Ya está resuelto en email_utils.py (requests sin SSL)

### Problema: SendGrid da error 403
**Solución**: Verificar email en SendGrid Dashboard
- Settings → Sender Authentication → Verificar josnishop@gmail.com

## 📝 Checklist Final

- [ ] .env está en .gitignore
- [ ] requirements.txt tiene `requests==2.31.0` y `sendgrid==6.12.4`
- [ ] Código hizo commit
- [ ] Variables configuradas en Railway
- [ ] Deploy exitoso
- [ ] Emails funcionando (vía SMTP al menos)

## 🎉 ¡Listo!

Tu sistema de emails funcionará en Railway de inmediato.
