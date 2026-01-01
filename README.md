# SmartAssist Agriculture Backend API 🌱

## Capstone Project Overview

**SmartAssist Agriculture** is a backend RESTful API developed as a **capstone project** to address real challenges faced by farmers in **conflict-affected and rural regions**, particularly in **eastern Democratic Republic of Congo (DRC)**.

This project focuses on providing **actionable, life‑impacting information** to farmers—not just technical features. It demonstrates how backend engineering can support **agriculture, safety, and resilience** in areas affected by **war, insecurity, and poor road infrastructure**.

The API is designed to be consumed by **mobile or web applications**, enabling farmers and supporting organizations to access critical agricultural and safety data through simple HTTP requests.

---

## 🌍 Real-World Problem Addressed

In many rural and conflict-affected regions:

* Farmers lack **reliable weather information**, leading to crop losses
* There is little or no guidance on **what crops to plant and when**
* Roads are often **unsafe due to insecurity or conflict**, putting farmers at risk when traveling to farms or markets
* Information is rarely available in **local languages** understood by farmers

These challenges directly affect **food security, income stability, and personal safety**.

---

## 🎯 Project Objectives (What This Project Achieves)

Through this backend API, I successfully built a system that:

* Provides **weather forecasts** to help farmers plan farming activities
* Offers **crop and planting calendar data** to guide seasonal decisions
* Stores and exposes **safe and unsafe route information** to improve farmer movement and safety
* Supports **local language readiness** (Swahili) for accessibility
* Demonstrates secure and scalable **user authentication and data access**

This project does not claim to solve conflict—but it **reduces risk and uncertainty** by making critical information accessible.

---

## ✅ Implemented Core Features (MVP)

### 🔐 User Management & Security

* User registration and login
* Token-based authentication (JWT / DRF Tokens)
* Secure access to protected endpoints
* Admin and normal user separation

### 🌦 Weather Information Module

* Integration with a third‑party weather API
* Daily and weekly weather forecasts
* Structured API responses suitable for frontend/mobile consumption

### 🌱 Crop Guide & Planting Calendar

* CRUD operations for crops
* Planting calendar records with recommended seasons
* Centralized agricultural knowledge accessible via API

### 🗺 Safety & Road Awareness (Conflict Context)

* CRUD operations for **danger zones** using latitude and longitude
* CRUD operations for **safe routes**
* Ability to return nearby safe or unsafe zones based on coordinates

➡️ This feature is particularly important in **war‑affected areas**, where knowing which roads are dangerous can prevent harm.

### 🌍 Language Support

* Designed with **Swahili support** in mind
* Extendable to additional local languages

---

## 🛠 Technologies Used

| Component            | Technology                                           |
| -------------------- | ---------------------------------------------------- |
| Backend Framework    | Django REST Framework                                |
| Programming Language | Python                                               |
| Database             | SQLite (development) / PostgreSQL (production-ready) |
| Authentication       | JWT / Token Authentication                           |
| External APIs        | Weather API (e.g., OpenWeather)                      |
| Version Control      | Git & GitHub                                         |
| Documentation        | README.md                                            |

---

## 🧩 Backend Design (Part 2)

### 1. Entity Relationship Diagram (ERD)

The backend is designed around a **relational database model** that reflects real agricultural activities and safety considerations.

**Main Entities:**

* **User** – authentication and system access
* **Farmer** – farmer profile linked to a user
* **Field** – agricultural fields owned or managed by farmers
* **Crop** – crop reference data
* **PlantingCalendar** – seasonal planting schedules linked to crops
* **WeatherRecord** – stored weather data per location/date
* **SafeRoute** – safe travel routes
* **DangerZone** – unsafe areas defined by coordinates

**Relationships:**

* One **User** → One **Farmer** (OneToOne)
* One **Farmer** → Many **Fields** (OneToMany)
* One **Crop** → Many **PlantingCalendar** entries (OneToMany)
* Routes and danger zones use **geographic coordinates** for proximity queries

This ERD design ensures **data consistency**, **scalability**, and **clear separation of concerns**.

---

### 2. API Endpoints

All endpoints follow **REST conventions**, use proper HTTP verbs, and return meaningful status codes.

#### 🔐 Users

| Method | Endpoint       | Description         |
| ------ | -------------- | ------------------- |
| GET    | /api/users     | Get all users       |
| POST   | /api/users     | Create a new user   |
| GET    | /api/users/:id | Get a specific user |
| PUT    | /api/users/:id | Update user info    |
| DELETE | /api/users/:id | Delete user         |

#### 👨‍🌾 Farmers

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| GET    | /api/farmers     | List all farmers      |
| POST   | /api/farmers     | Create farmer profile |
| GET    | /api/farmers/:id | View single farmer    |
| PUT    | /api/farmers/:id | Update farmer         |
| DELETE | /api/farmers/:id | Delete farmer         |

#### 🌾 Fields

| Method | Endpoint        | Description       |
| ------ | --------------- | ----------------- |
| GET    | /api/fields     | List fields       |
| POST   | /api/fields     | Create field      |
| GET    | /api/fields/:id | Get field details |
| PUT    | /api/fields/:id | Update field      |
| DELETE | /api/fields/:id | Delete field      |

#### 🌱 Crops

| Method | Endpoint       | Description  |
| ------ | -------------- | ------------ |
| GET    | /api/crops     | List crops   |
| POST   | /api/crops     | Add new crop |
| GET    | /api/crops/:id | Get crop     |
| PUT    | /api/crops/:id | Update crop  |
| DELETE | /api/crops/:id | Delete crop  |

#### 🌦 Weather Records

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | /api/weather     | Get weather records  |
| POST   | /api/weather     | Add weather info     |
| GET    | /api/weather/:id | Single weather entry |

#### 🛣 Safe Routes

| Method | Endpoint    | Description      |
| ------ | ----------- | ---------------- |
| GET    | /api/routes | List safe routes |
| POST   | /api/routes | Add safe route   |

#### 📅 Planting Calendar

| Method | Endpoint      | Description            |
| ------ | ------------- | ---------------------- |
| GET    | /api/calendar | Get planting schedules |
| POST   | /api/calendar | Add planting schedule  |

---

## 🧭 View & API Design Rationale (How the System Is Used)

This section explains **how each core model is exposed and used through the API**, and how it supports real farming activities. The design follows a **clean CRUD pattern**, with additional filtering, searching, and relationships to make the data practical for farmers and administrators.

---

### 1️⃣ Farmer

**Purpose:** Represents a user practicing farming. It is the central entity that connects land, crops, and activity.

**API Capabilities:**

* **List** – View all farmers, with optional search and filters (e.g., region, active status)
* **Detail** – View an individual farmer, including their fields and crops
* **Create / Update** – Add or edit farmer profiles (restricted to admin)
* **Delete** – Remove a farmer (admin-only)

**Design Options:**

* Search by username or region
* Filter by active/inactive status
* Navigation links to related fields and crops

➡️ This allows organizations or admins to **manage farmer data centrally**, even in unstable regions.

---

### 2️⃣ Field

**Purpose:** Represents plots of land owned or managed by a farmer.

**API Capabilities:**

* **List** – View all fields or filter by farmer, soil type, or size
* **Detail** – View field details and crops planted on it
* **Create / Update** – Add or edit field information
* **Delete** – Remove a field

**Design Options:**

* Filter by soil type or field size
* Link each field to its owner (farmer)
* Display crops associated with a field

➡️ This helps track **land usage and productivity**, which is critical for planning.

---

### 3️⃣ Crop

**Purpose:** Represents a specific crop grown in a field.

**API Capabilities:**

* **List** – View all crops, filterable by status (planted, growing, ready, harvested)
* **Detail** – View crop details such as field, planting date, expected harvest date, and status
* **Create / Update** – Add or update crop records
* **Delete** – Remove a crop

**Design Options:**

* Filter by status, planted date, expected harvest date, or field
* Sort by planting date or harvest readiness
* Admin-only bulk actions (e.g., mark crops as harvested)

➡️ This enables **crop lifecycle tracking**, improving yield planning and timing.

---

### 4️⃣ Planting Calendar

**Purpose:** Tracks planned planting and harvest schedules for crops and fields.

**API Capabilities:**

* **List** – View all planting schedules, sortable by date, crop, or field
* **Detail** – View a specific schedule (crop, field, planting date, harvest date)
* **Create / Update** – Add or modify schedules
* **Delete** – Remove a schedule

**Design Options:**

* Filter by field or crop
* Date-based navigation (seasonal view)
* Highlight upcoming planting or harvest periods

➡️ This feature helps farmers **anticipate activities**, even with limited access to extension services.

---

### 5️⃣ WeatherRecord

**Purpose:** Stores weather data associated with a field or location.

**API Capabilities:**

* **List** – View all weather records, filterable by field or date
* **Detail** – View a single weather entry
* **Create / Update** – Add or edit weather records (manual or API-fed)
* **Delete** – Remove a weather record

**Design Options:**

* Filter by field, date, or conditions (e.g., rainfall > threshold)
* Sort by most recent records

➡️ Weather data supports **risk reduction**, especially in unpredictable climates.

---

### 🔁 Common View Patterns Across All Models

All models follow a consistent design:

* **Create** – Add new records
* **Retrieve** – List and detail views
* **Update** – Modify existing records
* **Delete** – Remove records

**Enhanced Capabilities:**

* Filtering & searching by relationships, dates, and status
* Sorting and ordering for usability
* Navigation between related resources (Farmer → Field → Crop)

This consistent API design makes the system **easy to extend**, **secure**, and **frontend-friendly**.

---

## 🧬 Serializer Design & Data Security Strategy

This project uses **multiple serializers per model** to enforce **security, performance, and clarity**. Each serializer is designed for a specific use case (list, detail, create, update), preventing data leakage and ensuring proper validation.

---

### 1️⃣ Farmer (Custom User Model)

**Use cases:** signup, profile display, profile update

| Serializer             | Purpose        | Fields                                                                          | Notes                             |
| ---------------------- | -------------- | ------------------------------------------------------------------------------- | --------------------------------- |
| FarmerListSerializer   | List farmers   | id, username, farm_name, city_or_region                                         | Lightweight, hides sensitive data |
| FarmerDetailSerializer | Profile detail | username, first_name, last_name, email, phone_number, farm_name, city_or_region | Read-only (GET only)              |
| FarmerCreateSerializer | Signup         | username, email, farm_name, phone_number, password                              | Password is write-only & hashed   |
| FarmerUpdateSerializer | Update profile | first_name, last_name, email, phone_number, farm_name, city_or_region           | Partial updates allowed           |

➡️ This separation prevents exposure of sensitive information and enforces **safe authentication flows**.

---

### 2️⃣ Field

**Use cases:** list, detail, create, update, delete

| Serializer            | Purpose      | Fields                                        | Notes                |
| --------------------- | ------------ | --------------------------------------------- | -------------------- |
| FieldListSerializer   | List fields  | id, name, size_in_hectares, soil_type         | Lightweight          |
| FieldDetailSerializer | Detail view  | id, name, size_in_hectares, soil_type, farmer | Farmer is read-only  |
| FieldCreateSerializer | Create field | name, size_in_hectares, soil_type             | Farmer auto-assigned |
| FieldUpdateSerializer | Update field | name, size_in_hectares, soil_type             | Only editable fields |

➡️ Fields are always linked to a farmer, ensuring **ownership and traceability**.

---

### 3️⃣ Crop

**Use cases:** list, detail, create, update, delete

| Serializer           | Purpose     | Fields                                                                    | Notes                              |
| -------------------- | ----------- | ------------------------------------------------------------------------- | ---------------------------------- |
| CropListSerializer   | List crops  | id, name, status, expected_harvest                                        | Optimized for dashboards           |
| CropDetailSerializer | Detail view | All fields incl. field                                                    | Read-only (GET only)               |
| CropCreateSerializer | Create crop | name, description, category, fields, planted_on, expected_harvest, status | Validates field ownership          |
| CropUpdateSerializer | Update crop | Same as create                                                            | Partial updates, enforce ownership |

➡️ Ownership validation ensures farmers **cannot access or modify others’ data**.

---

### 4️⃣ Activity (Planting Calendar)

**Purpose:** Manages planting and harvest schedules

| Serializer               | Purpose         | Fields                                                             | Notes                      |
| ------------------------ | --------------- | ------------------------------------------------------------------ | -------------------------- |
| ActivityListSerializer   | List activities | id, title, field, scheduled_date, status                           | Minimal info               |
| ActivityDetailSerializer | Detail view     | All fields (crop, estimated_harvest_date, description)             | Read-only                  |
| ActivityCreateSerializer | Create schedule | title, field, scheduled_date, status, estimated_harvest_date, crop | Validates farmer ownership |
| ActivityUpdateSerializer | Update schedule | Same as create                                                     | Partial updates allowed    |

➡️ This supports **seasonal planning**, even in unstable environments.

---

### 5️⃣ WeatherRecord

**Purpose:** Stores historical and live weather data

| Serializer                    | Purpose       | Fields                                                                            | Notes                   |
| ----------------------------- | ------------- | --------------------------------------------------------------------------------- | ----------------------- |
| WeatherRecordListSerializer   | List records  | id, recorded_at, location, temperature, humidity, rainfall                        | Lightweight             |
| WeatherRecordDetailSerializer | Detail view   | All fields incl. field, farmer, wind_speed, source                                | Read-only               |
| WeatherRecordCreateSerializer | Create record | recorded_at, field, location, temperature, humidity, rainfall, wind_speed, source | Farmer auto-assigned    |
| WeatherRecordUpdateSerializer | Update record | Same as create                                                                    | Partial updates allowed |

➡️ Weather data is structured for **risk analysis and forecasting support**.

---

### 6️⃣ SecureRoute

**Purpose:** Represents safe and unsafe travel routes in conflict-affected areas

| Serializer                  | Purpose      | Fields                                                      | Notes                   |
| --------------------------- | ------------ | ----------------------------------------------------------- | ----------------------- |
| SecureRouteListSerializer   | List routes  | id, route_name, security_status                             | Lightweight             |
| SecureRouteDetailSerializer | Detail view  | All fields (route_path_geojson, risk_notes, last_updated)   | Read-only               |
| SecureRouteCreateSerializer | Create route | route_name, route_path_geojson, security_status, risk_notes | Farmer auto-assigned    |
| SecureRouteUpdateSerializer | Update route | Same as create                                              | Partial updates allowed |

➡️ This module directly supports **farmer safety in insecure regions**.

---

## 🧱 System Design & Engineering Practices

* RESTful API design using proper HTTP verbs (GET, POST, PUT, DELETE)
* Meaningful HTTP status codes (200, 201, 400, 401, 403, 404, 500)
* Modular Django app structure
* Clean serializers and viewsets
* Proper relational database design (Users, Crops, Weather, Routes, Danger Zones)
* Error handling with custom responses
* Logging using Python’s logging module

---

## 🧪 Development Process & Version Control

* Regular commits with clear messages (feature, fix, refactor)
* Progressive feature development
* No single bulk commit
* Git history reflects planning, implementation, and refinement

---

## 🚀 Installation & Local Setup

```bash
git clone https://github.com/rolandslt/smart_assist_agriculture.git
cd smart_assist_agriculture

python -m venv env
# Windows
env\\Scripts\\activate
# Linux / Mac
source env/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🎥 Capstone Video Demonstration

The project is demonstrated in a **5‑minute capstone video**, covering:

1. Problem context (agriculture + insecurity)
2. API architecture
3. Authentication flow
4. Core features demonstration
5. Real‑world impact and limitations

---

## 🔮 Future Improvements

* Offline data synchronization
* Push notifications for weather and security alerts
* AI‑based crop disease detection
* Farmer‑to‑farmer communication
* Farm expense and yield tracking

---

## 👤 Author

**Lulando Roland**
Backend Developer | Software Engineering Student

---

## 📄 License

This project was developed for **educational purposes** as part of a capstone requirement, with a strong focus on **real‑world impact** for farming communities.
