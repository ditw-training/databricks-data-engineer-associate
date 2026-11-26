-- RetailHub sales star: Bronze layer (Lab 07)
-- Raw files from the landing folders under ${source_path}, read incrementally.
-- Each table adds two columns from the file metadata: the file a row came from and the time the file arrived.

CREATE OR REFRESH STREAMING TABLE bronze_orders
COMMENT 'Raw orders from the landing folder orders/'
AS SELECT
  *,
  _metadata.file_path AS _source_file,
  _metadata.file_modification_time AS _ingested_at
FROM STREAM read_files('${source_path}/orders', format => 'json');

CREATE OR REFRESH STREAMING TABLE bronze_customers
COMMENT 'Raw customer files: the first snapshot, then the change files'
AS SELECT
  *,
  _metadata.file_path AS _source_file,
  _metadata.file_modification_time AS _ingested_at
FROM STREAM read_files('${source_path}/customers', format => 'csv', header => true);

CREATE OR REFRESH STREAMING TABLE bronze_products
COMMENT 'Raw product files'
AS SELECT
  *,
  _metadata.file_path AS _source_file,
  _metadata.file_modification_time AS _ingested_at
FROM STREAM read_files('${source_path}/products', format => 'csv', header => true);
