# Dispatch Workflow Documentation

## Overview
The dispatch workflow has been enhanced with status transition logic, automatic officer assignment, and role-based API endpoints.

## Status Transitions

### Valid Transitions
```
pending → dispatched → in_progress → resolved
         ↘ cancelled ↗
```

### Transition Rules
- **pending** can transition to: `dispatched`, `cancelled`
- **dispatched** can transition to: `in_progress`, `cancelled`
- **in_progress** can transition to: `resolved`, `cancelled`
- **resolved** - Terminal state (no further transitions)
- **cancelled** - Terminal state (no further transitions)

## Model Enhancements

### New Fields
- `dispatched_at` - Timestamp when dispatch was sent
- `in_progress_at` - Timestamp when officer started work
- `resolved_at` - Timestamp when incident was resolved

### New Methods
- `can_transition_to(new_status)` - Check if transition is valid
- `transition_to(new_status)` - Execute status transition
- `assign_officer(officer)` - Assign officer and auto-transition to dispatched
- `cancel(reason)` - Cancel dispatch with optional reason

## API Endpoints

### Standard CRUD
- `GET /api/dispatch/dispatches/` - List all dispatches
- `POST /api/dispatch/dispatches/` - Create dispatch (auto-sets dispatcher)
- `GET /api/dispatch/dispatches/<id>/` - Get dispatch details
- `PUT /api/dispatch/dispatches/<id>/` - Update dispatch
- `DELETE /api/dispatch/dispatches/<id>/` - Delete dispatch

### Workflow Actions
- `POST /api/dispatch/dispatches/<id>/transition/` - Change status
  - Body: `{"status": "in_progress"}`
  - Returns: Updated dispatch with message

- `POST /api/dispatch/dispatches/<id>/assign_officer/` - Assign officer
  - Body: `{"officer_id": 123}`
  - Auto-transitions to "dispatched" if currently "pending"

- `POST /api/dispatch/dispatches/<id>/cancel/` - Cancel dispatch
  - Body: `{"reason": "Optional reason"}`
  - Cannot cancel if already resolved or cancelled

### Role-Based Endpoints
- `GET /api/dispatch/dispatches/my_assignments/` - Officer's active assignments
  - Requires: OFFICER role
  - Returns: Dispatches assigned to current officer (excluding resolved/cancelled)

- `GET /api/dispatch/dispatches/my_created/` - Dispatcher's created dispatches
  - Requires: DISPATCHER role
  - Returns: All dispatches created by current dispatcher

## Usage Examples

### Create Dispatch (as Dispatcher)
```bash
POST /api/dispatch/dispatches/
{
    "incident": 1,
    "police_station": 2,
    "amotekun_station": null,
    "status": "pending",
    "notes": "Urgent response needed"
}
```

### Transition Status
```bash
POST /api/dispatch/dispatches/1/transition/
{
    "status": "dispatched"
}
```

### Assign Officer
```bash
POST /api/dispatch/dispatches/1/assign_officer/
{
    "officer_id": 5
}
```

### Cancel Dispatch
```bash
POST /api/dispatch/dispatches/1/cancel/
{
    "reason": "Duplicate dispatch"
}
```

### Get Officer Assignments
```bash
GET /api/dispatch/dispatches/my_assignments/
```

## Security
- All endpoints require authentication
- Role-based access control enforced
- Officers can only be assigned to dispatches
- Dispatchers are auto-set on dispatch creation

## Next Steps
1. Apply migration: `python manage.py migrate dispatch`
2. Test workflow with different user roles
3. Integrate with real-time notifications (Phase 8)
4. Add dispatcher dashboard controls
