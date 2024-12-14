from gpiozero import LED
from time import sleep
from I2C_LCD_driver import lcd
import board
import adafruit_dht
from time import *
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define GPIO pins for devices
living_light = LED(18)
bath_light = LED(17)
bed_light = LED(23)
air_con = LED(27)
fans = LED(22)

# Set the sensor type and the pin it’s connected to
sensor = adafruit_dht.DHT11(board.D4)  # Replace board.D22 with your actual GPIO pin
mylcd = lcd()

def set_bathroom_light(open):
    if open:
        bath_light.on()
        return "Bathroom light on"
    else:
        bath_light.off()
        return "Bathroom light off"

def set_living_room_light(open):
    if open:
        living_light.on()
        return "Living room light on"
    else:
        living_light.off()
        return "Living room light off"

def set_bedroom_light(open):
    if open:
        bed_light.on()
        return "Bedroom light on"
    else:
        bed_light.off()
        return "Bedroom light off"

def set_fan(open):
    if open:
        fans.on()
        return "Fan on"
    else:
        fans.off()
        return "Fan off"

def set_air_conditioner(open):
    if open:
        air_con.on()
        return "Air conditioner on"
    else:
        air_con.off()
        return "Air conditioner off"

current_temp = 25
def set_air_conditioner_temperature(up):
    global current_temp
    if up:
        current_temp = current_temp + 2
        return "Air conditioner temperature up to {:.1f} C".format(current_temp)
    else:
        current_temp = current_temp - 2
        return "Air conditioner temperature down to {:.1f} C".format(current_temp)

def update_lcd_display():
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        if temperature is not None:
            if not air_con.is_lit:  # If air conditioner is off
                mylcd.lcd_clear()
                print("clearing lcd")
                sleep(1)  # Adjust sleep time as needed for your display
                mylcd.lcd_display_string("Temp: {:.1f} C".format(temperature), 1, 3)
                mylcd.lcd_display_string("Humidity: {:.1f}%".format(humidity), 2, 3)
            else:  # If air conditioner is on
                global current_temp
                mylcd.lcd_display_string("AC Temp: {:.1f} C".format(current_temp), 1, 3)
                mylcd.lcd_display_string("Humidity: {:.1f}%".format(humidity), 2, 3)
    except RuntimeError as e:
        print('Failed to read sensor data, retrying...', e)


# Flask API Endpoints
@app.route('/bathroom_light', methods=['POST'])
def bathroom_light():
    data = request.json
    status = data.get('open', None)
    if status is None:
        return jsonify({"status": "not", "message": "Invalid parameters"})
    message = set_bathroom_light(status)
    return jsonify({"status": "success", "message": message})

@app.route('/living_room_light', methods=['POST'])
def living_room_light():
    data = request.json
    status = data.get('open', None)
    if status is None:
        return jsonify({"status": "not", "message": "Invalid parameters"})
    message = set_living_room_light(status)
    return jsonify({"status": "success", "message": message})

@app.route('/bedroom_light', methods=['POST'])
def bedroom_light():
    data = request.json
    status = data.get('open', None)
    if status is None:
        return jsonify({"status": "not", "message": "Invalid parameters"})
    message = set_bedroom_light(status)
    return jsonify({"status": "success", "message": message})

@app.route('/fan', methods=['POST'])
def fan():
    data = request.json
    status = data.get('open', None)
    if status is None:
        return jsonify({"status": "not", "message": "Invalid parameters"})
    message = set_fan(status)
    return jsonify({"status": "success", "message": message})

@app.route('/air_conditioner', methods=['POST'])
def air_conditioner():
    data = request.json
    status = data.get('open', None)
    if status is None:
        return jsonify({"status": "not", "message": "Invalid parameters"})
    message = set_air_conditioner(status)
    update_lcd_display()
    return jsonify({"status": "success", "message": message})

@app.route('/air_conditioner_temperature', methods=['POST'])
def air_conditioner_temperature():
    data = request.json
    up = data.get('up', None)
    if up is None:
        return jsonify({"status": "not", "message": "Invalid parameters"})
    message = set_air_conditioner_temperature(up)
    update_lcd_display()
    return jsonify({"status": "success", "message": message})

@app.route('/temperature', methods=['GET'])
def temperature():
    update_lcd_display()
    return jsonify({"status": "success", "message": f"Current temperature is {sensor.temperature}°C"})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=4000)

