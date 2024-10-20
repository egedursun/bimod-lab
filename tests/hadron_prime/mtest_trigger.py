import time
import requests

##############################################################################################################

BASE_URL = "..."  # Update with true value
HADRON_NODE_ID = -1  # Update with true value
HADRON_NODE_ID_HASH = "..."  # Update with true value
HADRON_NODE_ACTIVATION_AUTH_KEY = "..."  # Update with true value
SIMULATION_STEPS = 10  # times
WAIT_BETWEEN_STEPS = 2  # seconds

##############################################################################################################

actuation_url = f"{BASE_URL}/app/hadron_prime/hadron_node/activate/{HADRON_NODE_ID}/{HADRON_NODE_ID_HASH}/"
actuation_auth_key = HADRON_NODE_ACTIVATION_AUTH_KEY
movement_limit = SIMULATION_STEPS


for i in range(0, movement_limit):
    try:
        response = requests.post(
            actuation_url,
            headers={
                "Authorization": f"Bearer {actuation_auth_key}"
            }
        )
        print(f"""
        ============================
        ACTUATION STEP {i+1}:
        ============================
        Response: {response.json()}
        ============================
        ...
        """)
        time.sleep(2)
    except Exception as e:
        print(f"Unexpected error has occurred: {e}")
        break
