import simpy
from config import AppConfig
import random


class Terminal:
    def __init__(self, env : simpy.Environment):
        self.env = env
        self.berths = simpy.Resource(env, capacity=AppConfig.NUM_BERTHS)
        self.cranes = simpy.Resource(env, capacity=AppConfig.NUM_CRANES)
        self.trucks = simpy.Resource(env, capacity=AppConfig.NUM_TRUCKS)
    
    def dispatch_truck(self, truck):
        """
        Dispatch a truck after a delay.

        Args:
            truck: Truck to be dispatched.
        """
        yield self.env.timeout(AppConfig.TRUCK_MOVE_TIME  )
        self.trucks.release(truck)

    def unload_containers(self, vessel: int):
        """
        Unload containers from a vessel using cranes.

        Args:
            vessel: Vessel from which containers are to be unloaded.
        """
        crane = self.cranes.request()
        yield crane
        print(f"{self.env.now}: Quay crane starts unloading vessel {vessel}.")
        
        for i in range(AppConfig.CONTAINERS_PER_VESSEL):
            truck = self.trucks.request()
            yield truck
            yield self.env.timeout(AppConfig.CRANE_MOVE_TIME)
            print(f"{self.env.now}: Quay crane loads {i+1}/{AppConfig.CONTAINERS_PER_VESSEL} container onto a truck of Vessel {vessel}")
            self.env.process(self.dispatch_truck(truck))
        
        self.cranes.release(crane)

    def berth(self, vessel: int):
        """
        Berth a vessel at the terminal and start unloading containers.

        Args:
            vessel: Vessel to be berthed.
        """
        with self.berths.request() as berth:
            yield berth
            print(f"{self.env.now}: Vessel {vessel} berths at the terminal.")
            
            yield self.env.process(self.unload_containers(vessel))
            
            print(f"{self.env.now}: Vessel {vessel} unloaded.")
            
        print(f"{self.env.now}: Vessel {vessel} leaves the terminal.")

def vessel_generator(env: simpy.Environment, terminal: Terminal):
    """
    Generate vessels at random intervals and berth them at the terminal.

    Args:
        env (simpy.Environment): Simulation environment.
        terminal (Terminal): Terminal instance where vessels will berth.
    """
    vessel = 0
    while True:
        tb= int(random.expovariate(1 / AppConfig.INTER_ARRIVAL_TIME))
        yield env.timeout(tb)
        vessel += 1
        env.process(terminal.berth(vessel))

env = simpy.Environment()
terminal = Terminal(env)
env.process(vessel_generator(env, terminal))
env.run(until=AppConfig.SIMULATION_TIME)
