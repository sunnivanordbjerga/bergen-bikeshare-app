# Requirements

## Functional Requirements

### FR-1 Bike management

The system shall allow administrators to register new bikes.

### FR-2 Bike Overview

The system shall display all bikes, their current status and last known location.

### FR-3 Bike Filtering

The system shall allow filtering bikes by station and activity status.

### FR-4 Station Monitoring

The system shall display occupancy, capacity and usage statistics for all stations.

### FR-5 Complaint Overview

The system shall display a list of all bikes with active complaints and their complaint details.

### FR-6 Maintenance actions

The system shall allow moving bikes to service, repairing complaints and returning bikes to a station once all repairs
are complete.

### FR-7 Revenue analytics

The system shall display total revenue and revenue statistics by year, month, and subscription type.

### FR-8 Subscription analytics

The system shall display subscription sales and historical trends.

### FR-9 Map Overview

The system shall display station locations on an interactive map.

## Non-functional Requirements

### NFR-1 Persistence

The application shall persist data using SQLite

### NFR-2 Data Integrity

The application shall enforce data integrity through database constraints and foreign keys.

### NFR-3 Database Seeding

The application shall support automated generation of realistic seed data.

### NFR-4 User Interface

The application shall provide an interactive web interface using Shiny for Python.

### NFR-5 Maintainability

The application shall separate repositories, services and user interface components.

### NFR-6 Testing

Core business logic and data import functionality shall be covered by automated tests.
