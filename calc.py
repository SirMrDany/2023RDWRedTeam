import rabbitmq

license_plates = {}


def process_message(init_info):
    if init_info.license_plate in license_plates.keys():
        # calculate fee
        print(init_info.license_plate)
        del license_plates[init_info.license_plate]
    else:
        license_plate = init_info.get('licenseplate')
        init_info.remove('licenseplate')
        license_plates[license_plate] = init_info

