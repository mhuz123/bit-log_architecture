DROP TABLE IF EXISTS logs;
CREATE TABLE logs (
  timestamp DateTime,
  level String,
  message String,
  value Int32
) ENGINE = MergeTree()
ORDER BY timestamp;
