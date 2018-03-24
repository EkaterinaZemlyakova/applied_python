def process(trains: list, events: list, car_name: str) -> int:
    try:
        for event in events:
            if event['type'] == 'walk':
                train_index, car_index = get_info_by_passenger(trains, event['passenger'])
                select_car = car_index + event['distance']

                if select_car < 0:
                    raise IndexError

                trains[train_index]['cars'][select_car]['people'].append(event['passenger'])
                trains[train_index]['cars'][car_index]['people'].remove(event['passenger'])

            elif event['type'] == 'switch':
                if event['cars'] > 0:
                    train_from_index = get_train_index_by_name(trains, event['train_from'])
                    train_to_index = get_train_index_by_name(trains, event['train_to'])

                    switch_cars = trains[train_from_index]['cars'][-event['cars']:]
                    trains[train_to_index]['cars'].extend(switch_cars)

                    for car in switch_cars:
                        trains[train_from_index]['cars'].remove(car)
                else:
                    raise ValueError

        for train in trains:
            for car in train['cars']:
                if car['name'] == car_name:
                    return len(car['people'])

    except Exception:
        return -1


def get_info_by_passenger(trains: list, name: str) -> list:
    for train in trains:
        for car in train['cars']:
            if name in car['people']:
                return [trains.index(train), train['cars'].index(car)]


def get_train_index_by_name(trains: list, name: str) -> int:
    found = list(filter(lambda train: train['name'] == name, trains))

    if len(found) == 1:
        return trains.index(found[0])

    raise IndexError