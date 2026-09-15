-- ============================================================================
-- create_login_master.sql - server login for the Lakeflow Connect user
-- ============================================================================
-- Run FIRST, against the **master** database (Azure SQL Database has no USE),
-- then run enable_cdc.sql against AdventureWorksLT. Idempotent.
--
--   sqlcmd -S <sql_server_fqdn> -d master \
--          -U <sql_admin_login> -P '<sql_admin_password>' \
--          -i infra/sql/create_login_master.sql
--
-- Why a server login (not a contained user): on Azure SQL Database the
-- connector user must be a member of the ##MS_DatabaseConnector## server role
-- so it can access master - server roles only accept logins.
-- Docs: https://learn.microsoft.com/azure/databricks/ingestion/lakeflow-connect/sql-server-privileges
--
-- >>> REPLACE THE PLACEHOLDER PASSWORD BEFORE RUNNING <<<
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM sys.sql_logins WHERE name = N'lakeflow_connect')
BEGIN
    CREATE LOGIN lakeflow_connect WITH PASSWORD = N'CHANGE_ME-LakeflowC0nnect!';
    PRINT 'Login lakeflow_connect created';
END
ELSE
    PRINT 'Login lakeflow_connect already exists';
GO

IF IS_SRVROLEMEMBER(N'##MS_DatabaseConnector##', N'lakeflow_connect') = 1
    PRINT 'lakeflow_connect already in ##MS_DatabaseConnector##';
ELSE
BEGIN
    ALTER SERVER ROLE ##MS_DatabaseConnector## ADD MEMBER lakeflow_connect;
    PRINT 'lakeflow_connect added to ##MS_DatabaseConnector##';
END
GO
