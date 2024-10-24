from database.models import Halls

print(*map(lambda x: x.config_json, Halls.select()), sep="\n")
print("/`--ЭКРАН---\\")
