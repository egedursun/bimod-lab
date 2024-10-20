import random
from fastapi import FastAPI, HTTPException
from starlette.requests import Request

app = FastAPI()


GRID_SIZE = 10  # (N x N) grid
FOOD_COUNT = 10
ROBOT_SENSOR_RANGE = 3
ROBOT_MAX_STEP_SIZE_X = 1
ROBOT_MAX_STEP_SIZE_Y = 1


ROBOT_ACTION_SPACE_X = [x for x in range(-ROBOT_MAX_STEP_SIZE_X, ROBOT_MAX_STEP_SIZE_X + 1)]
ROBOT_ACTION_SPACE_Y = [y for y in range(-ROBOT_MAX_STEP_SIZE_Y, ROBOT_MAX_STEP_SIZE_Y + 1)]


class RobotAgent:
    def __init__(self):
        self.x = random.randint(0, GRID_SIZE - 1)
        self.y = random.randint(0, GRID_SIZE - 1)
        self.food_eaten = 0
        self.board_size = GRID_SIZE

    def move(self, move_x, move_y):
        new_x = min(max(self.x + move_x, 0), self.board_size - 1)
        new_y = min(max(self.y + move_y, 0), self.board_size - 1)
        self.x = new_x
        self.y = new_y

    def act(self, move_x, move_y):
        if move_x not in ROBOT_ACTION_SPACE or move_y not in ROBOT_ACTION_SPACE:
            raise ValueError("move_x and move_y must be in the action space: ", str(ROBOT_ACTION_SPACE))
        self.move(move_x, move_y)

    def check_for_food(self, environment):
        if environment[self.x][self.y] == 'F':
            environment[self.x][self.y] = '.'
            self.food_eaten += 1
            return True
        return False

    def find_nearest_food(self, environment):
        nearest_food = None
        nearest_distance = float('inf')
        for i in range(self.board_size):
            for j in range(self.board_size):
                if environment[i][j] == 'F':
                    distance = abs(self.x - i) + abs(self.y - j)
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_food = (i, j)
        return nearest_food


class Environment:
    def __init__(self, size=GRID_SIZE, food_count=FOOD_COUNT):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.food_positions = []
        self.place_food(food_count)

    def place_food(self, food_count):
        for _ in range(food_count):
            while True:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                if self.grid[x][y] == '.':
                    self.grid[x][y] = 'F'
                    self.food_positions.append((x, y))
                    break

    def get_state(self):
        return self.grid


def visualize_environment(cur_robot, cur_environment):
    grid = [row[:] for row in cur_environment.grid]
    grid[cur_robot.x][cur_robot.y] = 'R'

    print("\nCurrent Environment:")
    print("====================")
    for row in grid:
        print(" ".join(row))
    print("====================")
    print(f"Robot Position: ({cur_robot.x}, {cur_robot.y})")
    print(f"Food Eaten: {cur_robot.food_eaten}")
    print("====================\n\n")
    return


env = Environment()
robot = RobotAgent()

###################################################################################################################


# Middleware: Allow CORS for all origins
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# GET /current_state - Return the CURRENT STATE of the robot.
@app.get("/current_state")
def current_state():
    return {"position_x": robot.x, "position_y": robot.y}


# GET /goal_state - Return the NEAREST FOOD LOCATION as the goal state.
@app.get("/goal_state")
def goal_state():
    nearest_food = robot.find_nearest_food(env.grid)
    if nearest_food is None:
        return {"goal": "No food remaining on the grid."}
    return {"goal_position_x": nearest_food[0], "goal_position_y": nearest_food[1]}


# GET /error_calculation - Calculate and return the ERROR VALUE between the robot's position and the nearest food.
@app.get("/error_calculation")
def error_calculation():
    nearest_food = robot.find_nearest_food(env.grid)
    if nearest_food is None:
        return {"error": "No food remaining on the grid"}
    error_x = nearest_food[0] - robot.x
    error_y = nearest_food[1] - robot.y
    return {"error_x": error_x, "error_y": error_y}


# GET /measurements - Return the robot's SENSORY MEASUREMENTS (which is based on proximity to food & sensor range).
@app.get("/measurements")
def measurements():
    return {
        "measurement_range": ROBOT_SENSOR_RANGE,
        "sensor_data": [
            {"x": i, "y": j, "has_food": env.grid[i][j] == 'F'}
            for i in range(max(0, robot.x - 3), min(robot.board_size, robot.x + 4))
            for j in range(max(0, robot.y - 3), min(robot.board_size, robot.y + 4))
        ]
    }


# GET /action_set - Return the AVAILABLE ACTION SET for the robot.
@app.get("/action_set")
def action_set():
    return {
        "available_actions": {
            "move_x": ROBOT_ACTION_SPACE_X,
            "move_y": ROBOT_ACTION_SPACE_Y
        }
    }


# GET /analytic_calculations - Perform ANALYTIC CALCULATIONS (if any) and return the results.
@app.get("/analytic_calculations")
def analytic_calculations():
    return {"analytic_calculations": None}


# POST /actuation - MOVE/ACTUATE the robot based on move_x and move_y.
@app.post("/actuation")
async def actuation(request: Request):
    try:
        data = await request.json()
        print(data)
        move_x = data.get("move_x", 0)
        move_y = data.get("move_y", 0)
        robot.act(move_x, move_y)
        food_eaten = robot.check_for_food(env.grid)
        visualize_environment(cur_environment=env, cur_robot=robot)
        return {
            "success": True,
            "new_position": {"position_x": robot.x, "position_y": robot.y},
            "food_eaten": food_eaten,
            "total_food_eaten": robot.food_eaten
        }
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


# GET /environment - Return the current environment condition including robot and food.
@app.get("/environment")
def environment():
    grid = [row[:] for row in env.grid]
    grid[robot.x][robot.y] = 'R'
    return {"grid": grid}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
