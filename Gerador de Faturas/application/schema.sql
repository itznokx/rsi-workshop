CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    service TEXT NOT NULL,
    amount FLOAT NOT NULL,
    custom_message TEXT,
    path TEXT NOT NULL
);
