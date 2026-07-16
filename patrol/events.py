from django.dispatch import Signal

mission_created = Signal()

mission_started = Signal()

mission_completed = Signal()

mission_cancelled = Signal()

gps_received = Signal()

vehicle_assigned = Signal()

shift_started = Signal()

shift_ended = Signal()

panic_pressed = Signal()

officer_checked_in = Signal()


