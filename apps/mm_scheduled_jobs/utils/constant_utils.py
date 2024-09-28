class TriggerTypeChoicesNames:
    INTERVAL = 'interval'
    CHRONOLOGICAL = 'chronological'


SCHEDULED_JOB_INSTANCE_STATUSES = [
    ('pending', 'Pending'),
    ('building', 'Building'),
    ('initializing_assistant', 'Initializing Assistant'),
    ('generating', 'Generating'),
    ('saving_logs', 'Saving Logs'),
    ('cleaning_up', 'Cleaning Up'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]


class ScheduledJobInstanceStatusesNames:
    PENDING = 'pending'
    BUILDING = 'building'
    INITIALIZING_ASSISTANT = 'initializing_assistant'
    GENERATING = 'generating'
    SAVING_LOGS = 'saving_logs'
    CLEANING_UP = 'cleaning_up'
    COMPLETED = 'completed'
    FAILED = 'failed'
