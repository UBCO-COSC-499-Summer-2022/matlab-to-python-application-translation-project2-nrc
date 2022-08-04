def ur_symmetric(focal_l):
    return ((focal_l + 3.723) / 9.709) ** (-1 / 2.503)

def ur_asymmetric(focal_l):
    return ((focal_l + 0.811) / 7.59) ** (-1 / 2.727)


def cf_symmetric(ur):
    return ((ur ** (2.503 / -1)) * 9.709) - 3.723


def cf_asymmetric(ur):
    return ((ur ** (2.727 / -1)) * 7.59) - 0.811
