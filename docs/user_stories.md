# User stories

*NOTE: The roles "Repair Technician" and "Administrator" represent responsibilities and intended workflows.
The application does not implement authentication or role-based access control.*

## Repair Technician

**As a repair technician,**
**I want to see which bikes have registered complaints,**
**so I can prioritize repairs.**

**Acceptance Criteria:**

- [ ] The system displays the bike's current location and status
- [ ] The system displays all bikes with active complaints
- [ ] The system displays the complaint type for each bike
- [ ] Selecting a bike opens a detailed view of its complaints

**As a repair technician,**
**I want to move a bike to service,**
**so I can remove dysfunctional bikes from circulation.**

**Acceptance Criteria:**

- [ ] The repair technician can move a bike to service
- [ ] The bike status changes to `Service`
- [ ] Bikes in service don't appear as available

**As a repair technician,**
**I want to repair complaints and return bikes to a station,**
**so that repaired bikes become available again.**

**Acceptance Criteria:**

- [ ] The repair technician can mark complaints as repaired
- [ ] The system updates the list of remaining complaints
- [ ] The repair technician can return a bike to a station only when all complaints have been repaired
- [ ] The bike status changes from `Service` to `Parked`
- [ ] Returned bikes appear as available

## Administrator

**As an administrator,**
**I want to register new bikes,**
**so I can manage the bike fleet.**

**Acceptance Criteria:**

- [ ] The administrator can enter a bike name
- [ ] The administrator can assign an initial station
- [ ] Newly registered bikes are assigned the `Service` status
- [ ] The bike is persisted in the database
- [ ] The system prevents duplicate bike names
- [ ] The newly registered bike appears in the bike overview

**As an administrator,**
**I want to view and filter bikes,**
**so I can monitor bike availability and maintenance status.**

**Acceptance Criteria:**

- [ ] The system displays all bikes
- [ ] The administrator can filter bikes by station
- [ ] The administrator can filter bikes by activity status
- [ ] Selecting a bike displays additional bike information

**As an administrator,**
**I want to view station information and statistics,**
**so I can monitor station performance and usage.**

**Acceptance Criteria:**

- [ ] The system displays all stations
- [ ] The system displays the occupancy of each station
- [ ] The system displays the station capacity
- [ ] The system displays the number of trips originating from each station
- [ ] The administrator can open the station location in a map

**As an administrator,**
**I want to view revenue data,**
**so I can communicate business results to stakeholders.**

**Acceptance Criteria:**

- [ ] The system displays revenue trends by month and year
- [ ] The system displays revenue trends by subscription type
- [ ] The system displays total revenue

**As an administrator,**
**I want to view subscription analytics,**
**so I can understand customer behavior.**

**Acceptance Criteria:**

- [ ] The system displays subscriptions sold by type
- [ ] The system displays historical subscription trends