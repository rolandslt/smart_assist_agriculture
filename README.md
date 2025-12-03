# Capstone Project: Agricultural Support Backend API

## Project Idea
This project is a backend system designed to help farmers access agricultural support through:

- Weather forecasts  
- Planting calendars  
- Crop information  
- Safe and unsafe route mapping  
- Local language support  

The backend is a **RESTful API** consumable by mobile or frontend apps.  
Original idea, customized for rural farming communities in remote areas.  
[More info](https://docs.google.com/presentation/d/1N4rJAzRix98uPZRue-LfD1uU9iE3rkjnn5ADE5i4vTQ/edit?usp=sharing)

---

## Problem Statement
Farmers in many rural regions (eastern DRC) face:

- Lack of predictable weather information  
- No guidance on seasonal crops  
- Unsafe travel in conflict-affected areas  

These issues result in low production, crop losses, and unsafe movement.

---

## Project Objectives
- Provide reliable weather updates based on user location  
- Guide farmers on what to plant each season  
- Improve safety by displaying secure and insecure routes  
- Offer content in languages farmers understand

---

## Core Features (MVP)
- **User Management:** Register, Login, Profile, Authentication tokens  
- **Weather Module:** Fetch data from 3rd-party API, daily & weekly forecasts  
- **Planting Calendar & Crop Guide:** CRUD for crops, planting calendar  
- **Safe Road Mapping:** CRUD for danger zones & safe routes, nearby zones by coordinates  
- **Language Support:** Swahili and optionally other local languages  

---

## Future Features
- Offline data sync  
- Push notifications  
- AI-based crop disease detection  
- Farmer-to-farmer chat  
- Farm expense tracking

---

## Technology Stack
| Component | Choice |
|-----------|--------|
| Backend | Django REST Framework |
| Database | PostgreSQL / SQLite |
| Auth | JWT / Token Authentication |
| External Services | Weather API (e.g., OpenWeather) |
| Documentation | README.md |

---

## Installation & Setup
1. Clone the repository:
```bash

git clone https://github.com/rolandslt/smart_assist_agriculture.git
cd capstone_project

2. Create and activate virtual environment:
```bash

python -m venv env
env\Scripts\activate  # Windows # source env/bin/activate  # Linux/Mac
