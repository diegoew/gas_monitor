import config


LOAD_RESISTANCES = {
    'MQ-2': 5,
    'MQ-3': 12,
    'MQ-4': 13,
    'MQ-5': 14,
    'MQ-6': 15,
    'MQ-7': 16,
    'MQ-8': 17,
    'MQ-9': 18,
    'MQ-135': 20,
}

# Air resistance ratios (rsco/ro)
RSCO_RO_RATIOS = {
    'MQ-2': 9.48,
    'MQ-3': 60.31,
    'MQ-4': 4.43,
    'MQ-5': 6.46,
    'MQ-6': 9.94,
    'MQ-7': 26.09,
    'MQ-8': 1.00,
    'MQ-9': 9.71,
    'MQ-135': 3.5,
    }

assert set(LOAD_RESISTANCES) == set(RSCO_RO_RATIOS)
assert set(config.SENSOR_TYPES) <= set(LOAD_RESISTANCES)
