# traffic_optimizer.py

def calculate_green_time(vehicle_count):
    """
    Calculate green time based on traffic volume.

    Minimum green time: 20 seconds
    Maximum green time: 60 seconds
    """

    green_time = 20 + (vehicle_count * 2)

    green_time = max(20, min(green_time, 60))

    return green_time


def optimize_traffic(traffic_data):
    """
    Classical traffic signal optimization.

    traffic_data example:
    {
        "Road A": 8,
        "Road B": 27,
        "Road C": 5,
        "Road D": 12
    }
    """

    # Find road with highest traffic
    highest_road = max(
        traffic_data,
        key=traffic_data.get
    )

    highest_count = traffic_data[highest_road]

    # Calculate green time
    green_time = calculate_green_time(
        highest_count
    )

    # Traffic level
    if highest_count <= 5:
        traffic_level = "LOW"

    elif highest_count <= 12:
        traffic_level = "MEDIUM"

    else:
        traffic_level = "HIGH"

    return {
        "selected_road": highest_road,
        "vehicle_count": highest_count,
        "traffic_level": traffic_level,
        "green_time": green_time
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    traffic = {
        "Road A": 8,
        "Road B": 27,
        "Road C": 5,
        "Road D": 12
    }

    result = optimize_traffic(traffic)

    print("=" * 50)
    print("CLASSICAL TRAFFIC OPTIMIZER")
    print("=" * 50)

    print()

    print("Traffic Data:")

    for road, count in traffic.items():
        print(f"{road}: {count} vehicles")

    print()

    print("Selected Road:")
    print(result["selected_road"])

    print()

    print("Traffic Level:")
    print(result["traffic_level"])

    print()

    print("Green Time:")
    print(f'{result["green_time"]} seconds')

    print("=" * 50)