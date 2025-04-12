from gpiozero import MCP3008
import math
import time
import RPi.GPIO as GPIO
import csv
import random
import socket
import spidev

GPIO.setwarnings(False)


R0 = 8400.0
R1 = 10000.0
analog_input_X = MCP3008(channel=0)
analog_input_Y = MCP3008(channel=1)
analog_input_Z = MCP3008(channel=2)  
analog_input_L = MCP3008(channel=3)  
analog_input_M = MCP3008(channel=7)  
analog_input_N = MCP3008(channel=5)  

# PID Parameters ============================================

Kp = 50
Ki = 0.005
Kd = 1
kp = 50
ki = 0.005
kd = 1
dt = 0
Dt = 0.5
I_X = 0
preP_X = 0
I_Y = 0
preP_Y = 0
I_Z = 0
preP_Z = 0
I_L = 0
preP_L = 0
I_M = 0
preP_M = 0
I_N = 0
preP_N = 0
integral_max = 200000  

# GPIO Setup ================================
GPIO.setmode(GPIO.BCM)
# Peltier =====================================
pin_A1 = 18
pin_A2 = 27
pin_B1 = 24
pin_B2 = 25
pin_C1 = 12
pin_C2 = 13
pin_D1 = 5
pin_D2 = 6
pin_E1 = 19
pin_E2 = 16
pin_F1 = 26
pin_F2 = 20
GPIO.setup(pin_A1, GPIO.OUT)
GPIO.setup(pin_A2, GPIO.OUT)
GPIO.setup(pin_B1, GPIO.OUT)
GPIO.setup(pin_B2, GPIO.OUT)
GPIO.setup(pin_C1, GPIO.OUT)
GPIO.setup(pin_C2, GPIO.OUT)
GPIO.setup(pin_D1, GPIO.OUT)
GPIO.setup(pin_D2, GPIO.OUT)
GPIO.setup(pin_E1, GPIO.OUT)
GPIO.setup(pin_E2, GPIO.OUT)
GPIO.setup(pin_F1, GPIO.OUT)
GPIO.setup(pin_F2, GPIO.OUT)

freq = 20
duty = 0
pwm_A1 = GPIO.PWM(pin_A1, freq)
pwm_A2 = GPIO.PWM(pin_A2, freq)
pwm_A1.start(0)
pwm_A2.start(0)
pwm_B1 = GPIO.PWM(pin_B1, freq)
pwm_B2 = GPIO.PWM(pin_B2, freq)
pwm_B1.start(0)
pwm_B2.start(0)
pwm_C1 = GPIO.PWM(pin_C1, freq)
pwm_C2 = GPIO.PWM(pin_C2, freq)
pwm_D1 = GPIO.PWM(pin_D1, freq)
pwm_D2 = GPIO.PWM(pin_D2, freq)
pwm_E1 = GPIO.PWM(pin_E1, freq)
pwm_E2 = GPIO.PWM(pin_E2, freq)
pwm_F1 = GPIO.PWM(pin_F1, freq)
pwm_F2 = GPIO.PWM(pin_F2, freq)
pwm_C1.start(0)
pwm_C2.start(0)
pwm_D1.start(0)
pwm_D2.start(0)
pwm_E1.start(0)
pwm_E2.start(0)
pwm_F1.start(0)
pwm_F2.start(0)


HOST = '192.168.1.152'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  

print("Waiting for Unity client...")
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")



# ===========================================

def get_target_temp_X(elapsed_time):
    
    if elapsed_time <= 30.0:
        return (5/30) * elapsed_time + 20
    else:
        cycle_time = (elapsed_time - 30) % (80)  
        if cycle_time <= 15: 
            return -(5 / 15) * cycle_time + 25.0
        elif cycle_time <= 45:  
            return (5 / 30) * (cycle_time - 15) + 20.0
        elif cycle_time <= 50:
            return -(5 / 5) * (cycle_time - 45) + 25.0
        else:
            return (5 / 30 ) * (cycle_time - 50) + 20.0
def get_target_temp_Y(elapsed_time):
    
    if elapsed_time <= 7.5:  
        return 20.0
    elif elapsed_time <= 45:
        return (5/37.5) * (elapsed_time - 7.5) + 20
    else:
        cycle_time = (elapsed_time - (30 + 15)) % (80) 
        if cycle_time <= 12.5:  
            return -(5 / 12.5) * cycle_time + 25.0
        elif cycle_time <= 35:  
            return (5 / 22.5) * (cycle_time - 12.5) + 20.0
        elif cycle_time <= 42.5:
            return -(5 / 7.5) * (cycle_time - 35) + 25.0
        else:
            return (5 / 37.5 ) * (cycle_time - 42.5) + 20.0
def get_target_temp_N(elapsed_time):
    
    if elapsed_time <= 17.5:  
        return 20.0
    elif elapsed_time <= 57.5:
        return (5/40.0) * (elapsed_time - 17.5) + 20
    else:
        cycle_time = (elapsed_time - (30 + 27.5)) % (80) 
        if cycle_time <= 10:  
            return -(5 / 10) * cycle_time + 25.0
        elif cycle_time <= 30:  
            return (5 / 20) * (cycle_time - 10) + 20.0
        elif cycle_time <= 40:
            return -(5 / 10) * (cycle_time - 30) + 25.0
        else:
            return (5 / 40 ) * (cycle_time - 40) + 20.0
def get_target_temp_M(elapsed_time):
    
    if elapsed_time <= 30:  
        return 20.0
    elif elapsed_time <= 67.5:
        return (5/37.5) * (elapsed_time - 30) + 20
    
    else:
        cycle_time = (elapsed_time - (30 + 37.5)) % (80)  
        if cycle_time <= 7.5: 
            return -(5 / 7.5) * cycle_time + 25.0
        elif cycle_time <= 30:  
            return (5 / 22.5) * (cycle_time - 7.5) + 20.0
        elif cycle_time <= 42.5:
            return -(5 / 12.5) * (cycle_time - 30) + 25.0
        else:
            return (5 / 37.5) * (cycle_time - 42.5) + 20.0

while True:
    reading_X = analog_input_X.value
    voltage_adc_X = reading_X * 3.3 
    R_X = R0 * (6.6 - voltage_adc_X) / (3.7467 + voltage_adc_X)
    
    x = (1 / 3435) * math.log(R_X / R1) + 1 / 298
    temp_X = 1 / x - 273

    
    P_X = 20.0 - temp_X  
    I_X += P_X * Dt
    De_X = (P_X - preP_X) / Dt
    preP_X = P_X
    U_X = 15 * P_X + 0.5 * I_X + 3 * De_X

    duty_X = min(100, abs(U_X))  
    if P_X>0 and U_X>0:
        pwm_A1.ChangeDutyCycle(duty_X)
        pwm_A2.ChangeDutyCycle(0)
        print(f'x={temp_X:.2f}')
    elif P_X<0 and U_X<0:
        pwm_A2.ChangeDutyCycle(duty_X)
        pwm_A1.ChangeDutyCycle(0)
        print(f'x={temp_X:.2f}')
        print()
        
    reading_Y = analog_input_Y.value
    voltage_adc_Y = reading_Y * 3.3 
    R_Y = R0 * (6.6 - voltage_adc_Y) / (3.7467 + voltage_adc_Y)
    
    y = (1 / 3435) * math.log(R_Y / R1) + 1 / 298
    temp_Y = 1 / y - 273

    
    P_Y = 20.0 - temp_Y  
    I_Y += P_Y * Dt
    De_Y = (P_Y - preP_Y) / Dt
    preP_Y = P_Y
    U_Y = 15 * P_Y + 0.5 * I_Y + 3 * De_Y

    duty_Y = min(100, abs(U_Y))  
    if P_Y>0 and U_Y>0:
        pwm_B1.ChangeDutyCycle(duty_Y)
        pwm_B2.ChangeDutyCycle(0)
        print(f'y={temp_Y:.2f}')
    elif P_Y<0 and U_Y<0:
        pwm_B2.ChangeDutyCycle(duty_Y)
        pwm_B1.ChangeDutyCycle(0)
        print(f'y={temp_Y:.2f}')
        print()
    
    reading_N = analog_input_N.value
    voltage_adc_N = reading_N * 3.3 
    R_N = R0 * (6.6 - voltage_adc_N) / (3.747 + voltage_adc_N)
    
    n = (1 / 3435) * math.log(R_N / R1) + 1 / 298
    temp_N = 1 / n - 273
    # ==============================================================

   
    reading_N = analog_input_N.value
    voltage_adc_N = reading_N * 3.3 
    R_N = R0 * (6.6 - voltage_adc_N) / (3.7467 + voltage_adc_N)
    
    n = (1 / 3435) * math.log(R_N / R1) + 1 / 298
    temp_N = 1 / n - 273

    
    P_N = 40.0 - temp_N  
    I_N += P_N * Dt
    De_N = (P_N - preP_N) / Dt
    preP_N = P_N
    U_N = 15 * P_N + 0.5 * I_N + 3 * De_N

    duty_N = min(100, abs(U_N))  
    if P_N>0 and U_N>0:
        pwm_F1.ChangeDutyCycle(duty_N)
        pwm_F2.ChangeDutyCycle(0)
        print(f'n={temp_N:.2f}')
    elif P_N<0 and U_N<0:
        pwm_F2.ChangeDutyCycle(duty_N)
        pwm_F1.ChangeDutyCycle(0)
        print(f'n={temp_N:.2f}')
        print()

    reading_M = analog_input_M.value
    voltage_adc_M = reading_M * 3.3 
    R_M = R0 * (6.6 - voltage_adc_M) / (3.7467 + voltage_adc_M)
    
    m = (1 / 3435) * math.log(R_M / R1) + 1 / 298
    temp_M = 1 / m - 273

    
    P_M = 40.0 - temp_M  
    I_M += P_M * Dt
    De_M = (P_M - preP_M) / Dt
    preP_M = P_M
    U_M = 15 * P_M + 0.5 * I_M + 3 * De_M

    duty_M = min(100, abs(U_M))  
    if P_M>0 and U_M>0:
        pwm_E1.ChangeDutyCycle(duty_M)
        pwm_E2.ChangeDutyCycle(0)
        print(f'm={temp_M:.2f}')
    elif P_M<0 and U_M<0:
        pwm_E2.ChangeDutyCycle(duty_M)
        pwm_E1.ChangeDutyCycle(0)
        print(f'm={temp_M:.2f}')
        print()

    
 
    reading_Z = analog_input_Z.value
    voltage_adc_Z = reading_Z * 3.3 
    R_Z = R0 * (6.6 - voltage_adc_Z) / (3.7467 + voltage_adc_Z)
    
    z = (1 / 3435) * math.log(R_Z / R1) + 1 / 298
    temp_Z = 1 / z - 273

    
    P_Z = 20.0 - temp_Z  
    I_Z += P_Z * Dt
    De_Z = (P_Z - preP_Z) / Dt
    preP_Z = P_Z
    U_Z = 15 * P_Z + 0.5 * I_Z + 3 * De_Z

    duty_Z = min(100, abs(U_Z))  
    if P_Z>0 and U_Z>0:
        pwm_C1.ChangeDutyCycle(duty_Z)
        pwm_C2.ChangeDutyCycle(0)
        print(f'z={temp_Z:.2f}')
    elif P_Z<0 and U_Z<0:
        pwm_C2.ChangeDutyCycle(duty_Z)
        pwm_C1.ChangeDutyCycle(0)
        print(f'z={temp_Z:.2f}')
        print()


    
    reading_L = analog_input_L.value
    voltage_adc_L = reading_L * 3.3 
    R_L = R0 * (6.6 - voltage_adc_L) / (3.7467 + voltage_adc_L)
    
    l = (1 / 3435) * math.log(R_L / R1) + 1 / 298
    temp_L = 1 / l - 273

   
    P_L = 20.0 - temp_L  
    I_L += P_L * Dt
    De_L = (P_L - preP_L) / Dt
    preP_L = P_L
    U_L = 15 * P_L + 0.5 * I_L + 3 * De_L

    duty_L = min(100, abs(U_L))  
    if P_L>0 and U_L>0:
        pwm_D1.ChangeDutyCycle(duty_L)
        pwm_D2.ChangeDutyCycle(0)
        print(f'l={temp_L:.2f}')
    elif P_L<0 and U_L<0:
        pwm_D2.ChangeDutyCycle(duty_L)
        pwm_D1.ChangeDutyCycle(0)
        print(f'l={temp_L:.2f}')
        print()


    if  temp_X <= 21.0 and temp_Y <= 21.0 and temp_Z <= 21.0 and temp_L <= 21.0 and temp_N >= 30.0 and temp_M >= 30.0:  
        break
 
    time.sleep(0.25)  

start_time = time.time()

try:

    with open('opamp.csv', 'w', newline='') as csvfile:
        fieldnames = ['Elapsed Time', 'Temperature_x', 'Temperature_y', 'Temperature_z', 'Temperature_l', 'Temperature_m', 'Temperature_n' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            elapsed_time = time.time() - start_time
            elapsed_time_str = f"{elapsed_time:.2f}\n"  
            client_socket.sendall(elapsed_time_str.encode('utf-8'))

            dt += 0.1
            

            # Thermistor ================================================
            reading_X = analog_input_X.value
            voltage_adc_X = reading_X * 3.3 
            R_X = R0 * (6.6 - voltage_adc_X) / (3.747 + voltage_adc_X)
           
            x = (1 / 3435) * math.log(R_X / R1) + 1 / 298
            temp_X = 1 / x - 273
            # ==============================================================

            
            target_temp_Y = get_target_temp_Y(elapsed_time)
            target_temp_X = get_target_temp_X(elapsed_time)
            target_temp_N = get_target_temp_N(elapsed_time)
            target_temp_M = get_target_temp_M(elapsed_time)

            P_X = target_temp_X - temp_X
            I_X += P_X * dt
            I_X = max(-integral_max, min(integral_max, I_X))  
            De_X = (P_X - preP_X) / dt
            preP_X = P_X
            U_X = Kp * P_X + Ki * I_X + Kd * De_X

            if abs(U_X) >= 100:
                duty_X = 100
            else:
                duty_X = abs(U_X)

            if P_X > 0 and U_X > 0:
                pwm_A1.ChangeDutyCycle(duty_X)  
                pwm_A2.ChangeDutyCycle(0)
            elif P_X < 0 and U_X < 0:
                pwm_A2.ChangeDutyCycle(duty_X) 
                pwm_A1.ChangeDutyCycle(0)
            # Thermistor ================================================
            reading_Y = analog_input_Y.value
            voltage_adc_Y = reading_Y * 3.3 
            R_Y = R0 * (6.6 - voltage_adc_Y) / (3.747 + voltage_adc_Y)
            
            y = (1 / 3435) * math.log(R_Y / R1) + 1 / 298
            temp_Y = 1 / y - 273
            # ==============================================================

            

            P_Y = target_temp_Y - temp_Y
            I_Y += P_Y * dt
            I_Y = max(-integral_max, min(integral_max, I_Y))  
            De_Y = (P_Y - preP_Y) / dt
            preP_Y = P_Y
            U_Y = kp * P_Y + ki * I_Y + kd * De_Y

            if abs(U_Y) >= 100:
                duty_Y = 100
            else:
                duty_Y = abs(U_Y)

            if P_Y > 0 and U_Y > 0:
                pwm_B1.ChangeDutyCycle(duty_Y) 
                pwm_B2.ChangeDutyCycle(0)
            elif P_Y < 0 and U_Y < 0:
                pwm_B2.ChangeDutyCycle(duty_Y)  
                pwm_B1.ChangeDutyCycle(0)
            
            # Thermistor ================================================
            reading_Z = analog_input_Z.value
            voltage_adc_Z = reading_Z * 3.3 
            R_Z = R0 * (6.6 - voltage_adc_Z) / (3.747 + voltage_adc_Z)
            
            z = (1 / 3435) * math.log(R_Z / R1) + 1 / 298
            temp_Z = 1 / z - 273
            # ==============================================================

            
            
            P_Z = target_temp_M - temp_Z
            I_Z += P_Z * dt
            I_Z = max(-integral_max, min(integral_max, I_Z))  
            De_Z = (P_Z - preP_Z) / dt
            preP_Z = P_Z
            U_Z = kp * P_Z + ki * I_Z + kd * De_Z

            if abs(U_Z) >= 100:
                duty_Z = 100
            else:
                duty_Z = abs(U_Z)

            if P_Z > 0 and U_Z > 0:
                pwm_C1.ChangeDutyCycle(duty_Z) 
                pwm_C2.ChangeDutyCycle(0)
            elif P_Z < 0 and U_Z < 0:
                pwm_C2.ChangeDutyCycle(duty_Z)  
                pwm_C1.ChangeDutyCycle(0)
            # Thermistor ================================================
            reading_L = analog_input_L.value
            voltage_adc_L = reading_L * 3.3 
            R_L = R0 * (6.6 - voltage_adc_L) / (3.747 + voltage_adc_L)
            
            l = (1 / 3435) * math.log(R_L / R1) + 1 / 298
            temp_L = 1 / l - 273
            # ==============================================================

            

            P_L = target_temp_N - temp_L
            I_L += P_L * dt
            I_L = max(-integral_max, min(integral_max, I_L))  
            De_L = (P_L - preP_L) / dt
            preP_L = P_L
            U_L = Kp * P_L + Ki * I_L + Kd * De_L

            if abs(U_L) >= 100:
                duty_L = 100
            else:
                duty_L = abs(U_L)

            if P_L > 0 and U_L > 0:
                pwm_D1.ChangeDutyCycle(duty_L)  
                pwm_D2.ChangeDutyCycle(0)
            elif P_L < 0 and U_L < 0:
                pwm_D2.ChangeDutyCycle(duty_L)  
                pwm_D1.ChangeDutyCycle(0)
                
            # Thermistor ================================================
            reading_M = analog_input_M.value
            voltage_adc_M = reading_M * 3.3 
            R_M = R0 * (6.6 - voltage_adc_M) / (3.747 + voltage_adc_M)
            
            m = (1 / 3435) * math.log(R_M / R1) + 1 / 298
            temp_M = 1 / m - 273
            # ==============================================================

            
            
            P_M = 41.0 - temp_M
            I_M += P_M * dt
            I_M = max(-integral_max, min(integral_max, I_M))  
            De_M = (P_M - preP_M) / dt
            preP_M = P_M
            U_M = Kp * P_M + Ki * I_M + Kd * De_M

            if abs(U_M) >= 100:
                duty_M = 100
            else:
                duty_M = abs(U_M)

            if P_M > 0 and U_M > 0:
                pwm_E1.ChangeDutyCycle(duty_M)  
                pwm_E2.ChangeDutyCycle(0)
            elif P_M < 0 and U_M < 0:
                pwm_E2.ChangeDutyCycle(duty_M)   
                pwm_E1.ChangeDutyCycle(0)
            # Thermistor ================================================
            reading_N = analog_input_N.value
            voltage_adc_N = reading_N * 3.3 
            R_N = R0 * (6.6 - voltage_adc_N) / (3.747 + voltage_adc_N)
            
            n = (1 / 3435) * math.log(R_N / R1) + 1 / 298
            temp_N = 1 / n - 273
            # ==============================================================

            

            P_N = 41.0 - temp_N
            I_N += P_N * dt
            I_N = max(-integral_max, min(integral_max, I_N))  
            De_N = (P_N - preP_N) / dt
            preP_N = P_N
            U_N = Kp * P_N + Ki * I_N + Kd * De_N

            if abs(U_N) >= 100:
                duty_N = 100
            else:
                duty_N = abs(U_N)

            if P_N > 0 and U_N > 0:
                pwm_F1.ChangeDutyCycle(duty_N)  
                pwm_F2.ChangeDutyCycle(0)
            elif P_N < 0 and U_N < 0:
                pwm_F2.ChangeDutyCycle(duty_N)  
                pwm_F1.ChangeDutyCycle(0)




           
            writer.writerow({'Elapsed Time': elapsed_time, 'Temperature_x': temp_X, 'Temperature_y': temp_Y, 'Temperature_z': temp_Z, 'Temperature_l': temp_L, 'Temperature_m': temp_M, 'Temperature_n': temp_N,})

            print(f'temp_X={temp_X:.2f}, temp_Y={temp_Y:.2f}, temp_Z={temp_Z:.2f}, temp_L={temp_L:.2f}, temp_M={temp_M:.2f}, temp_N={temp_N:.2f}, elapsed_time = {elapsed_time}')  

            time.sleep(0.1)
           
except KeyboardInterrupt:
    print("Server stopped.")
    
finally:
    client_socket.close()
    server_socket.close()








