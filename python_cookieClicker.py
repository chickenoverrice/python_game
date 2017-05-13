# http://www.codeskulptor.org/#user40_6WjL7cMK3oZ9lJC.py

"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(80)

import poc_clicker_provided as provided

#NEW_GAME = provided.BuildInfo().clone()

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 500.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_cookies = 0.0
        self._cps = 1.0
        self._time = 0.0
        self._total_cookies = 0.0
        self._history =  [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        state_1 = "Time: " + str(self._time)
        state_2 = "Current Cookies: " + str(self._current_cookies)
        state_3 = "CPS: " + str(self._cps)
        state_4 = "Total Cookies: " + str(self._total_cookies)
        return state_1 + " " + state_2 + " " + state_3 + " " + state_4
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        cost = cookies - self._current_cookies
        time = 0.0
        if cost > 0.0:
            time = math.ceil(cost/self._cps)
        else:
            time = 0.0
        return time
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_cookies += (self._cps * time)
            #self._total_cookies += self._current_cookies
            self._total_cookies += self._cps * time
            self._time += time
        else:
            pass
        #print self._time, self._cps, self._current_cookies, self._total_cookies
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookies))
        else:
            pass
        
       
    
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    newclicker = ClickerState()
    new_game = build_info.clone()
    while newclicker.get_time() <= duration:
        item = strategy(newclicker.get_cookies(), newclicker.get_cps(), newclicker.get_history(),
                    duration - newclicker.get_time(), new_game)        
        if item == None:
            break
        else:
            time = newclicker.time_until(new_game.get_cost(item))
            if time <= duration - newclicker.get_time():
                newclicker.wait(time)
                newclicker.buy_item(item, new_game.get_cost(item), new_game.get_cps(item))
                new_game.update_item(item)
            else:
                break
    
    left_time = duration - newclicker.get_time()
    if left_time > 0.0:
        newclicker.wait(left_time)

    return newclicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    pick = None
    cost = float('inf')
    for item in build_info.build_items():
        if build_info.get_cost(item) < cost: 
            cost = build_info.get_cost(item)
            if (time_left * cps + cookies) >= cost:
                pick = item
        
    return pick

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    pick = None
    cost = float('-inf')
    for item in build_info.build_items():
        if build_info.get_cost(item) > cost: 
            cost = build_info.get_cost(item)
            if (time_left * cps + cookies) >= cost:
                pick = item
    
    return pick


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    pick = None
    ratio = float('-inf')
    for item in build_info.build_items():
        if build_info.get_cps(item) / build_info.get_cost(item) > ratio: 
            cost = build_info.get_cost(item)
            ratio = build_info.get_cps(item) / build_info.get_cost(item)
            if (time_left * cps + cookies) >= cost:
                pick = item
    
    return pick
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("None", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
    

