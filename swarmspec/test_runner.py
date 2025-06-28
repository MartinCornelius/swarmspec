import yaml
import time
import math

from swarmspec.drone import Drone

def load_scenario(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def run_test(scenario):
    drones = []
    for d in scenario["drones"]:
        drone = Drone(d["id"], d["initial_position"])
        drone.set_waypoints(d["waypoints"])
        drones.append(drone)

    tolerance = scenario.get("tolerance", 5)
    max_time = scenario.get("max_time", 60)
    start_time = time.time()
    all_finished = False

    while not all_finished:
        dt = 0.1
        time.sleep(dt)
        all_finished = True

        for drone in drones:
            finished = drone.step(dt)
            if not finished:
                all_finished = False

    print("now going for the reuslts")
    results = {}
    for drone in drones:
        last_wp = drone.waypoints[-1]
        dist = math.dist(drone.position, last_wp)
        results[drone.id] = dist <= tolerance

    print(f"ALL DONE: {time.time() - start_time}")
    return results

if __name__ == "__main__":
    print("started airframe...")
    scenario = load_scenario("scenarios/example_scenario.yaml")
    print("loaded scenario...")
    results = run_test(scenario)
    print("done running test scenario...")
    for drone_id, passed in results.items():
        print(f"{drone_id}: {"PASS" if passed else "FAIL"}")
