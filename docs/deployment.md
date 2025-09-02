# Despliegue móvil

Esta guía explica cómo instalar las dependencias del proyecto y realizar pruebas en entornos móviles, ya sea como PWA o mediante un cliente React Native.

## Instalación

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi sqlalchemy httpx
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
