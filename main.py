import pandas as pd
import os.path
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt


def is_not_valid_file(file_path):
    return False if file_path != "" and os.path.exists(file_path) else True


def ask_file_name():
    return input("Insira o nome do arquivo para salvar \n")


def ask_file_path(measurement_name):
    return input(f"Insira o caminho do arquivo de {measurement_name} \n")


def ask_potential_window():
    return input('Qual a janela de potencial utilizada (em mV)? \n')


def ask_scan_rate():
    return input('Qual a velocidade de varredura da medida (em mV/s)? \n')


def ask_device_mass():
    return input('Qual a massa da amostra (em ug)? \n')


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
        temp_data = pd.concat([temp_data, data_frame.iloc[x:x + (N_OF_ROWS_AS_NUMBER + 1), :].reset_index()], axis=1)
        x += N_OF_ROWS_AS_NUMBER + 1
    return temp_data


def integrate_data(data_to_integrate, x_axis):
    temp_list = []
    for k, v in enumerate(data_to_integrate):
        temp_list.append(integrate.trapezoid(data_to_integrate[k], x_axis[k]))
    return temp_list


data_path = ask_file_path('ciclovoltametria')
while is_not_valid_file(data_path):
    message_invalid_path()
    data_path = ask_file_path('ciclovoltametria')

first_cycle_rows = ask_first_cycle_row()
FIRST_CYCLE_ROWS_AS_NUMBER = int(make_input_as_number(first_cycle_rows, ask_first_cycle_row))

n_of_rows = ask_cycle_row_n()
N_OF_ROWS_AS_NUMBER = int(make_input_as_number(n_of_rows, ask_cycle_row_n))

device_mass = ask_device_mass()
DEVICE_MASS_AS_NUMBER = make_input_as_number(device_mass, ask_device_mass) * 10 ** (-6)

scan_rate = ask_scan_rate()
SCAN_RATE_AS_NUMBER = make_input_as_number(scan_rate, ask_scan_rate) * 10 ** (-3)

potential_window = ask_potential_window()
POTENTIAL_WINDOW_AS_NUMBER = make_input_as_number(potential_window, ask_potential_window) * 10 ** (-3)

# ------------------ DADOS DE ENTRADA QUE VOCÊ ME PASSOU, SE QUISER RODAR OS SEUS TESTES SEM PRECISAR FICAR DANDO INPUT
# -------------------------------- É SÓ COMENTAR AS LINHAS DE INPUT E DESCOMENTAR ESTAS

#
# DEVICE_MASS_AS_NUMBER = 7.22 * 10 ** (-4)
# SCAN_RATE_AS_NUMBER = 0.2
# N_OF_ROWS_AS_NUMBER = 655
# POTENTIAL_WINDOW_AS_NUMBER = 0.8
# FIRST_CYCLE_ROWS_AS_NUMBER = 738
# data_file = pd.read_table('C:/Users/robee/Desktop/ciclos MXene 15wt.% PEDOT PSS.txt', sep='\t')

PROP_CONSTANT = 1 / (DEVICE_MASS_AS_NUMBER * SCAN_RATE_AS_NUMBER * POTENTIAL_WINDOW_AS_NUMBER)
CYCLE_NUMBER = 5000
data_file = pd.read_table(data_path, sep='\t')

data_file_sliced = data_file.iloc[(FIRST_CYCLE_ROWS_AS_NUMBER+1):, 1:]

data_sanitized = sanitize_data(data_file_sliced)

voltage_data = data_sanitized.iloc[:, 1::3].transpose().to_numpy()
current_data = data_sanitized.iloc[:, 2::3].transpose().to_numpy()
index_data = np.array(list(range(1, 2)))
cycle_list = list(range(1,  CYCLE_NUMBER))

integral_values = integrate_data(current_data, voltage_data)

capacitance = [element * PROP_CONSTANT for element in integral_values]

percentile_var = [element * 100 / capacitance[0] for element in capacitance]

pd.DataFrame([cycle_list, capacitance, percentile_var])\
    .transpose()\
    .to_csv(
    ask_file_name(),
    sep='\t',
    decimal=',',
    index=False,
    header=['ciclo', 'C F/g', '% do ciclo 1']
    )

plt.plot(cycle_list, capacitance, 'or')
plt.show()
