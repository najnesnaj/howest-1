import random

def generate_random_data(n=69):
    assert n >= 33, "Need enough space to insert 4 high values with 8 apart"

    valid_quads = []
    for i in range(0, n - 24):
        for j in range(i + 8, n - 16):
            for k in range(j + 8, n - 8):
                for l in range(k + 8, n):
                    valid_quads.append((i, j, k, l))

    chosen_quad = random.choice(valid_quads)
    high_positions = set(chosen_quad)

    data = [random.randint(30, 70)]
    for i in range(1, n):
        if i in high_positions:
            value = random.randint(81, 100)
        else:
            prev = data[i - 1]
            low = max(1, prev - 20)
            high = min(100, prev + 20)
            value = random.randint(low, high)
            if value > 80:
                value = random.randint(low, min(80, high))
        data.append(value)

    return data
