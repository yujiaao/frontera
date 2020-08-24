#--------------------------------------------------------
# Frontier
#--------------------------------------------------------
BACKEND = 'frontera.contrib.backends.sqlalchemy.Distributed'
user = "zixun_my"
password = "swqi2C#2@YcYqzCj"
host = "10.27.15.147"
database_name = "overseas_frontera"
SQLALCHEMYBACKEND_ENGINE = f'mysql+pymysql://{user}:{password}@{host}/{database_name}?charset=utf8mb4'

MAX_REQUESTS = 5
MAX_NEXT_REQUESTS = 1

#--------------------------------------------------------
# Logging
#--------------------------------------------------------
LOGGING_EVENTS_ENABLED = False
LOGGING_MANAGER_ENABLED = False
LOGGING_BACKEND_ENABLED = False
LOGGING_DEBUGGING_ENABLED = False
