API Endpoints to Test
Public Endpoints (No Authentication Required)
Incidents:

GET /api/incidents/ - List all incidents
POST /api/incidents/ - Create new incident
GET /api/incidents/<id>/ - Get specific incident
PUT /api/incidents/<id>/ - Update incident
DELETE /api/incidents/<id>/ - Delete incident
Police Stations:

GET /api/stations/police/ - List all police stations
GET /api/stations/police/<id>/ - Get specific police station
Amotekun Stations:

GET /api/stations/amotekun/ - List all Amotekun stations
GET /api/stations/amotekun/<id>/ - Get specific Amotekun station
LGAs:

GET /api/lga/ - List all LGAs
Authenticated Endpoints (Require Login)
Dispatches:

GET /api/dispatch/dispatches/ - List all dispatches
POST /api/dispatch/dispatches/ - Create dispatch
GET /api/dispatch/dispatches/<id>/ - Get specific dispatch
PUT /api/dispatch/dispatches/<id>/ - Update dispatch
DELETE /api/dispatch/dispatches/<id>/ - Delete dispatch
POST /api/dispatch/dispatches/<id>/transition/ - Change status
POST /api/dispatch/dispatches/<id>/assign_officer/ - Assign officer
POST /api/dispatch/dispatches/<id>/cancel/ - Cancel dispatch
GET /api/dispatch/dispatches/my_assignments/ - Officer's assignments
GET /api/dispatch/dispatches/my_created/ - Dispatcher's created dispatches
Authentication Endpoints
POST /accounts/login/ - Login
POST /accounts/logout/ - Logout
POST /accounts/signup/ - Register
GET /accounts/confirm-email/<key>/ - Confirm email
POST /accounts/password/change/ - Change password
Dashboard Endpoints
GET /dashboard/ - Redirect to role-specific dashboard
GET /dashboard/citizen/ - Citizen dashboard
GET /dashboard/officer/ - Officer dashboard
GET /dashboard/dispatcher/ - Dispatcher dashboard
GET /dashboard/admin/ - Admin dashboard