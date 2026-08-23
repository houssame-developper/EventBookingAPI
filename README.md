# Event Booking API

![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

A modern, async REST API for event booking management built with **FastAPI**, **SQLModel**, and **PostgreSQL**. It provides secure authentication, role-based access control, rate limiting, and comprehensive testing coverage.

---

## Table of Contents

1. [About the Project](#about-the-project)
2. [Tech Stack & Tools](#tech-stack--tools)
3. [Database](#database)
4. [AI Assistance Disclaimer](#ai-assistance-disclaimer)
5. [Getting Started](#getting-started)
6. [Project Structure](#project-structure)
7. [Testing](#testing)
8. [License](#license)

---

## About the Project

**Event Booking API** is a production-ready backend service designed to manage event bookings with a focus on security, performance, and scalability. The API enables users to register, authenticate, browse events, and make bookings, while administrators can manage users, events, and monitor the system.

### Core Features

- **User Authentication & Authorization**: JWT-based access tokens and HTTP-only refresh tokens with role-based access control (`ADMIN` / `USER`).
- **Event Management**: Full CRUD operations for events with slot reservation tracking and soft deletes.
- **Booking System**: Users can book events with automatic slot counting and availability validation.
- **Rate Limiting**: SlowAPI-powered rate limiting to protect endpoints from abuse.
- **CORS Support**: Configured for cross-origin requests with secure cookie handling.
- **Comprehensive Testing**: Integration and API test suites with fixtures, factories, and permission coverage.

### Project Goals

- Provide a clean, async-first API architecture using modern Python tooling.
- Ensure secure authentication flows with proper token management.
- Deliver a maintainable codebase with repository pattern, service layer separation, and Pydantic schema validation.
- Enable reliable database migrations and testing workflows via Docker.

---

## Tech Stack & Tools

### Backend Framework
- **FastAPI** — Modern, high-performance async web framework
- **Uvicorn** — ASGI server for running the application

### Database & ORM
- **PostgreSQL 18** — Primary relational database
- **SQLModel** — SQLAlchemy-based ORM with Pydantic validation
- **asyncpg** — Async PostgreSQL driver
- **Alembic** — Database schema migration tool

### Authentication & Security
- **PyJWT** — JSON Web Token generation and verification
- **pwdlib + bcrypt** — Password hashing and verification
- **python-multipart** — Form data parsing (for OAuth2 password flow compatibility)

### Testing & Quality
- **pytest** — Test framework
- **pytest-asyncio** — Async test support
- **httpx** — Async HTTP client for API testing
- **polyfactory** — Test data factories for Pydantic models

### Containerization & DevOps
- **Docker** — Container runtime
- **Docker Compose** — Multi-container orchestration (app + PostgreSQL + test database)

### Other Libraries
- **slowapi** — Rate limiting middleware
- **python-dotenv** — Environment variable management
- **pydantic** — Data validation and settings management

---

## Database

### Database Engine
- **PostgreSQL 18.4** (running in Docker)
- Two isolated database containers:
  - `db` — Main application database (`mydatabase`)
  - `testdb` — Dedicated test database (`testdb`)

### ORM & Models
- **SQLModel** is used as the primary ORM, built on top of SQLAlchemy 2.0 and Pydantic v2.
- All database models are defined in `app/models.py`:
  - `User` — Stores user accounts with soft delete support (`deleted_at`)
  - `Event` — Stores event details with slot management (`total_slots`, `reserved_slots`)
  - `Booking` — Association table linking users to events with booking timestamps

### Migrations
- **Alembic** is configured for schema versioning and migrations.
- Migration scripts are stored in `app/migrations/versions/`.
- The `env.py` is configured for async migration execution.
- Database URL is injected dynamically via environment variables.

### Key Database Features
- **Soft deletes** via `deleted_at` timestamp columns
- **Check constraints** for data integrity (e.g., `total_slots >= 1`)
- **Server defaults** for `created_at` and `updated_at` timestamps
- **Foreign key constraints** with `ON DELETE RESTRICT` for referential integrity

---

## AI Assistance Disclaimer

> **Important**: This project was primarily developed through my own architectural design, core logic implementation, and coding efforts. The codebase structure, business logic, authentication flows, database schema design, and main feature implementations are entirely my original work.

Artificial Intelligence tools were utilized strictly as an **assistant** in the following limited capacities:
- Generating repetitive boilerplate code (e.g., CRUD operations, test fixtures)
- Troubleshooting complex integration issues between tools (e.g., async event loop conflicts between `pytest-asyncio`, `asyncpg`, and SQLAlchemy)
- Assisting with deep research on unfamiliar technical bugs and framework-specific behaviors
- Suggesting best practices for testing patterns and error handling

All AI-generated suggestions were reviewed, validated, and adapted by me to ensure they aligned with the project's architecture and quality standards.

---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.14+ (for local development without Docker)

### Environment Variables

Create a `.env` file in the project root:

```env
# PostgreSQL Configuration
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword123
POSTGRES_DB=mydatabase
POSTGRES_PORT=5432

# FastAPI Configuration
DATABASE_URL=postgresql+asyncpg://myuser:mypassword123@db:5432/mydatabase
TEST_DATABASE_URL=postgresql+asyncpg://myuser:mypassword123@testdb:5432/testdb
TEST_POSTGRES_DB=testdb

# Security
SECRET_KEY=your-secret-key-here
TIME_EXPIRE_ACCESS_TOKEN=300
TIME_EXPIRE_REFRESH_TOKEN=2592000
```

### Running with Docker

```bash
# Start all services (app + databases)
docker-compose up -d --build

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
cd app
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

---

## Project Structure

```
eventHorz/
├── .env                          # Environment variables
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Container build definition
├── requirements.txt              # Python dependencies
└── app/
    ├── main.py                   # FastAPI application entry point
    ├── alembic.ini               # Alembic configuration
    ├── config/
    │   ├── auth_utils.py         # JWT, password hashing, token utilities
    │   ├── database.py           # SQLAlchemy async engine & session factory
    │   ├── limiter.py            # Rate limiting configuration
    │   └── settings.py           # Application settings
    ├── migrations/
    │   ├── env.py                # Alembic async environment
    │   └── versions/             # Migration scripts
    ├── models.py                 # SQLModel database models
    ├── routes/
    │   ├── auth_routes.py        # Authentication endpoints
    │   ├── user_routes.py        # User management endpoints
    │   ├── event_routes.py       # Event management endpoints
    │   └── booking_routes.py     # Booking endpoints
    ├── schemas/
    │   ├── user_schema.py        # User Pydantic schemas
    │   └── event_schema.py       # Event & Booking Pydantic schemas
    ├── service/
    │   ├── auth_service.py       # Authentication business logic
    │   ├── user_service.py       # User business logic
    │   └── event_service.py      # Event & Booking business logic
    ├── repositories/
    │   ├── base_repo.py          # Generic repository pattern
    │   ├── user_repo.py          # User database operations
    │   ├── event_repo.py         # Event database operations
    │   └── booking_repo.py       # Booking database operations
    └── tests/
        ├── conftest.py           # Shared test fixtures
        ├── constants.py           # Test factories and constants
        ├── integration/           # Integration tests (repositories)
        ├── api/                   # API endpoint tests
        └── unit/                  # Unit tests (services, auth)
```

---

## Testing

### Test Structure
- **Unit Tests** (`tests/unit/`) — Test services and auth utilities in isolation with mocked repositories
- **Integration Tests** (`tests/integration/`) — Test repository layer against a real PostgreSQL database
- **API Tests** (`tests/api/`) — Test all HTTP endpoints with authentication, permissions, and edge cases

### Running Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test suites
docker-compose exec backend pytest tests/integration -v
docker-compose exec backend pytest tests/api -v
docker-compose exec backend pytest tests/unit -v

# Run with markers
docker-compose exec backend pytest -m integration -v
docker-compose exec backend pytest -m api -v
docker-compose exec backend pytest -m unit -v
```

### Test Coverage
- Repository CRUD operations for `User`, `Event`, and `Booking`
- Authentication flows: register, login, refresh token, logout
- Permission checks: admin-only endpoints, authenticated endpoints, public endpoints
- Edge cases: deleted users, duplicate emails, wrong passwords, missing tokens
- Rate limiting behavior
- CORS and cookie handling

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## ⬇️ Arabic Version (النسخة العربية)

---

# واجهة برمجة تطبيقات حجز الفعاليات

![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

واجهة برمجة تطبيقات REST حديثة وغير متزامنة (async) لإدارة حجز الفعاليات، مبنية باستخدام **FastAPI** و **SQLModel** و **PostgreSQL**. توفر الواجهة مصادقة آمنة، تحكم في الصلاحيات، تحديد معدل الطلبات، وتغطية شاملة للاختبارات.

---

## محتويات الدليل

1. [عن المشروع](#about-the-project)
2. [التقنيات والأدوات](#tech-stack--tools)
3. [قاعدة البيانات](#database)
4. [ملاحظة حول استخدام الذكاء الاصطناعي](#ai-assistance-disclaimer)
5. [البدء السريع](#getting-started)
6. [هيكل المشروع](#project-structure)
7. [الاختبارات](#testing)
8. [الترخيص](#license)

---

## عن المشروع

**واجهة برمجة تطبيقات حجز الفعاليات (Event Booking API)** هي خدمة خلفية جاهزة للإنتاج مصممة لإدارة حجز الفعاليات مع التركيز على الأمان والأداء والقابلية للتوسع. تمكن الواجهة المستخدمين من التسجيل والمصادقة وتصفح الفعاليات وإجراء الحجوزات، بينما يمكن للمسؤولين إدارة المستخدمين والفعاليات ومراقبة النظام.

### الميزات الأساسية

- **المصادقة والتفويض**: رموز وصول JWT و رموز منعشة HTTP-only مع تحكم في الصلاحيات (`ADMIN` / `USER`).
- **إدارة الفعاليات**: عمليات CRUD كاملة للفعاليات مع تتبع حجز المقاعد والحذف الناعم (soft delete).
- **نظام الحجوزات**: يمكن للمستخدمين حجز الفعاليات مع حساب تلقائي للمقاعد والتحقق من التوفر.
- **تحديد معدل الطلبات**: حماية نقاط النهاية من الاستخدام المفرط باستخدام SlowAPI.
- **دعم CORS**: مُعد للطلبات من مصادر مختلفة مع التعامل الآمن مع الكوكيز.
- **اختبارات شاملة**: مجموعات اختبارات للتكامل وواجهة برمجة التطبيقات مع-fixtures ومصانع اختبار وتغطية للصلاحيات.

### أهداف المشروع

- توفير بنية API نظيفة وغير متزامنة باستخدام أدوات Python الحديثة.
- ضمان تدفقات مصادقة آمنة مع إدارة مناسبة للرموز.
- تقديم قاعدة بيانات قابلة للصيانة مع نمط Repository وفصل طبقة الخدمة والتحقق من Pydantic.
- تمكين سير عمل موثوق للترحيلات والاختبارات عبر Docker.

---

## التقنيات والأدوات

### إطار العمل الخلفي
- **FastAPI** — إطار عمل ويب حديث وعالي الأداء للواجهات غير المتزامنة
- **Uvicorn** — خادم ASGI لتشغيل التطبيق

### قاعدة البيانات وORM
- **PostgreSQL 18** — قاعدة بيانات علائقية أساسية
- **SQLModel** — ORM مبني على SQLAlchemy 2.0 مع التحقق من Pydantic
- **asyncpg** — مشغل PostgreSQL غير متزامن
- **Alembic** — أداة ترحيل schema قاعدة البيانات

### المصادقة والأمان
- **PyJWT** — توليد والتحقق من JSON Web Tokens
- **pwdlib + bcrypt** — تجزئة والتحقق من كلمات المرور
- **python-multipart** — تحليل بيانات النماذج

### الاختبارات والجودة
- **pytest** — إطار عمل الاختبارات
- **pytest-asyncio** — دعم الاختبارات غير المتزامنة
- **httpx** — عميل HTTP غير متزامن لاختبارات API
- **polyfactory** — مصانع اختبار لنماذج Pydantic
- **Faker** — توليد بيانات وهمية

### الحاويات والعمليات
- **Docker** — وقت تشغيل الحاويات
- **Docker Compose** — تنسيق الحاويات المتعددة (التطبيق + PostgreSQL + قاعدة بيانات الاختبار)

### مكتبات أخرى
- **slowapi** — وسيط تحديد معدل الطلبات
- **python-dotenv** — إدارة متغيرات البيئة
- **pydantic** — التحقق من البيانات وإدارة الإعدادات

---

## قاعدة البيانات

### محرك قاعدة البيانات
- **PostgreSQL 18.4** (يعمل في Docker)
- حاويتان منفصلتان لقاعدة البيانات:
  - `db` — قاعدة بيانات التطبيق الرئيسية (`mydatabase`)
  - `testdb` — قاعدة بيانات اختبار مخصصة (`testdb`)

### ORM والنماذج
- **SQLModel** هو ORM الأساسي، مبني على SQLAlchemy 2.0 و Pydantic v2.
- جميع نماذج قاعدة البيانات معرفة في `app/models.py`:
  - `User` — يخزن حسابات المستخدمين مع دعم الحذف الناعم (`deleted_at`)
  - `Event` — يخزن تفاصيل الفعاليات مع إدارة المقاعد (`total_slots`, `reserved_slots`)
  - `Booking` — جدول ربط بين المستخدمين والفعاليات مع طوابق الحجز

### الترحيلات
- **Alembic** مُعد لإصدارات الـ schema والترحيلات.
- سكريبات الترحيل مخزنة في `app/migrations/versions/`.
- الـ `env.py` مُعد للتنفيذ غير المتزامن للترحيلات.
- عنوان قاعدة البيانات يُدخل ديناميكياً عبر متغيرات البيئة.

### ميزات قاعدة البيانات الرئيسية
- **حذف ناعم** عبر عمود `deleted_at`
- **قيود تحقق (Check Constraints)** لسلامة البيانات (مثال: `total_slots >= 1`)
- **قيم افتراضية للخادم** لأعمدة `created_at` و `updated_at`
- **قيود مفاتيح خارجية** مع `ON DELETE RESTRICT` لسلامة المراجع

---

## ملاحظة حول استخدام الذكاء الاصطناعي

> **هام**: هذا المشروع تم تطويره بشكل أساسي من خلال تصميمي الخاص للبنية المعمارية، وتنفيذ المنطق الأساسي، والبرمجة. بنية الكود، والمنطق التجاري، وتدفقات المصادقة، وتصميم schema قاعدة البيانات، وتطبيقات الميزات الرئيسية هي كلها عمل أصلي مني.

تم استخدام أدوات الذكاء الاصطناعي بشكل صارم كـ **مساعد** في Capacities المحدودة التالية:
- توليد أكواد متكررة ونمطية (مثال: عمليات CRUD، اختبارات fixtures)
- استكشاف أخطاء التكامل المعقدة بين الأدوات (مثال: تعارضات event loop غير المتزامنة بين `pytest-asyncio` و `asyncpg` و SQLAlchemy)
- المساعدة في البحث العميق عن أخطاء تقنية غير مألوفة وسلوكيات الأطر
- اقتراح أفضل الممارسات لأنماط الاختبارات ومعالجة الأخطاء

جميع الاقتراحات التي تم إنشاؤها بالذكاء الاصطناعي تم مراجعتها والتحقق منها وتكييفها من قبلي لضمان توافقها مع بنية المشروع ومعايير الجودة.

---

## البدء السريع

### المتطلبات الأساسية
- Docker و Docker Compose
- Python 3.14+ (للتطوير المحلي بدون Docker)

### متغيرات البيئة

أنشئ ملف `.env` في جذر المشروع:

```env
# PostgreSQL Configuration
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword123
POSTGRES_DB=mydatabase
POSTGRES_PORT=5432

# FastAPI Configuration
DATABASE_URL=postgresql+asyncpg://myuser:mypassword123@db:5432/mydatabase
TEST_DATABASE_URL=postgresql+asyncpg://myuser:mypassword123@testdb:5432/testdb
TEST_POSTGRES_DB=testdb

# Security
SECRET_KEY=your-secret-key-here
TIME_EXPIRE_ACCESS_TOKEN=300
TIME_EXPIRE_REFRESH_TOKEN=2592000
```

### التشغيل باستخدام Docker

```bash
# تشغيل جميع الخدمات (التطبيق + قواعد البيانات)
docker-compose up -d --build

# عرض السجلات
docker-compose logs -f backend

# إيقاف الخدمات
docker-compose down
```

### التطوير المحلي (بدون Docker)

```bash
# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# تثبيت التبعيات
pip install -r requirements.txt

# تشغيل ترحيلات قاعدة البيانات
cd app
alembic upgrade head

# تشغيل الخادم
uvicorn main:app --reload
```

---

## هيكل المشروع

```
eventHorz/
├── .env                          # متغيرات البيئة
├── docker-compose.yml            # إعداد Docker Compose
├── Dockerfile                    # تعريف بناء الحاوية
├── requirements.txt              # تبعيات Python
└── app/
    ├── main.py                   # نقطة دخول تطبيق FastAPI
    ├── alembic.ini               # إعداد Alembic
    ├── config/
    │   ├── auth_utils.py         # JWT، تجزئة كلمات المرور، أدوات الرموز
    │   ├── database.py           # محرك SQLAlchemy غير المتزامن ومصنع الجلسات
    │   ├── limiter.py            # إعداد تحديد معدل الطلبات
    │   └── settings.py           # إعدادات التطبيق
    ├── migrations/
    │   ├── env.py                # بيئة Alembic غير المتزامنة
    │   └── versions/             # سكريبات الترحيل
    ├── models.py                 # نماذج قاعدة البيانات SQLModel
    ├── routes/
    │   ├── auth_routes.py        # نقاط نهاية المصادقة
    │   ├── user_routes.py        # نقاط نهاية إدارة المستخدمين
    │   ├── event_routes.py       # نقاط نهاية إدارة الفعاليات
    │   └── booking_routes.py     # نقاط نهاية الحجوزات
    ├── schemas/
    │   ├── user_schema.py        # مخططات Pydantic للمستخدمين
    │   └── event_schema.py       # مخططات Pydantic للفعاليات والحجوزات
    ├── service/
    │   ├── auth_service.py       # منطق عمل المصادقة
    │   ├── user_service.py       # منطق عمل المستخدمين
    │   └── event_service.py      # منطق عمل الفعاليات والحجوزات
    ├── repositories/
    │   ├── base_repo.py          # نمط Repository العام
    │   ├── user_repo.py          # عمليات قاعدة بيانات المستخدمين
    │   ├── event_repo.py         # عمليات قاعدة بيانات الفعاليات
    │   └── booking_repo.py       # عمليات قاعدة بيانات الحجوزات
    └── tests/
        ├── conftest.py           # اختبارات fixtures مشتركة
        ├── constants.py           # مصانع الاختبار والثوابت
        ├── integration/           # اختبارات التكامل (repositories)
        ├── api/                   # اختبارات نقاط نهاية API
        └── unit/                  # اختبارات الوحدات (services, auth)
```

---

## الاختبارات

### بنية الاختبارات
- **اختبارات الوحدات** (`tests/unit/`) — تختبر الخدمات وأدوات المصادقة بشكل منفصل مع مستودعات وهمية (mocked)
- **اختبارات التكامل** (`tests/integration/`) — تختبر طبقة المستودعات ضد قاعدة PostgreSQL حقيقية
- **اختبارات API** (`tests/api/`) — تختبر جميع نقاط النهاية HTTP مع المصادقة والصلاحيات والحالات الحدية

### تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
docker-compose exec backend pytest

# تشغيل مجموعات اختبار محددة
docker-compose exec backend pytest tests/integration -v
docker-compose exec backend pytest tests/api -v
docker-compose exec backend pytest tests/unit -v

# التشغيل باستخدام العلامات
docker-compose exec backend pytest -m integration -v
docker-compose exec backend pytest -m api -v
docker-compose exec backend pytest -m unit -v
```

### تغطية الاختبارات
- عمليات CRUD للمستودعات: `User`، `Event`، `Booking`
- تدفقات المصادقة: تسجيل، دخول، تحديث الرمز، تسجيل خروج
- فحوصات الصلاحيات: نقاط نهاية للمسؤولين فقط، نقاط نهاية مصادقة، نقاط نهاية عامة
- الحالات الحدية: مستخدمين محذوفين، بريد إلكتروني مكرر، كلمات مرور خاطئة، رموز مفقودة
- سلوك تحديد معدل الطلبات
- التعامل مع CORS والكوكيز

---

## الترخيص

هذا المشروع مرخص بموجب ترخيص MIT. انظر ملف [LICENSE](LICENSE) للتفاصيل.
