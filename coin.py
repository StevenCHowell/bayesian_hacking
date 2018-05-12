import time
import numpy as np
import bokeh.plotting
import bokeh.io
import bokeh.layouts
from bokeh.palettes import Category10_10 as palette


# p_a = 1.0 / 100.0
# p_ba = 1.0
# p_na = 99.0 / 100.0
# p_bna = 0.5 ** 10
# p_b = p_ba * p_a + p_bna * p_na
# p_ab = p_ba * p_a / p_b


def flip_generator(coins, *, n_flips=10):
    n_coins = len(coins)
    
    coin_index = np.random.randint(0, n_coins, 1)[0]
    drawn_coin = coins[coin_index]
    coin_unfair = drawn_coin == 1  # did we get the unfair coin?

    if coin_unfair:
        all_heads = True
    else: 
        for j in range(n_flips):
            flip = np.random.rand()  # random number between [0, 1)

            if flip < 0.5:
                all_heads = True
            else:
                all_heads = False
                break

    if all_heads:
        # report the index and if the coin was unfair
        yield coin_unfair


def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = bokeh.io.curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = '► Play'
        
        bokeh.io.curdoc().remove_periodic_callback(callback_id)


def animate_update():
    global n_all_heads
    global n_unfair
    n_max = 100000 
    n_show = 500

    if n_all_heads > n_max:
        bokeh.io.curdoct().remove_periodic_callback(callback_id)
    
    else:
        new_data = dict(x=[0], y=[0])
        res = list(flip_generator(coins))
        if res:
            n_all_heads += 1
            if res[0]:
                n_unfair += 1
            frac_unfair = n_unfair / n_all_heads

            new_data['x'] = [n_all_heads]  
            new_data['y'] = [frac_unfair]  
            
            test_data.stream(new_data, n_show)

            bokeh.io.push_notebook(handle=handle)

            # time.sleep(slider.value)


# 100 coin all fair
n_coins = 100
coins = np.zeros(n_coins, dtype=np.int)  

# make one coin unfair
coins[np.random.randint(1, 100, 1)] = 1  

# generate the figure
fig = bokeh.plotting.figure(plot_width=800, plot_height=400)
test_data = bokeh.models.sources.ColumnDataSource(data=dict(x=[0], y=[0]))
line = fig.line("x", "y", source=test_data)

# set the globals
callback_id = None
n_all_heads = 0
n_unfair = 0

# define the speed slider
slider = bokeh.models.Slider(start=0, end=1, value=1, step=0.1, title="Speed")
# slider.on_change('value', slider_update)

# define the play button
button = bokeh.models.Button(label='► Play', width=60)
button.on_click(animate)

# layout the app
layout = bokeh.layouts.layout([
    [fig],
    [slider, button],
], sizing_mode='scale_width')
bokeh.io.curdoc().add_root(layout)

# execute the app
bokeh.io.curdoc().title = "Coins"