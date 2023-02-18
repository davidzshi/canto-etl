CREATE VIEW canto_activities AS
SELECT
    ct.blockNumber::bigint AS block_number,
    DATEADD(s, ct.timestamp::bigint, '1970-01-01'::timestamp) AS block_timestamp,
    ct.hash::text AS tx_hash,
    ct.fromAddress::text AS from_address,
    ct.toAddress::text AS to_address,
    NULL AS canto_transferred,
    ROUND(ct.Value::float/1000000000000000000, 18)::DECIMAL AS token_amount,
    ct.contractAddress::text AS token_address,
    ct.tokenSymbol::text AS token_symbol
FROM
    canto.canto_token_transfers ct

UNION ALL

SELECT
    ctx.blockNumber::bigint AS block_number,
    DATEADD(s, ctx.timestamp::bigint, '1970-01-01'::timestamp) AS block_timestamp,
    ctx.hash::text AS tx_hash,
    ctx.fromAddress::text AS from_address,
    ctx.toAddress::text AS to_address,
    ROUND(ctx.value::float/1000000000000000000, 18)::DECIMAL AS canto_transferred,
    NULL AS token_amount,
    NULL AS token_address,
    NULL AS token_symbol
FROM
    canto.canto_transactions ctx;
