-- this is only for if you want to insert the data into a table instead of using materialized views

CREATE TABLE canto_activities (
    block_number BIGINT,
    block_timestamp TIMESTAMP,
    tx_hash TEXT,
    from_address TEXT,
    to_address TEXT,
    canto_transferred NUMERIC,
    token_amount NUMERIC,
    token_address TEXT,
    token_symbol TEXT
);
