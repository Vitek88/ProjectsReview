# Data Collection from GreenWallbox Chargers

This project implements an automated data collection service for GreenWallbox electric vehicle charging stations. The service periodically retrieves charging session data and stores it in a Microsoft SQL Server database.

## Project Overview

The service performs the following main functions:

1. Authenticates with the GreenWallbox API
2. Downloads charging session reports for specified time periods
3. Processes the data (extracting from ZIP, parsing CSV)
4. Stores the data in a SQL Server database
5. Runs continuously with error handling and retry logic

## Requirements

- Python 3.8 or higher
- ODBC Driver 17 for SQL Server
- Microsoft SQL Server instance
- Network access to GreenWallbox API (https://greenwallbox.cloud)

### Python Dependencies

```
requests
urllib3
pyodbc
```

## Configuration

The service is configured through a `config.json` file which must contain:

```json
{
    "username": "YourGreenWallboxUsername",
    "password": "YourGreenWallboxPassword",
    "object_ids": "comma,separated,charger,ids",
    "api_login_url": "https://greenwallbox.cloud/api/users/login",
    "api_export_url": "https://greenwallbox.cloud/api/export/wallbox",
    "sql_server": "your-sql-server",
    "sql_database": "your-database",
    "sql_user": "sql-username",
    "sql_password": "sql-password",
    "Update_date": "YYYY-MM-DD HH:MM:SS"
}
```

- `username`, `password`: GreenWallbox API credentials
- `object_ids`: Comma-separated list of charger IDs to monitor
- `api_login_url`, `api_export_url`: GreenWallbox API endpoints
- `sql_*`: SQL Server connection details
- `Update_date`: Last successful data update timestamp (managed automatically)

## Database Schema

The service creates a table named `GreenWallbox` with the following schema:

```sql
CREATE TABLE GreenWallbox (
    [UserName] NVARCHAR(255),
    [StartDate] NVARCHAR(255),
    [StartHour] NVARCHAR(255),
    [EndDate] NVARCHAR(255),
    [EndHour] NVARCHAR(255),
    [ChargingTime] NVARCHAR(255),
    [Energy] FLOAT
)
```

## Running the Service

1. Install the required dependencies:
   ```powershell
   pip install requests urllib3 pyodbc
   ```

2. Configure your `config.json` file with appropriate credentials and settings

3. Run the service:
   ```powershell
   python main_service_v5.py
   ```

The service will:
- Run continuously
- Retry on errors with a 15-minute delay
- Log all activities to `greenwallbox.log`
- Update the configuration file with the latest successful update timestamp

## Logging

The service logs all activities to `greenwallbox.log`. The log includes:
- Service start/stop events
- API authentication attempts
- Data download status
- Database operations
- Errors and retry attempts

Log messages are formatted as:
```
YYYY-MM-DD HH:MM:SS [LEVEL] Message
```

## Error Handling

The service implements robust error handling for:
- API authentication failures
- Network connectivity issues
- Invalid data formats
- Database connection problems
- CSV parsing errors

On encountering an error, the service:
1. Logs the error details
2. Waits for 15 minutes
3. Retries the operation

## Development Tools

The project includes a documentation generator script (`generate_md_docs.py`) that automatically creates markdown documentation from Python source code. To use it:

```powershell
python generate_md_docs.py /path/to/project --out docs
```

This will:
- Parse all Python files in the project
- Extract docstrings and code structure
- Generate markdown documentation
- Create a SUMMARY.md index file