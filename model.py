import enum
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from agent import Roomba, Dirt
import time

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, dirty_density=0.6, time_limit=60):
        print(N)
        self.num_agents = N
        self.grid = Grid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
        self.time = time.time()
        self.time_limit = time_limit
        self.initial_dirty_cells = 0
        self.num_cells = 0

        for cont, x, y in self.grid.coord_iter():
            if self.random.random() < dirty_density:
                if (x,y) != (0,0):
                    new_cell = Dirt((x,y), self)
                    self.grid._place_agent((x, y), new_cell)
                    self.schedule.add(new_cell)
                    self.initial_dirty_cells += 1
            self.num_cells += 1
        
        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            a = Roomba(i+1000, self) 
            self.schedule.add(a)
            self.grid.place_agent(a, (0,0))
        

    def step(self) -> None:
        '''Advance the model by one step.'''
        self.schedule.step()
        dc = self.getDirtyCells()
        cc = self.getCleanCells()
        t = self.getTime()
        if dc == 0:
            self.running = False
            self.log("No more dirty cells", t, dc, cc, 0, 100)
        if t > self.time_limit:
            self.running = False
            self.log("Time limit exceeded", t, dc, cc, self.percentage(dc, self.initial_dirty_cells), self.percentage(cc, self.num_cells))

    def getDirtyCells(self) -> int:
        dirty_cells = 0
        for cont, x, y in self.grid.coord_iter():
            if type(cont).__name__ == "Dirt":
                dirty_cells += 1
        return dirty_cells

    def getCleanCells(self) -> int:
        clean_cells = 0
        for cont, x, y in self.grid.coord_iter():
            if type(cont).__name__ == "NoneType":
                clean_cells += 1
        return clean_cells

    def getTime(self) -> float:
        return round(time.time() - self.time, 2)

    def log(self, log_type : str, time : float, dirty_cells : int, clean_cells : int, p_dirty_cells : float, p_clean_cells : float) -> None:
        with open("log.txt", 'a') as file:
                file.write(f"{log_type}\nTime: {time}, Time Limit: {self.time_limit}\nDirty Cells: {dirty_cells}, Clean Cells: {clean_cells}\nDirty Cell Percentage: %{p_dirty_cells}, Clean Cell Percentage: %{p_clean_cells} \n")
                file.write(f"Agents: {self.num_agents}\n")
                for r in self.getAgentMovements():
                    file.write(f"Agent: {r[0]}, Movements: {r[1]}\n")
                file.write('\n')

    def percentage(self, n, total) -> float:
        q = n/total
        return round(q*100, 2)

    def getAgentMovements(self):
        agents = self.schedule.agents
        for i, agent in enumerate(agents):
            if type(agent).__name__ == "Roomba":
                yield (agent.unique_id, agent.movements)

            