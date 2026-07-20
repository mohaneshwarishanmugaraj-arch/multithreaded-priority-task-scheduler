# configuration.py

# ==========================================
# Priority Levels
# ==========================================

HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

PRIORITIES = [HIGH, MEDIUM, LOW]

# ==========================================
# Thread Configuration
# ==========================================

NUM_PRODUCERS = 2
NUM_WORKERS = 2

# ==========================================
# Task Configuration
# ==========================================

TASKS_PER_PRODUCER = 10

MIN_WEIGHT = 1
MAX_WEIGHT = 10

MIN_RESOURCE_UNITS = 1
MAX_RESOURCE_UNITS = 5

MIN_EXECUTION_TIME = 1
MAX_EXECUTION_TIME = 5

# ==========================================
# Scheduler Configuration
# ==========================================

BUFFER_SIZE = 10

# Time (in seconds) after which a waiting task
# is promoted to the next higher priority
AGING_TIME = 10

# ==========================================
# Resource Pool
# ==========================================

TOTAL_RESOURCES = 10

# ==========================================
# Task States
# ==========================================

CREATED = "CREATED"
QUEUED = "QUEUED"
RUNNING = "RUNNING"
COMPLETED = "COMPLETED"
PROMOTED = "PROMOTED"

# ==========================================
# Logging
# ==========================================

ENABLE_LOGS = True