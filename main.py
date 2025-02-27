'''
The main module which spawns a gui and a effect thread and opens a socket connection to the specified
host. The effect algorithm is in the effect module. Change this file to develop your effect.
Change the host and port to your needs in this main file and also the values representing your led configuration.

Created on 27.11.2014

@author: Fabian Hertwig
'''

from threading import Thread
import gui
import hyperion
import runpy
import json_client


# Change this to your Pis / Hyperion data. There is no harm done if wrong data is set here.
# The connection will simply time out.
hyperion_host = 'rpi1.lan'
#hyperion_host = '192.168.178.32'
hyperion_port = 19444

# Change this according to your led configuration.
horizontal_led_num = 18
vertical_led_num = 11
first_led_offset_num = 0
leds_in_clockwise_direction = True
has_corner_leds = False


def run_effect():
    """
    Runs the module effect. Copy any hyperion effect code in this module or create your own.
    Note that effects that call hyperion.setColor(r, g, b) or hyperion.setImage(img) are not supported.
    """
    runpy.run_module("effect")


def main():
    hyperion.init(horizontal_led_num, vertical_led_num, first_led_offset_num, leds_in_clockwise_direction,
                  has_corner_leds)

    # Open the connection to the json server. Uncomment if you do not want to send data to the server.
    json_client.open_connection(hyperion_host, hyperion_port)

    # create own thread for the effect
    effect_thread = Thread(target=run_effect)

    effect_thread.start()
    gui.createWindow()

    # After the window was closed abort the effect through the fake hyperion module
    hyperion.set_abort(True)
    # wait for the thread to stop
    effect_thread.join()

    # close potential connections
    json_client.close_connection()
    print("Exiting")


if __name__ == '__main__':
    main()

