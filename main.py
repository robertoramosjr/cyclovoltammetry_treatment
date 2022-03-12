import pandas as pd
import os.path
from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np


def is_not_valid_file(file_path):
    return False if file_path != "" and os.path.exists(file_path) else True


def is_bigger_data_frame(data_frame_1, data_frame_2):
    return len(data_frame_1) > len(data_frame_2)


def equalize_data_frame_rows(data_frame_1, data_frame_2):
    return data_frame_1.loc[0:len(data_frame_2)-1, :]


def ask_file_name():
    return input("Insira o nome do arquivo para salvar \n")


def ask_file_path(measurement_name):
    return input(f"Insira o caminho do arquivo de {measurement_name} \n")


def ask_potential_windows():
    return input('Qual a janela de potencial utilizada (em mV)? \n')


def ask_scan_rate():
    return input('Qual a velocidade de varredura da medida (em mV/s)? \n')


def ask_device_mass():
    return input('Qual a massa da amostra (em ng)? \n')


def ask_first_cycle_row():
    return input('Qual o número de linhas do primeiro scan? \n')


def ask_cycle_row_n():
    return input('Qual o número de linhas dos outros scan? \n')


def message_invalid_path():
    return print("Arquivo inválido ou inexistente \n")


def message_is_not_number():
    return print("O que foi inserido não é um número, por favor, insira um número. \n")


def make_input_as_number(number, function):
    while not number.isdigit():
        message_is_not_number()
        number = function()
    else:
        number = float(number)
    return number


def sanitize_data(data_frame):
    x = 0
    temp_data = pd.DataFrame()
    while x < len(data_frame):
        temp_data = pd.concat([temp_data, data_frame.iloc[x:x + N_OF_ROWS_AS_NUMBER, :].reset_index()], axis=1)
        x += N_OF_ROWS_AS_NUMBER + 1
    return temp_data


def integrate_data(data_to_integrate, x_axis):
    temp_list = []
    for k, v in enumerate(data_to_integrate):
        temp_list.append(integrate.trapezoid(data_to_integrate[k], x_axis[k]))
    return temp_list


# data_path = ask_file_path('ciclovoltametria')
# while is_not_valid_file(data_path):
#     message_invalid_path()
#     data_path = ask_file_path('ciclovoltametria')
#
# first_cycle_rows = ask_first_cycle_row()
# FIRST_CYCLE_ROWS_AS_NUMBER = int(make_input_as_number(first_cycle_rows, ask_first_cycle_row))
#
# n_of_rows = ask_cycle_row_n()
# N_OF_ROWS_AS_NUMBER = int(make_input_as_number(n_of_rows, ask_cycle_row_n))
#
# device_mass = ask_device_mass()
# DEVICE_MASS_AS_NUMBER = make_input_as_number(device_mass, ask_device_mass) * 10 ** (-9)
#
# scan_rate = ask_scan_rate()
# SCAN_RATE_AS_NUMBER = make_input_as_number(scan_rate, ask_scan_rate) * 10 ** (-3)
#
# potential_window = ask_potential_windows()
# POTENTIAL_WINDOW_AS_NUMBER = make_input_as_number(potential_window, ask_potential_windows) * 10 ** (-3)

         # DADOS DE ENTRADA QUE VOCÊ ME PASSOU, SE QUISER RODAR OS SEUS TESTES SEM PRECISAR FICAR DANDO INPUT
            # É SÓ COMENTAR AS LINHAS DE INPUT E DESCOMENTAR ESTAS

DEVICE_MASS_AS_NUMBER = 7.22 * 10 ** (-7)
SCAN_RATE_AS_NUMBER = 0.2
N_OF_ROWS_AS_NUMBER = 655
POTENTIAL_WINDOW_AS_NUMBER = 0.8
FIRST_CYCLE_ROWS_AS_NUMBER = 738
PROP_CONSTANT = 1 / (DEVICE_MASS_AS_NUMBER * SCAN_RATE_AS_NUMBER * POTENTIAL_WINDOW_AS_NUMBER)

data_file = pd.read_table('C:/Users/robee/Desktop/ciclos MXene 15wt.% PEDOT PSS - testes.txt', sep='\t', header=None)

# data_file = pd.read_table(data_path, sep='\t', header=None)

data_file_sliced = data_file.iloc[FIRST_CYCLE_ROWS_AS_NUMBER:, 1:]

data_sanitized = sanitize_data(data_file_sliced)
print(data_sanitized)

voltage_data = data_sanitized.iloc[:, 1::3].transpose().to_numpy()
current_data = data_sanitized.iloc[:, 2::3].transpose().to_numpy()
index_data = np.array(list(range(1, 2)))

integral_values = integrate_data(current_data, voltage_data)

capacitance = [element * PROP_CONSTANT for element in integral_values]

pd.DataFrame(capacitance).to_csv(ask_file_name(), sep='\t', decimal=',')

for key, value in enumerate(current_data):
    plt.plot(voltage_data[key][:], current_data[key][:], 'o')
plt.show()


"""
Por enquanto está configurado para plotar ixv pois comecei encontrar uns erros e não tive tempo de corrigir.
Quando eu conseguir mexer de novo, arrumarei este erro e farei com que o script plote para você capacitância x número
do ciclo.
Claro, isso se for interessante para você, se não for, me diga por favor!
"""
