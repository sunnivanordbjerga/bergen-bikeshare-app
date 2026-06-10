-- Bergen BikeShare database schema.
-- SQLite 3.

CREATE TABLE IF NOT EXISTS Station
(
    StationID   INTEGER PRIMARY KEY,
    StationName TEXT    NOT NULL UNIQUE,
    Latitude    REAL    NOT NULL
        CHECK (Latitude BETWEEN -90 AND 90),
    Longitude   REAL    NOT NULL
        CHECK (Longitude BETWEEN -180 AND 180),
    MaxCapacity INTEGER NOT NULL
        CHECK (MaxCapacity > 0)
);


CREATE TABLE IF NOT EXISTS ActivityStatus
(
    ActivityStatusID INTEGER PRIMARY KEY,
    Description      TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS Bike
(
    BikeID           INTEGER PRIMARY KEY,
    BikeName         TEXT    NOT NULL UNIQUE,
    LastStationID    INTEGER,                    -- NULL when bike is active, missing or in service
    ActivityStatusID INTEGER NOT NULL,
    FOREIGN KEY (LastStationID)
        REFERENCES Station (StationID),
    FOREIGN KEY (ActivityStatusID)
        REFERENCES ActivityStatus (ActivityStatusID)
);


CREATE TABLE IF NOT EXISTS User
(
    UserID    INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName  TEXT NOT NULL,
    PhoneNr   TEXT NOT NULL UNIQUE,
    Latitude  REAL
        CHECK (Latitude BETWEEN -90 AND 90),
    Longitude REAL
        CHECK (Longitude BETWEEN -180 AND 180)
);


CREATE TABLE IF NOT EXISTS SubscriptionType
(
    SubscriptionTypeID INTEGER PRIMARY KEY,
    Description        TEXT    NOT NULL UNIQUE,
    Price              REAL    NOT NULL
        CHECK (Price >= 0),
    DurationInDays     INTEGER NOT NULL
        CHECK (DurationInDays > 0)
);


CREATE TABLE IF NOT EXISTS Subscription
(
    SubscriptionID     INTEGER PRIMARY KEY,
    UserID             INTEGER NOT NULL,
    StartDate          TEXT    NOT NULL, -- save as YYYY-MM-DD HH:MM:SS
    SubscriptionTypeID INTEGER NOT NULL,
    FOREIGN KEY (UserID)
        REFERENCES User (UserID),
    FOREIGN KEY (SubscriptionTypeID)
        REFERENCES SubscriptionType (SubscriptionTypeID)
);


CREATE TABLE IF NOT EXISTS ComplaintType
(
    ComplaintTypeID INTEGER PRIMARY KEY,
    Description     TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS Complaint
(
    ComplaintID     INTEGER PRIMARY KEY,
    BikeID          INTEGER NOT NULL,
    UserID          INTEGER NOT NULL,
    ComplaintTypeID INTEGER NOT NULL,
    ReportDate      TEXT    NOT NULL, -- save as YYYY-MM-DD HH:MM:SS
    FOREIGN KEY (BikeID)
        REFERENCES Bike (BikeID),
    FOREIGN KEY (UserID)
        REFERENCES User (UserID),
    FOREIGN KEY (ComplaintTypeID)
        REFERENCES ComplaintType (ComplaintTypeID)
);


CREATE TABLE IF NOT EXISTS Trip
(
    TripID         INTEGER PRIMARY KEY,
    UserID         INTEGER NOT NULL,
    BikeID         INTEGER NOT NULL,
    StartStationID INTEGER NOT NULL,
    EndStationID   INTEGER,
    StartTime      TEXT    NOT NULL, -- save as YYYY-MM-DD HH:MM:SS
    EndTime        TEXT,             -- NULL while trip is active
    CHECK (
        EndTime IS NULL
        OR StartTime <= EndTime
        ),
    FOREIGN KEY (UserID)
        REFERENCES User (UserID),
    FOREIGN KEY (BikeID)
        REFERENCES Bike (BikeID),
    FOREIGN KEY (StartStationID)
        REFERENCES Station (StationID),
    FOREIGN KEY (EndStationID)
        REFERENCES Station (StationID)
);


-- Indexes

CREATE INDEX IF NOT EXISTS idx_bike_status
    ON Bike (ActivityStatusID);

CREATE INDEX IF NOT EXISTS idx_bike_location
    ON Bike (LastStationID);
