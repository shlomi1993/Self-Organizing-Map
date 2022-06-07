def utility(color, engine, manufacturer):
    c_map = { 'red': 3, 'blue': 2, 'green': 1 }
    e_map = { 'electric': 3, 'petrol': 2, 'Diesel': 1 }
    m_map = { 'german': 3, 'french': 2, 'british': 1 }
    return 3 * 3 * c_map[color] + 3 * e_map[engine] + 1 * m_map[manufacturer]


def main():
    results = []
    for c in ['red', 'blue', 'green']:
        for e in ['electric', 'petrol', 'Diesel']:
            for m in ['german', 'french', 'british']:
                u = utility(c, e, m)
                results.append((u, (c, e, m)))
    results.sort(key=lambda t: t[0], reverse=True)
    for r in results:
        print(r)


main()
