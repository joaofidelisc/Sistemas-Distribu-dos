import uuid


def get_integrante_joaofidelis():
    fidelis_item = {
    'id': 'JoaoVitorFidelisCardozo_' + str(uuid.uuid4()),
    'lastName': 'Fidelis Cardozo',
    'informationsFromSchool':{
        'anoDeIngresso': 2019,
        'curso': 'Engenharia de Computação',
        'RA': 769719,
    },
}
    return fidelis_item

def get_integrante_rafaeltury():
    tury_item = {
        'id': 'RafaelTuryMinatel_' + str(uuid.uuid4()),
        'lastName': 'Tury Minatel',
        'informationsFromSchool':{
        'anoDeIngresso': 2019,
        'curso': 'Engenharia de Computação',
        'RA': 761725,
        },
    }
    return tury_item

def get_integrante_thiagoaraujo():
    araujo_item = {
    'id': 'ThiagoAraujo_' + str(uuid.uuid4()),
    'lastName': 'Araujo',
    'informationsFromSchool':{
        'anoDeIngresso': 2019,
        'curso': 'Engenharia de Computação',
        'RA': 769850,
        },
    }
    return araujo_item


