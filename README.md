# CreatorApp 🎮

CreatorApp is a feature-rich Django-based turn-based battle game where users can unleash their creativity by designing unique characters, partners, and enemies. Strategize your builds, climb the leaderboard, and engage in epic 2v1 battles!

[**🚀 Try the Live App on Azure**](https://creatorapp-cagtbxfsemaca3bd.spaincentral-01.azurewebsites.net/)

---

## 🌟 Key Features

- **Strategic Turn-Based Combat**: Engage in battles with attacks, heals, and buffs.
- **Full CRUD Management**: Create and customize characters, partners, enemies, and cards.
- **Deep Customization**: Select roles, types, and stats that dynamically impact combat performance.
- **Advanced Battle Mechanics**: 2-vs-1 combat (Character + Partner vs. Enemy) with real-time battle logs.
- **Asynchronous Achievements**: Earn rewards automatically as you meet specific milestones.
- **Social & Competition**: Global leaderboard, user profiles, and inquiry management for admins.
- **Automated Notifications**: Receive detailed battle results via email upon victory.

---

## 📂 Structure Overview

```text
CreatorApp/
├── accounts/           # User authentication, profiles, and battle stats.
├── achievements/       # Async tracking and awarding of user achievements.
├── battle/             # Core combat logic, stat calculation, and battle sessions.
├── cards/              # Cosmetic and functional theme management for creations.
├── characters/         # Character creation and management.
├── common/             # Shared models, mixins, validators, and core site pages.
├── contacts/           # User inquiry system and contact management.
├── CreatorApp/         # Project configuration (settings, middleware, celery).
├── enemies/            # Enemy creation and management.
├── partners/           # Partner creation and management.
├── media/              # Local media storage (Cloudinary used in production).
├── static/             # CSS, JavaScript, and global images.
├── templates/          # Global and app-specific HTML templates.
└── manage.py           # Django management script.
```

---

## 🛠️ Tech Stack & Dependencies

### Core Frameworks
- **Python 3.x**
- **Django 6.0**: The primary web framework.
- **Django REST Framework**: For API capabilities.

### Infrastructure & Storage
- **PostgreSQL**: Production-grade relational database.
- **Cloudinary**: Cloud-based image and media management.
- **WhiteNoise**: Efficient static file serving.

### Asynchronous Processing
- **Celery**: Distributed task queue for background jobs (emails, achievements).
- **Redis**: High-performance message broker and cache.

### Cloud Services (Production)
- **Azure App Service**: Web hosting.
- **Azure Database for PostgreSQL**: Managed database.
- **Azure Cache for Redis**: Managed Redis instance.
- **Azure Communication Services**: Reliable email delivery.

---

## 🚀 Local Setup

Follow these steps to get the project running on your local machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ivanivanov-it/CreatorApp.git
   cd CreatorApp
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory (refer to `.env.example`):
   ```ini
   SECRET_KEY=your_secret_key
   DJANGO_SETTINGS_MODULE=CreatorApp.settings.local
   DEBUG="True"
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_PORT=5432
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=127.0.0.1
   MAINTENANCE="False"
   ```

5. **Initialize Database**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

---

## ☁️ Deployment

The application is architected for **Azure Cloud Services**, ensuring scalability and reliability:

- **Web Hosting**: Deployed on **Azure App Service** (Linux) using Gunicorn.
- **Database**: Utilizes **Azure Database for PostgreSQL (Flexible Server)**.
- **Caching & Tasks**: **Azure Cache for Redis** serves as both the Celery broker and the Django cache backend.
- **Email Service**: Integrated with **Azure Communication Services (Email)** via a custom backend for transactional emails.
- **Security**: Configured with HSTS, SSL redirection, and secure cookie policies in `production.py`.

---

## 🔐 Access Control & Administration

### Administrator Credentials (Testing)
For testing the live application, you can use the following administrator account:
*   **Username:** `admin`
*   **Password:** `admin`

### Security Overview
The application implements strict protection at the **view level**. Access to specific pages and actions is restricted based on user groups and ownership. Even if a user knows the URL to a restricted page, the system will prevent access unless they belong to the required group or have the necessary permissions.

### User Roles & Permissions
Permissions are managed through three primary groups:

#### 1. Moderators
Moderators have elevated administrative rights over game content:
*   **Full CRUD Access:** They can view, create, edit, and delete characters, partners, enemies, and cards belonging to **all users**.
*   **Normal User Comparison:** Standard users can view and create content, but they are restricted to editing or deleting **only their own** creations.

#### 2. BattleManager
This group oversees the combat aspects of the application:
*   **Universal Access:** Users in this group can access the URLs of **all battles** and view the detailed results and logs for any match in the system.
*   **Normal User Restriction:** Users outside of this group are strictly limited to accessing only their own battle results.

#### 3. ContactManagers
This group handles user communication and support:
*   **Inquiry Management:** Members gain access to the dedicated **"Contacts"** page. Here, they can review all messages sent via the contact-us form and resolve user inquiries.
*   **Normal User Restriction:** This page is completely hidden and inaccessible to standard users.

---

## 🧪 Testing

To run the automated test suite:

```bash
# Set environment for local testing
set DJANGO_SETTINGS_MODULE=CreatorApp.settings.local
python manage.py test
```

---
*Built with passion and powered by Django.*
