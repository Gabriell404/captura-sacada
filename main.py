import keyboard
import time
from threading import Thread
import re
import requests as rq

prefixos_validos = [
    "246", "025", "641", "029", "038", "000", "740", "107", "031", "096", "318", "752", "248", "036", 
    "204", "225", "044", "263", "473", "222", "040", "215", "756", "748", "505", "229", "003", "707", 
    "024", "456", "214", "047", "037", "041", "004", "224", "626", "394", "233", "734", "612", "063",
    "604", "320", "653", "630", "249", "184", "479", "376", "074", "217", "065", "600", "755", "746", 
    "151", "045", "623", "611", "643", "638", "747", "072", "250", "749", "366", "637", "464", "634", 
    "208", "655", "610", "370", "021", "073", "719", "078", "069", "070", "477", "487", "751", "062", 
    "492", "488", "409", "230", "033"
]

def is_valid_codigo_de_barras(codigo):
    return len(codigo) >= 44 and any(codigo.startswith(str(prefixo)) for prefixo in prefixos_validos)

def listen():
    entrada_atual = ""

    def on_key_event(e):
        nonlocal entrada_atual

        if e.event_type == keyboard.KEY_DOWN:
            if e.name.isdigit() or e.name == 'enter' or e.name == 'tab':
                entrada_atual += e.name

                if e.name == 'enter' or e.name == 'tab':
                    if is_valid_codigo_de_barras(entrada_atual):
                        codigo_de_barra = re.sub("[^0-9]", "", entrada_atual)
                        print(f'Código de barra lido: {codigo_de_barra}')
                        
                        data = {
                            "codigo": codigo_de_barra
                        }
                        result = rq.post(f'http://10.54.56.147:8001/api/codigo', json=data)
                        print(f'result: {result}')
                        entrada_atual = ""
                        
                    else:
                        print("Código de barra inválido")
                    entrada_atual = ""

    keyboard.hook(on_key_event)

    while True:
        time.sleep(0.1)

thread = Thread(target=listen)
thread.start()
thread.join()