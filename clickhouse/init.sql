DROP TABLE IF EXISTS logs;
CREATE TABLE logs (
  timestamp DateTime,
  level String,
  message String,
  value Int32,
  received_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY timestamp;
