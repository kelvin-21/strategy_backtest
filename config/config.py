from config import OPEN, HIGH, LOW, CLOSE, ADJ_CLOSE, VOLUME, GEO_RETURN_SIG, THIS_YEAR, MONTHS, TOTAL, RETURN_GEO, RETURN_AVG, RETURN, PRICE, OCC, OCC_PROFIT, OCC_LOSS, RETURN_STD, OCC_SIG

represent_in_precentage = [
    RETURN_AVG, RETURN, RETURN_GEO
    ]

represent_with_comma = [
    OPEN, HIGH, LOW, CLOSE, ADJ_CLOSE, VOLUME, PRICE
]

represent_as_integer = [
    OCC, OCC_PROFIT, OCC_LOSS
]

represent_as_decimal = [
    RETURN_STD
]


geo_cols_total = ['{}_{}'.format(TOTAL, GEO_RETURN_SIG)]
geo_cols_year = ['{}_{}'.format(i, GEO_RETURN_SIG) for i in range(2000, THIS_YEAR+1)]
geo_cols_month = ['{}_{}'.format(MONTHS[i], GEO_RETURN_SIG) for i in range(1, 12+1)]
represent_in_precentage.extend(geo_cols_total + geo_cols_year + geo_cols_month)

occ_cols_total = ['{}_{}'.format(TOTAL, OCC_SIG)]
occ_cols_year = ['{}_{}'.format(i, OCC_SIG) for i in range(2000, THIS_YEAR+1)]
occ_cols_month = ['{}_{}'.format(MONTHS[i], OCC_SIG) for i in range(1, 12+1)]
represent_as_integer.extend(occ_cols_total + occ_cols_year + occ_cols_month)