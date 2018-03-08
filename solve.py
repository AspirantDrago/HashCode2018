name = 'e_high_bonus'

class Riders():
    def __init__(self, a, b, x, y, s, f):
        self.start_row = a
        self.start_col = b
        self.finish_row = x
        self.finish_col = y
        self.start = s
        self.finish = f
        self.dist = abs(a - x) + abs(b - y)
        self.free = True

    def optimal(self, x, y, now):
        global steps
        global bonus
        dist = max(abs(x - self.start_row) + abs(y - self.finish_row), self.start - now) + self.dist
        if abs(x - self.start_row) + abs(y - self.finish_row) == self.start - now:
            dist -= bonus
        if now + dist > self.finish:
            return float("inf")
        return dist

    def prize(self, x, y, now):
        global bonus
        if now + self.dist > self.finish:
            return 0
        rez = self.dist
        if abs(x - self.start_row) + abs(y - self.finish_row) == self.start - now:
            rez += bonus
        return rez


sum_b = 0
fin = open(name + '.in', 'r')
rows, cols, fleet, n_riders, bonus, steps = map(int, fin.readline().split())
riders = []
for i in range(n_riders):
    a, b, x, y, s, f = map(int, fin.readline().split())
    riders.append(Riders(a, b, x, y, s, f))
fin.close()
fleet_rid = [0] * fleet
for f in range(fleet):
    fleet_rid[f] = []
fleet_free = [0] * fleet
fleet_pos = [[0, 0]] * fleet
for now in range(steps + 1):
    print('now', now)
    for f in range(fleet):
        if fleet_free[f] > 0:
            fleet_free[f] -= 1
    while True:
        optimal_f = -1
        optimal_r = -1
        optimal_val = float("inf")
        for f in range(fleet):
            if fleet_free[f] == 0:
                for r in range(n_riders):
                    if riders[r].free:
                        dist = riders[r].optimal(fleet_pos[f][0], fleet_pos[f][1], now)
                        if dist < optimal_val:
                            optimal_val = dist
                            optimal_f = f
                            optimal_r = r
                            print('val', optimal_val)
        if optimal_val == float("inf"):
            break
        print(now, optimal_val, optimal_f, optimal_r)
        sum_b += riders[optimal_r].prize(fleet_pos[optimal_f][0], fleet_pos[optimal_f][1], now)
        riders[optimal_r].free = False
        fleet_rid[optimal_f].append(optimal_r)
        fleet_free[optimal_f] = optimal_val
        fleet_pos[optimal_f] = [riders[optimal_r].finish_row, riders[optimal_r].finish_col]
    if now % 1000 == 0:
        fout = open(name + '.out', 'w')
        for i in range(fleet):
            print(len(fleet_rid[i]), *fleet_rid[i], file=fout)
        fout.close()
fout = open(name + '.out', 'w')
for i in range(fleet):
    print(len(fleet_rid[i]), *fleet_rid[i], file=fout)
fout.close()
print('PRIZE:', sum_b)