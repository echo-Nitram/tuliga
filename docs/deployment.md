# Despliegue móvil

Esta guía explica cómo instalar las dependencias del proyecto y realizar pruebas en entornos móviles, ya sea como PWA o mediante un cliente React Native.

## Instalación

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi sqlalchemy httpx stripe mercadopago
```

### Frontend Web/PWA

```bash
cd frontend
npm install
```

Si se opta por una PWA dentro del mismo repositorio, crear una carpeta `frontend/pwa/` reutilizando los componentes existentes.

### Cliente React Native

Si se prefiere un proyecto móvil nativo, generar un proyecto con **Expo** en un repositorio aparte y consumir los mismos endpoints de autenticación y fixtures.

## Pruebas móviles

### Progresive Web App

```bash
cd frontend
npm run build
npm run start
# luego abrir http://localhost:3000 en el navegador y usar las herramientas de desarrollo móviles
```

### React Native

```bash
cd ../app-nativa
npm install
npx expo start
# Escanear el código QR con la app de Expo para probar en un dispositivo físico
```

Tanto la PWA como el cliente React Native pueden reutilizar los endpoints existentes de autenticación y fixtures del backend.

## Variables de entorno

Configura las credenciales necesarias para los proveedores de pago y de la API de fútbol creando un archivo `.env` basado en `.env.example`.

Sin `API_FOOTBALL_KEY` el backend no podrá comunicarse con la API externa y se detendrá al iniciar.

```bash
API_FOOTBALL_KEY=tu_clave_de_api_football
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLIC_KEY=pk_live_...
MERCADOPAGO_ACCESS_TOKEN=APP_USR-...
MERCADOPAGO_PUBLIC_KEY=TEST-...
```

## Consideraciones de producción

- Usa las claves de producción proporcionadas por cada servicio.
- Asegura los endpoints HTTPS y configura los webhooks de notificación de pagos.
- Maneja los errores de los SDKs y registra los intentos fallidos para poder reintentarlos.
