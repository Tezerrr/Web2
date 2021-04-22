import time


def save(em, pasw, m, name=False):
    s = open('static\img\save.txt', 'a', encoding="utf-8")
    s.write(f"\n{name}-{em}-{pasw}-{m}-{time.asctime()}")
    print(
        "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
    print(f"Сохранено - {name}-{em}-{pasw}-{m}-{time.asctime()}")
    s.close()

