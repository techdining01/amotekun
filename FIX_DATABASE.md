# Database Schema Fix Instructions

## Problem
The `/api/incidents/` endpoint was failing with:
```
django.db.utils.ProgrammingError: column reports_incident.reporter_id does not exist
```

This occurred because the `Incident` model has a `reporter` ForeignKey field, but the database schema was never updated with a migration to add this column.

## Solution

### Step 1: Apply the Migration
I've created the missing migration file: `reports/migrations/0009_incident_reporter.py`

Run the following command to apply the migration:

```bash
python manage.py migrate
```

Or run the batch file:
```bash
apply_migrations.bat
```

### Step 2: Clean Up Unnecessary Files
Run the cleanup script to remove temporary files and the old corrupted `app.js`:

```bash
cleanup.bat
```

## What Was Fixed

### 1. Migration File Created
- **File**: `reports/migrations/0009_incident_reporter.py`
- **Purpose**: Adds the missing `reporter` ForeignKey field to the `Incident` model
- **Dependencies**: Depends on migration `0008_floodzone_risk_level_road_name`

### 2. Files to Clean Up
The following temporary/unnecessary files will be removed by `cleanup.bat`:
- `cleanup_js.py` - Temporary Python script
- `static/js/read_appjs.py` - Temporary Python script  
- `static/js/app.js` - Old corrupted file (will be backed up to `app.js.backup` first)
- `run_migrations.bat` - Redundant batch file (replaced by `apply_migrations.bat`)

### 3. Files to Keep
- `apply_migrations.bat` - For running migrations
- `cleanup.bat` - For cleaning up temporary files
- All new modular JavaScript files in `static/js/`

## Verification

After applying migrations, test the endpoint:

```bash
curl http://localhost:8000/api/incidents/
```

Or visit in your browser:
```
http://localhost:8000/api/incidents/
```

The endpoint should now return a GeoJSON FeatureCollection of incidents without errors.

## If Issues Persist

If you still encounter database errors, you may need to:

1. Check migration status:
```bash
python manage.py showmigrations reports
```

2. If migration is not applied, force it:
```bash
python manage.py migrate reports 0009
```

3. If there are data inconsistencies, you may need to reset the database (WARNING: This deletes all data):
```bash
python manage.py migrate reports zero
python manage.py migrate reports
```
