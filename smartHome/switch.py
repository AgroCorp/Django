import RPi.GPIO as GPIO

ports = [31, 36, 33, 35]


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    for pin in ports:
        GPIO.setup(pin, GPIO.OUT)


def get_switch_status():
    switch_port = 0
    states = {}

    for i in range(4):
        if GPIO.input(ports[i]):
            states[i + 1] = 'on'
        else:
            states[i+1] = 'of'

        # if i == 0:
        #     switch_port = 31
        #     if GPIO.input(switch_port):
        #         states[i + 1] = "on"
        #     else:
        #         states[i + 1] = "off"
        # elif i == 1:
        #     switch_port = 36
        #     if GPIO.input(switch_port):
        #         states[i + 1] = "on"
        #     else:
        #         states[i + 1] = "off"
        # elif i == 2:
        #     switch_port = 33
        #     if GPIO.input(switch_port):
        #         states[i + 1] = "on"
        #     else:
        #         states[i + 1] = "off"
        # elif i == 3:
        #     switch_port = 35
        #     if GPIO.input(switch_port):
        #         states[i + 1] = "on"
        #     else:
        #         states[i + 1] = "off"

    return states


def switch_toggle(number, state_to):
    try:
        switch_port = ports[int(number) - 1]
    except ValueError:
        switch_port = -1


    # if number == "1":
    #     switch_port = 6
    # elif number == "2":
    #     switch_port = 16
    # elif number == "3":
    #     switch_port = 13
    # elif number == "4":
    #     switch_port = 19
    #
    # ports[int(number)]

    response = {}

    if switch_port != -1:
        if state_to == "off":
            GPIO.output(switch_port, GPIO.LOW)
            response[number] = "off"
        elif state_to == "on":
            GPIO.output(switch_port, GPIO.HIGH)
            response[number] = "on"
    print(response)
    print(switch_port)
    return response


def clean():
    GPIO.cleanup(ports)
