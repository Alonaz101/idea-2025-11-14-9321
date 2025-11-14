# Project Overview

This repository contains the implementation of features based on Jira issues SCRUM-402 through SCRUM-412.

## Features Summary

### MVP Features

- **SCRUM-402: Mood Input & Recommendation Engine**
  - User can submit mood input.
  - Backend API recommends recipes matching mood tags.
- **SCRUM-403: User Authentication & Profile Management**
  - User registration and login with secure bcrypt password hashing.
  - JWT-based authentication.
- **SCRUM-404: Recipe Search and Filter**
  - Search recipes by mood, difficulty, and prep time.
  - Efficient querying with database indexes.

### Post-MVP Features

- **SCRUM-405: User Ratings and Feedback**
  - Users can rate recipes and leave textual feedback.
- **SCRUM-406: Social Sharing of Recipes**
  - Share recipes via social media (placeholder implementation).
- **SCRUM-407: Ingredient Substitutions**
  - Suggest alternative ingredients for recipes.

### Future Features

- **SCRUM-408: AI-Driven Mood Detection**
  - AI/ML inference of user mood from text or facial expressions (stubbed).
- **SCRUM-409: Grocery Delivery Integration**
  - Integration with third-party grocery delivery services (stubbed).

### Non-functional Requirements

- **SCRUM-410: Security, Privacy & Compliance Implementation**
  - HTTPS enforcement, role-based access control, GDPR compliance.
- **SCRUM-411: Performance, Scalability & Reliability Measures**
  - DB indexing, caching, horizontal scaling, load balancing.
- **SCRUM-412: Testing, Logging, and Monitoring Guidelines**
  - Unit and integration testing, centralized logging, monitoring & alerts.

## Code Structure

- `backend/app.py` - Core backend with MVP features.
- `backend/post_mvp_features.py` - Post-MVP features.
- `backend/future_features.py` - Stub implementations for future features.
- `backend/non_functional.py` - Security, performance, and monitoring features.

## Traceability

Each commit references corresponding Jira issue keys for traceability.

---

*This overview is generated automatically from Jira issues input.*
