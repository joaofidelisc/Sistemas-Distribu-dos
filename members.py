import uuid


def get_member_joaofidelis():
    fidelis_item = {
    'id': 'JoaoVitorFidelisCardozo_' + str(uuid.uuid4()),
    'lastName': 'Fidelis Cardozo',
    'collegeInformation':{
        'yearOfEntry': 2019,
        'course': 'Engenharia de Computação',
        'studentID': 769719,
        },
    }
    return fidelis_item

def get_member_rafaeltury():
    tury_item = {
    'id': 'RafaelTuryMinatel_' + str(uuid.uuid4()),
    'lastName': 'Tury Minatel',
    'collegeInformation':{
        'yearOfEntry': 2019,
        'course': 'Engenharia de Computação',
        'studentID': 761725,
        },
    }
    return tury_item

def get_member_thiagoaraujo():
    araujo_item = {
    'id': 'ThiagoAraujo_' + str(uuid.uuid4()),
    'lastName': 'Araujo',
    'collegeInformation':{
        'yearOfEntry': 2019,
        'course': 'Engenharia de Computação',
        'studentID': 769850,
        },
    }
    return araujo_item


