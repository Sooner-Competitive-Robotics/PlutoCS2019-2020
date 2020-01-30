#!/usr/bin/env python3

import pygame, serial, json, socketserver

import help_lib as hl

def main():
    """Send controller signal to collision avoidance"""

    global joystick, DEAD_ZONE_Y, logger, c_status

    # Initial status
    c_status = "Disconnected"

    # Dead zone for y-axis
    DEAD_ZONE_Y = 0.1

    #setup
    pygame.display.init()
    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Create logger
    logger = hl.create_logger(__name__)

    class Handler_TCPServer(socketserver.StreamRequestHandler):
        """Send to signals to collision avoidance"""

        def handle(self):

            global joystick, DEAD_ZONE_Y, c_status

            c_status = "Connected"
            logger.info(c_status)

            # Default control dictionary
            control_dict = {
                "left_stick": 0.0,
                "right_stick": 0.0,
                "led": False,
                "autonomous_signal": False
            }

            # While connection exists
            while True:

                try:

                    pygame.event.get()

                    # Turn on LED if A is pressed 
                    if joystick.get_button(0) == 1:
                        contro_dict["led"] = True

                    # Turn off LED if B is pressed
                    elif joystick.get_button(1) == 1:
                        control_dict["led"] = False

                    # Read y-positions of left and right sticks
                    control_dict["leftStick"] = joystick.get_axis(1)
                    control_dict["rightStick"] = joystick.get_axis(3)

                    # If y-pos of sticks are in "dead zone", round them to 0
                    # TODO: pygame can do this for us
                    if abs(control_dict["leftStick"]) < DEAD_ZONE_Y:
                        control_dict["leftStick"] = 0
                    if abs(control_dict["rightStick"]) < DEAD_ZONE_Y:
                        control_dict["rightStick"] = 0

                    # Dump dictionary to a line string and send to collision avoidance
                    send_msg = json.dumps(send_dict) + "\n"
                    send_msg = send_msg.encode()

                    self.request.sendall(send_msg)

                # Bad practice but lazy right now
                except:

                    c_status = "Disconnected"
                    break

    # Start server and serve forever
    HOST, PORT = "localhost", 9001

    socketserver.TCPServer.allow_reuse_address = True
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    tcp_server.serve_forever()
        
if __name__ == "__main__":
    main()


