import numpy as np

p_a = 1.0 / 100.0
p_ba = 1.0
p_na = 99.0 / 100.0
p_bna = 0.5 ** 10
p_b = p_ba * p_a + p_bna * p_na
p_ab = p_ba * p_a / p_b

n_coins = 100
coins = np.zeros(n_coins, dtype=np.int)  # 100 coin all fair
coins[np.random.randint(1, 100, 1)] = 1  # make one coin unfair

n_flips = 10
n_samples = 1000000

all_heads_coins = []

# v1
for i in range(n_samples):
    coin = coins[np.random.randint(1, 100, 1)[0]]
    heads = 1
    for j in range(n_flips):
        flip = np.random.rand()  # random number between 0, 1
        if coin == 1 or flip > 0.5:
            heads = 1
        else:
            heads = 0
            break
    if heads:
        all_heads_coins.append([i, coin])

n_all_heads = len(all_heads_coins)
all_heads_coins = np.array(all_heads_coins)
all_heads_coins = np.c_[all_heads_coins, np.empty(n_all_heads)]
for i in range(n_all_heads):
    all_heads_coins[i, 2] = all_heads_coins[:i, 1].sum() * 1.0 / (i + 1)
print('probability coin was unfair: {:.3}'.format(all_heads_coins[-1, 2]))

try:
    import bokeh.plotting
    from bokeh.palettes import Category10_10 as palette
    bokeh.plotting.output_file('coin.html')

    p = bokeh.plotting.figure(
        y_axis_label='draws when all heads was unfair coin',
        x_axis_label='trials')
    p.line(all_heads_coins[:, 0], all_heads_coins[:, 2], color=palette[0])
    p.line(all_heads_coins[[0, -1], 0], [p_ab, p_ab], color=palette[1])
    bokeh.plotting.show(p)
except:
    pass