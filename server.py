from model import RandomModel, Dirt
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "#4895ef",
                 "r": 0.5}

    if (isinstance(agent, Dirt)):
        portrayal["Color"] = "#dda15e"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

model_params = {
    "N": UserSettableParameter("slider", "Number of Roombas", 5, 1, 10, 1),
    "width":10,
    "height":10,
    "dirty_density": UserSettableParameter("slider", "Dirty Cell Density", 0.6, 0.1, 1.0, 0.1),
    "time_limit" : UserSettableParameter("slider", "Time Limit", 60, 1, 300, 1)
    }

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(RandomModel, [grid], "Roomba Madness", model_params)
                       
server.port = 8521 # The default
server.launch()