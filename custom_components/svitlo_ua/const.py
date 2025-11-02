"""Constants for Svitlo UA integration."""
DOMAIN = "svitlo_ua"
PLATFORMS = ["sensor", "binary_sensor", "calendar"]

# Підтримувані регіони (відображаються в списку конфігурації)
REGIONS = {
    "Київ": "Kyiv",
    "Київська область": "Kyiv region",
    "Дніпропетровська область (Дніпро)": "Dnipropetrovsk",
    "Львівська область": "Lviv",
    "Харківська область": "Kharkiv",
    "Одеська область": "Odesa",
    "Миколаївська область": "Mykolaiv",
    "Чернігівська область": "Chernihiv",
    "Тернопільська область": "Ternopil",
    "Вінницька область": "Vinnytsia"
}
# Примітка: Ключі наведені українською для зручності, значення – англійською (використовуються внутрішньо).

# Регіони, де потрібно вибрати постачальника (кілька операторів)
REGION_PROVIDERS = {
    "Dnipropetrovsk": ["DTEK", "CEK"],  # Для Дніпропетровської обл. можливий DTEK або ЦЕК
    # Інші регіони не потребують вибору постачальника
}

# Мапування регіонів та постачальників на джерело даних і необхідні коди
YASNO_CITY_CODES = {
    "Kyiv": "kiev",
    "Dnipropetrovsk": "dnipro"  # використовується для DTEK (Ясно)
}
# Доменні імена субдоменів на energy-ua.info для регіонів
ENERGY_UA_SUBDOMAINS = {
    "Kyiv region": "kyiv",       # Kyiv та область на сайті Київ (адресний пошук)
    "Lviv": "lviv",
    "Kharkiv": "kharkiv",
    "Odesa": "odesa",
    "Mykolaiv": "mykolaiv",
    "Chernihiv": "chernigiv",   # зверніть увагу: "chernigiv" латиницею
    "Ternopil": "ternopil",
    "Vinnytsia": "vinnytsia",
    "Dnipropetrovsk": "dnipro"  # для ЦЕК (якщо вибрано)
}
