def data_check(day, month, year):
    norm_year = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    try:
        day, month, year = int(day), int(month), int(year)
        if year >= 2006:
            return False
        n_y = norm_year[abs(month - 1)]
        if year % 4 != 0:
            if n_y >= day:
                return True
            return False
        else:
            if n_y >= day or (n_y == 1 and day == 29):
                return True
            return False
    except:
        return False
