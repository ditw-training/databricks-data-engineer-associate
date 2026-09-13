-- ============================================================================
-- enable_cdc.sql - AdventureWorksLT CDC enablement for Lakeflow Connect
-- ============================================================================
-- Run AFTER `terraform apply` and AFTER create_login_master.sql (which creates
-- the lakeflow_connect server login), against the AdventureWorksLT database
-- (NOT master). Idempotent: safe to re-run any number of times.
--
-- Exact invocation (values come from `terraform output`):
--
--   sqlcmd -S <sql_server_fqdn> -d master \
--          -U <sql_admin_login> -P '<sql_admin_password>' \
--          -i infra/sql/create_login_master.sql
--   sqlcmd -S <sql_server_fqdn> -d AdventureWorksLT \
--          -U <sql_admin_login> -P '<sql_admin_password>' \
--          -i infra/sql/enable_cdc.sql
--
-- e.g.
--   sqlcmd -S sql-dea-training-ab12c.database.windows.net -d AdventureWorksLT \
--          -U deatrainer -P '***' -i infra/sql/enable_cdc.sql
--
-- NOTE ON TIERS: CDC on Azure SQL Database requires >= S3 (DTU) or >= 1 vCore.
-- The Terraform-provisioned GP_S_Gen5_1 (serverless, 1 vCore) qualifies.
-- If you downgraded the SKU below that, sp_cdc_enable_db fails - use the
-- CHANGE TRACKING alternative at the bottom instead (any tier, and also
-- supported by Lakeflow Connect).
--
-- The lakeflow_connect password is set in create_login_master.sql - use that
-- value in the Lakeflow Connect connection UI.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Enable CDC at the database level (guarded - idempotent)
-- ----------------------------------------------------------------------------
IF NOT EXISTS (
    SELECT 1 FROM sys.databases
    WHERE name = DB_NAME() AND is_cdc_enabled = 1
)
BEGIN
    EXEC sys.sp_cdc_enable_db;
    PRINT 'CDC enabled on database ' + DB_NAME();
END
ELSE
    PRINT 'CDC already enabled on database ' + DB_NAME();
GO

-- ----------------------------------------------------------------------------
-- 2. Enable CDC per table (guarded via cdc.change_tables - idempotent)
-- ----------------------------------------------------------------------------
DECLARE @tables TABLE (schema_name SYSNAME, table_name SYSNAME);
INSERT INTO @tables VALUES
    (N'SalesLT', N'Customer'),
    (N'SalesLT', N'Product'),
    (N'SalesLT', N'SalesOrderHeader'),
    (N'SalesLT', N'SalesOrderDetail');

DECLARE @schema SYSNAME, @table SYSNAME;
DECLARE table_cursor CURSOR LOCAL FAST_FORWARD FOR
    SELECT schema_name, table_name FROM @tables;
OPEN table_cursor;
FETCH NEXT FROM table_cursor INTO @schema, @table;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM cdc.change_tables ct
        JOIN sys.tables  t ON t.object_id = ct.source_object_id
        JOIN sys.schemas s ON s.schema_id = t.schema_id
        WHERE s.name = @schema AND t.name = @table
    )
    BEGIN
        EXEC sys.sp_cdc_enable_table
            @source_schema        = @schema,
            @source_name          = @table,
            @role_name            = NULL, -- no gating role - access via grants below
            @supports_net_changes = 0;
        PRINT 'CDC enabled: ' + @schema + '.' + @table;
    END
    ELSE
        PRINT 'CDC already enabled: ' + @schema + '.' + @table;
    FETCH NEXT FROM table_cursor INTO @schema, @table;
END
CLOSE table_cursor;
DEALLOCATE table_cursor;
GO

-- Verify: lists all CDC-enabled tables.
EXEC sys.sp_cdc_help_change_data_capture;
GO

-- ----------------------------------------------------------------------------
-- 3. Low-privilege user for the Lakeflow Connect connection (idempotent)
-- ----------------------------------------------------------------------------
-- Database user mapped to the lakeflow_connect server LOGIN created by
-- create_login_master.sql (Azure SQL DB needs the login for the
-- ##MS_DatabaseConnector## server role). Use this user (not the admin) in the
-- Lakeflow Connect connection.
-- A contained user with the same name (older version of this script) is
-- replaced by the login-mapped one.
IF EXISTS (
    SELECT 1 FROM sys.database_principals
    WHERE name = N'lakeflow_connect' AND authentication_type_desc = N'DATABASE'
)
BEGIN
    DROP USER lakeflow_connect;
    PRINT 'Dropped contained user lakeflow_connect (replaced by login-mapped user)';
END

IF NOT EXISTS (
    SELECT 1 FROM sys.database_principals WHERE name = N'lakeflow_connect'
)
BEGIN
    CREATE USER lakeflow_connect FOR LOGIN lakeflow_connect;
    PRINT 'User lakeflow_connect created';
END
ELSE
    PRINT 'User lakeflow_connect already exists';
GO

-- Read access to source tables + CDC change tables.
ALTER ROLE db_datareader ADD MEMBER lakeflow_connect;
GRANT SELECT ON SCHEMA::SalesLT TO lakeflow_connect;
GRANT SELECT ON SCHEMA::cdc TO lakeflow_connect;
GO

-- Metadata access the SQL Server connector needs on Azure SQL Database
-- (docs: "Microsoft SQL Server database user requirements" - Azure SQL
-- Database table). The sp_tables/sp_columns_100/... EXECUTE grants from the
-- on-prem table do NOT apply here and fail with error 4629 outside master.
GRANT VIEW DATABASE STATE TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.schemas                TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.tables                 TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.columns                TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.key_constraints        TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.foreign_keys           TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.check_constraints      TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.default_constraints    TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.change_tracking_tables TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.objects                TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.triggers               TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.indexes                TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.index_columns          TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.fulltext_index_columns TO lakeflow_connect;
GRANT SELECT ON OBJECT::sys.fulltext_indexes       TO lakeflow_connect;
GO

-- DDL support objects (schema-change handling for CDC) are NOT created here.
-- If the connection wizard's Validate step reports missing objects/permissions,
-- run Databricks' utility script (as db_owner) and then, e.g.:
--   EXEC dbo.lakeflowFixPermissions @User = 'lakeflow_connect', @Tables = 'SCHEMAS:SalesLT';
-- Script + reference: https://learn.microsoft.com/azure/databricks/ingestion/lakeflow-connect/sql-server-utility
GO

PRINT 'Done. Test with: SELECT COUNT(*) FROM SalesLT.Customer; (as lakeflow_connect)';
GO

-- ----------------------------------------------------------------------------
-- 4. ALTERNATIVE: CHANGE TRACKING (cheaper - works on ANY tier)
-- ----------------------------------------------------------------------------
-- Lakeflow Connect also supports Change Tracking. Use it instead of CDC if
-- the database runs below 1 vCore / S3, or to shave cost further. Do not
-- enable both mechanisms for the same connector pipeline - pick one.
-- Uncomment to use:
/*
-- Database level:
IF NOT EXISTS (
    SELECT 1 FROM sys.change_tracking_databases
    WHERE database_id = DB_ID()
)
    ALTER DATABASE CURRENT
    SET CHANGE_TRACKING = ON (CHANGE_RETENTION = 3 DAYS, AUTO_CLEANUP = ON);
GO

-- Per table (repeat for each source table):
IF NOT EXISTS (SELECT 1 FROM sys.change_tracking_tables
               WHERE object_id = OBJECT_ID(N'SalesLT.Customer'))
    ALTER TABLE SalesLT.Customer ENABLE CHANGE_TRACKING WITH (TRACK_COLUMNS_UPDATED = ON);
IF NOT EXISTS (SELECT 1 FROM sys.change_tracking_tables
               WHERE object_id = OBJECT_ID(N'SalesLT.Product'))
    ALTER TABLE SalesLT.Product ENABLE CHANGE_TRACKING WITH (TRACK_COLUMNS_UPDATED = ON);
IF NOT EXISTS (SELECT 1 FROM sys.change_tracking_tables
               WHERE object_id = OBJECT_ID(N'SalesLT.SalesOrderHeader'))
    ALTER TABLE SalesLT.SalesOrderHeader ENABLE CHANGE_TRACKING WITH (TRACK_COLUMNS_UPDATED = ON);
IF NOT EXISTS (SELECT 1 FROM sys.change_tracking_tables
               WHERE object_id = OBJECT_ID(N'SalesLT.SalesOrderDetail'))
    ALTER TABLE SalesLT.SalesOrderDetail ENABLE CHANGE_TRACKING WITH (TRACK_COLUMNS_UPDATED = ON);
GO

-- Permission the connector user needs for Change Tracking reads:
GRANT VIEW CHANGE TRACKING ON SCHEMA::SalesLT TO lakeflow_connect;
GO
*/
