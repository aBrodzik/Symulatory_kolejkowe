import numpy as np

# ===================================
#         SYSTEM MM1
# ===================================


class Pakiet:
    def __init__(self, time_a, czy_czekal):
        self.time_A = time_a
        self.czy_czekal = czy_czekal

    def __repr__(self):
        return "Czas wejscia {0}, czy_czekal = {1}".format(self.time_A, self.czy_czekal)


class Zdarzenie:
    def __init__(self, time, zdarzenie):
        self.time = time
        self.type = zdarzenie

    def __repr__(self):
        return "Zdarzenie {1}: {0}".format(self.time, self.type)


def my_min(lista_zdarzen):
    min = lista_zdarzen[0].time
    min_id = 0
    for i in range(len(lista_zdarzen)):
        if lista_zdarzen[i].time < min:
            min = lista_zdarzen[i].time
            min_id = i

    return min_id


# Startowe parametry
simulation_time = 10000
arrival_rate = 9.5
service_rate = 10

#obliczenie przewidywanych parametrów
l = arrival_rate
u = service_rate
rho = l/u
w = (rho/u)/(1-rho)


# Inicjalizacja
arrival_times = []  # lista A
departure_times = []  # list D
lista_zdarzen = [] # lista nastepnego A i D
server_busy = False
sys_time = 0
delay_counter = 0
total_delay = 0
queue = []
queue_size = 1000
qt = 0
bt = 0
number_in_queue = 0
temp_time = 0
i=0
init = True
ai = 0 # licznik A
di = 0 # licznik D

max_packets = 1000000

# Generowanie czasów A
for i in range(max_packets):
    temp = np.random.exponential(1 / arrival_rate)  # lambda = 1/b
    arrival_times.append(float(temp))
#print("A: ", arrival_times)

# Generowanie czasów D
while not len(departure_times) == max_packets:
    temp = np.random.exponential(1 / service_rate)
    departure_times.append(float(temp))

#print("D: ", departure_times)

print("Start symulacji")
while True:

    if init: # dodanie pierwszych zdarzeń A i D
        print(ai)  # = 0
        lista_zdarzen.append(Zdarzenie(arrival_times[ai] + sys_time, 'A'))
        lista_zdarzen.append(Zdarzenie(departure_times[di] + arrival_times[ai], 'D'))
        di = di + 1
        ai = ai + 1
        init = False
        temp_time = sys_time

    if not lista_zdarzen:
        break
    else:
        number_in_queue = len(queue)
        next_id = my_min(lista_zdarzen)
        #print(lista_zdarzen)
        temp_time = sys_time
        sys_time = lista_zdarzen[next_id].time
        print(ai)
        temp_time = sys_time - temp_time
        qt = qt + (number_in_queue * temp_time)
        if server_busy:
            bt = bt + (temp_time)

        #Zdarzenie przybycia klienta
        if lista_zdarzen[next_id].type == 'A':

            #Zaplanuj kolejne zdarzenie przybycia
            if ai < len(arrival_times):
                lista_zdarzen.append(Zdarzenie(arrival_times[ai] + sys_time, 'A'))
                ai = ai + 1

                czy_A_ma_D = False #kiedy po stanie Idle przychodzi nowy pakiet to wygeneruj czas wyjścia
                for z in range(len(lista_zdarzen)):
                    if lista_zdarzen[z].type == 'D':
                        czy_A_ma_D = True
                if not czy_A_ma_D:
                    lista_zdarzen.append(Zdarzenie(departure_times[di-1] + sys_time, 'D'))

            if server_busy:
                queue.append(Pakiet(lista_zdarzen[next_id].time, True))
                if len(queue) > queue_size:
                    print("Error Queue FULL")
                    break
            else:
                server_busy = True
                packet_in_server = Pakiet(lista_zdarzen[next_id].time, False)
                delay_counter = delay_counter + 1

        if lista_zdarzen[next_id].type == 'D':

            if di < len(departure_times):  # nastepne zdarzenie to D
                di = di + 1
                if di < ai:
                    lista_zdarzen.append(Zdarzenie(departure_times[di-1] + sys_time, 'D'))

            # Zdarzenie zakończenia obsługi
                if not queue:
                    server_busy = False
                else:
                    next_packet = queue[0]
                    queue.pop(0)
                    # oblicz opóźnienie klienta przechodzącego do obłsugi
                    if next_packet.czy_czekal:
                        delay = sys_time - next_packet.time_A
                        total_delay = total_delay + delay
                    packet_in_server = next_packet
                    delay_counter = delay_counter + 1

        lista_zdarzen.pop(next_id)

    # print(my_min(lista_zdarzen))
    i = i + 1

print("="*50)
print("Results:")
print("="*50)
print("Simulation time: ", sys_time)
print("Max_packets: {0}, ai: {1}, di: {2}, ilość opóźnień: {3}".format(max_packets, ai, di, delay_counter))
print("-"*50)
print("Calkowite opoznienie: ", total_delay)
dn = total_delay/delay_counter
print("Srednie opóxnienie:", dn)
print("Przewidywane średnie opóźnienie:{0} || {1:.2f}%".format(w, abs((w-dn)*100/w)))
print("-"*50)
print("Q(t): ", qt)
print("przewidywane qn:", w*l)
print("qn: ", qt/sys_time)
print("B(t): ", bt)
bn = bt/sys_time
print("bn: ", bn)
print("Przewidywane obciążenie systemu:{0} || {1:.2f}%".format(rho, abs((rho-bn)*100/rho)))
print("-"*50)
