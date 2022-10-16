# initial table for statistics scrapped from website

CREATE TABLE stats (
    rid SERIAL PRIMARY KEY,
    date DATE,
    personnel_total INTEGER,
    personnel_delta INTEGER,
    personnel_killed INTEGER,
    personnel_wounded INTEGER,
    personnel_captured INTEGER,
    acv INTEGER,
    acv_delta INTEGER,
    tanks INTEGER,
    tanks_delta INTEGER,
    artillery INTEGER,
    artillery_delta INTEGER,
    aircrafts INTEGER,
    aircrafts_delta INTEGER,
    helicopters INTEGER,
    helicopters_delta INTEGER,
    naval INTEGER,
    naval_delta INTEGER
);