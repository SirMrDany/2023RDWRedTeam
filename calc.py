license_plates = {}


def process_message(init_info):
    if init_info.get('licenseplate') in license_plates.keys():
        # calculate fee
        print(init_info.get('licenseplate'))
        del license_plates[init_info.get('licenseplate')]
    else:
        license_plate = init_info.get('licenseplate')
        del init_info['licenseplate']
        license_plates[license_plate] = init_info

