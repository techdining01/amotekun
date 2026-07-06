LoginForm

CitizenSignupForm

OfficerSignupForm

DispatcherSignupForm

AdminSignupForm

PasswordResetForm

ChangePasswordForm

MFAForm


auth_card

auth_field

password_strength

role_selector

avatar_upload

step_indicator

otp_input

social_button

verification_banner

security_notice


auth/

    login.html

    register.html

    citizen_signup.html

    officer_signup.html

    dispatcher_signup.html

    admin_signup.html

    verify_email.html

    email_sent.html

    password_reset.html

    password_change.html

    profile.html

    security.html


    ROLE_DASHBOARD = {
    User.Role.SUPER_ADMIN: "super-admin-dashboard",
    User.Role.STATE_ADMIN: "state-dashboard",
    User.Role.LGA_ADMIN: "lga-dashboard",
    User.Role.POLICE_COMMANDER: "police-dashboard",
    User.Role.POLICE_OFFICER: "police-officer-dashboard",
    User.Role.AMOTEKUN_COMMANDER: "amotekun-dashboard",
    User.Role.AMOTEKUN_OFFICER: "amotekun-officer-dashboard",
    User.Role.DISPATCHER: "dispatcher-dashboard",
    User.Role.ANALYST: "analytics-dashboard",
    User.Role.FACILITY_MANAGER: "facility-dashboard",
    User.Role.EMERGENCY_RESPONDER: "responder-dashboard",
    User.Role.CITIZEN: "citizen-dashboard",
    User.Role.AI_OPERATOR: "ai-dashboard",
    User.Role.AUDITOR: "audit-dashboard",
}




static/

    audio/

        incident.mp3

        dispatch.mp3

        patrol.mp3

        panic.mp3

        weather.mp3

        hotspot.mp3

        notification.mp3

    js/

        dashboard/

            sound.js








   



           incidents/

    incident_card.html
    incident_row.html
    incident_priority_badge.html
    incident_status_badge.html
    incident_timeline.html
    
    
patrol/

    patrol_card.html
    patrol_vehicle.html
    patrol_officer.html
    patrol_status_badge.html



maps/

    leaflet_map.html
    layer_switcher.html
    legend.html
    map_toolbar.html



ai/

    prediction_card.html
    recommendation_card.html
    hotspot_card.html
    confidence_badge.html


    dashboard/

    widget.html
    widget_header.html
    widget_toolbar.html
    widget_loading.html
    widget_error.html
    widget_empty.html



