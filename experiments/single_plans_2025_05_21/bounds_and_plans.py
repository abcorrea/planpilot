import json
import sys

JSON_PROPERTIES_FILE = "data/experiments-eval/properties"


def get_raw_data(json_file):
    # Read the JSON file
    try:
        with open(json_file, "r") as file:
            raw_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {json_file} was not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file {json_file}.")
        exit(1)
    return raw_data


def get_data(raw_data):

    bounds = {}
    plans = {}
    for key in raw_data:
        entry = raw_data[key]
        if "coverage" not in entry or entry["coverage"] != 1:
            continue

        domain = entry["domain"]
        problem = entry["problem"]
        plan_cost = int(entry["cost"])
        plan = entry["plan"]

        my_key = f"{domain}:{problem}"

        assert plan_cost not in bounds or bounds[my_key] == plan_cost
        bounds[my_key] = plan_cost
        plans[my_key] = plan

    return bounds, plans


def merge(data_lower_bound, data_higher_bound):
    data = data_higher_bound.copy()

    if data_lower_bound:
        questionable_keys = set(data_higher_bound.keys()) - set(data_lower_bound.keys())
        assert not questionable_keys, f"Missing keys in dict2: {questionable_keys}"

    for key in data_lower_bound:
        if key not in data_higher_bound:
            data[key] = data_lower_bound[key]
        assert data[key] >= data_lower_bound[key]
        data[key] = max(data[key], data_lower_bound[key])
    return data


def main():
    bound_raw_data = get_raw_data(JSON_PROPERTIES_FILE)
    bounds, plans = get_data(bound_raw_data)
    json.dump(bounds, sys.stdout, indent=4)
    print()
    print()
    json.dump(plans, sys.stdout, indent=4)
    print()


if __name__ == "__main__":
    main()
