# 👁️ Sistema de Gestión de Óptica

[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

Este sistema es una solución de software diseñada para la **transformación digital** de pequeñas ópticas independientes. El proyecto sustituye los sistemas tradicionales descentralizados y fragmentados (como las hojas de cálculo o los registros en papel) por una **Arquitectura de Sistema y Base de Datos Centralizada**, optimizando el flujo de trabajo clínico y comercial en un único ecosistema digital.

---

## 🎯 Características Principales (Módulos)

El sistema está estructurado bajo la arquitectura **MVT (Model-View-Template)** de Django y cubre los siguientes requisitos funcionales:

- **👥 Gestión Centrada en el Cliente:** Alta, edición y búsqueda avanzada multicanal (búsqueda inteligente por Nombre, Apellidos o DNI mediante objetos `Q`).
- **🩺 Gabinete Clínico & Graduaciones:** Registro de la historia clínica del paciente, vinculando consultas y graduaciones con validaciones técnicas.
- **📦 Inventario y Stock en Tiempo Real:** Control automatizado de existencias de monturas, lentes y líquidos. El sistema resta stock automáticamente al confirmar una venta.
- **🛒 Venta Rápida y Encargos:** Pasarela ágil para facturar productos de mostrador o gestionar encargos asignados a un vendedor específico.
- **🔒 Seguridad y Roles:** Acceso restringido mediante decoradores de Django y herencia de modelos de usuario personalizados (`AbstractUser`) para delimitar funciones de Administradores y Ópticos.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología Utilizada | Función |
|------------|---------------------|----------|
| **Backend** | Python & Django | Lógica de negocio, ORM y enrutamiento seguro. |
| **Base de Datos** | SQLite3 (Desarrollo) / Listo para PostgreSQL | Almacenamiento e integridad referencial de datos. |
| **Frontend** | HTML5, CSS3, Bootstrap 5 | Interfaz de usuario responsiva y componentes `form-control`. |
| **Autenticación** | Django Auth Framework | Control de sesiones y gestión de roles personalizados. |

---

## 🚀 Arquitectura y Buenas Prácticas Técnicas

Para los desarrolladores que revisen el código, destacan las siguientes implementaciones:

- **Desacoplamiento de Modelos:** Uso de `settings.AUTH_USER_MODEL` para referenciar el modelo de usuario personalizado, evitando bloqueos por importación circular.
- **Referencias Perezosas (*Lazy References*):** Uso de relaciones mediante *strings* (`'Usuario'`) para garantizar la flexibilidad en el orden de carga del ORM.
- **Formularios Dinámicos:** Integración de `ModelForm` con personalización de `widgets` para inyectar clases nativas de Bootstrap y formatos de fecha dinámicos.
- **Estrategia de Calidad:** Validación del sistema mediante un enfoque mixto de **Pruebas de Caja Negra** (funcionales y de interfaz) y **Pruebas de Caja Blanca** (inspección de flujo de control y condicionales en vistas).

---

## ⚙️ Instalación y Despliegue Local

Este proyecto incluye scripts automatizados para facilitar su ejecución en entornos Windows. Sigue estos tres sencillos pasos:

### 1. Preparación del Entorno

Si es la primera vez que ejecutas el proyecto, haz doble clic en el archivo automatizado para crear el entorno virtual, instalar las dependencias de Python y ejecutar las migraciones de la base de datos:

```bash
instalar.bat
```

### 2. Lanzamiento del Servidor

Para iniciar el servidor local de desarrollo de Django en ocasiones posteriores, ejecuta:

```bash
iniciar.bat
```

### 3. Acceso al Sistema

Abre tu navegador web preferido e introduce la siguiente dirección:

```http
http://127.0.0.1:8000
```

---

## 🤝 Autor

**Eloy Compés Cruz**  
Desarrollo de Aplicaciones Web (DAW)

- [Mi LinkedIn](https://www.linkedin.com/in/eloycompes/)
- eloycompes@gmail.com

---
