import csv
import math
import apicalls
from datetime import datetime

license_plates = {}


def process_message(init_info):
    # Get license plate from dictionary
    license_plate = init_info.get('licenseplate')

    # Exits toll gate
    if license_plate in license_plates.keys():
        current_info = license_plates.get(license_plate)
        lat1 = current_info.get('lat')
        lon1 = current_info.get('lon')
        lat2 = init_info.get('lat')
        lon2 = init_info.get('lon')
        fee = 0

        distance = math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 100

        vehicle_info = eval(apicalls.getVehicleInfo(license_plate))
        # fuel_category = eval(apicalls.getFuelInfo(license_plate))

        enter_time = datetime.fromtimestamp(current_info.get('time'))
        enter_hour = enter_time.hour
        leave_time = datetime.fromtimestamp(init_info.get('time'))
        leave_hour = leave_time.hour

        peak = 1

        if 7 < enter_hour < 9 or 16 < leave_hour < 18:
            peak = 1.5

        mass = float(vehicle_info[0].get('massa_rijklaar')) / 1000

        # GET THESE FROM RDW OPEN API
        fuel_type = 1
        fuel_usage = 1

        # get things from dany
        fee = 0.0136 * mass**2 * distance + 0.0033 * peak * fuel_type * fuel_usage * distance

        # calculate fee
        print(license_plate + ' pays ' + str(fee))

        history_dict = {'license_plate': license_plate,
                        'entry_lat': current_info.get('lat'), 'entry_lon': current_info.get('lon'),
                        'entry_id': current_info.get('id'), 'entry_time': current_info.get('time'),
                        'exit_lat': init_info.get('lat'), 'exit_lon': init_info.get('lon'),
                        'exit_id': init_info.get('id'), 'exit_time': init_info.get('time'), 'fee': fee,
                        'distance': distance}
        # Open the CSV file in append mode
        with open('history.csv', 'a', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.DictWriter(csvfile, fieldnames=history_dict.keys())
            # If the file is empty, write the header row
            if csvfile.tell() == 0:
                writer.writeheader()
            # Write the row to the CSV file
            writer.writerow(history_dict)

        del license_plates[license_plate]
    else:
        # Enters toll gate
        del init_info['licenseplate']
        license_plates[license_plate] = init_info

