def fmt(seconds):
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}:{s:02d}"