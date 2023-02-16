TEMPERATURE_GRADE = {
            'norm': [18, 20],
            'low': 16,
            'high': 25
            }
HUMIDITY_GRADE = {
            'norm': [50, 55],
            'low': 45,
            'high': 60
            }
NORM_PRESS = {
            'norm': [731, 741],
            'low': 730,
            'high': 742
            }

# Если давление падает, то вероятно, что погода будет ухудшаться.
# Если давление растет - то это признак улучшения погоды
# Зимой высокое давление означает заморозки, а при низком давлении происходит потепление и возможны осадки
# Летом, наоборот, при повышении давления погода становится жаркой и сухой, а при понижении – холодает,
# и наступают дожди.
# Северный ветер чаще приносит прохладную погоду в местах, удаленных от океана.

