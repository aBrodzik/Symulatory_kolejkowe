# ===================================
#         SYSTEM wrr BEGIN
# ===================================


class Pakiet:
    def __init__(self, time_a, czy_czekal):
        self.time_A = time_a
        self.czy_czekal = czy_czekal

    def __repr__(self):
        return "{0}".format(self.time_A)


class Zdarzenie:
    def __init__(self, id, time, zdarzenie):
        self.id = id
        self.time = time
        self.type = zdarzenie

    def __repr__(self):
        return "{1}: {0}".format(self.time, self.type)


def find_next(lista_zdarzen):
    min = lista_zdarzen[0].time
    min_id = 0
    for i in range(len(lista_zdarzen)):
        if lista_zdarzen[i].time < min:
            min = lista_zdarzen[i].time
            min_id = i

    return min_id


def wrr_check(WX, wx_counter):
    if wx_counter < WX:
        return True
    else:
        return False


W1 = 1
W2 = 2
arrival_rate_1 = 2
arrival_rate_2 = 3
service_rate = 10

if ((arrival_rate_1 > arrival_rate_2) and W1 < W2) or (arrival_rate_2 > arrival_rate_1 and W2 < W1): # inaczej zawsze przepelni sie kolejka
    t = arrival_rate_1
    arrival_rate_1 = arrival_rate_2
    arrival_rate_2 = t

arrival_interval_1 = 1 / arrival_rate_1
arrival_interval_2 = 1 / arrival_rate_2
service_interval = 1 / service_rate
max_packets = 1000000
i = 0
server_busy = False
kolejka1 = []
kolejka2 = []
kolejka_size = 1000
delay_counter = 0
nastepna_kolejka = 1
sys_time = 0
lista_zdarzen = []
w1_counter = 0
w2_counter = 0
total_delay = 0
qt=0
qt1=0
qt2=0
bt=0
ki_1 = 1
ki_2 = 2




if arrival_interval_1 <= arrival_interval_2:
    lista_zdarzen.append(Zdarzenie(0, arrival_interval_1, 1))
    lista_zdarzen.append(Zdarzenie(0, arrival_interval_2, 2))

else:
    lista_zdarzen.append(Zdarzenie(0, arrival_interval_2, 2))
    lista_zdarzen.append(Zdarzenie(0, arrival_interval_1, 1))

ki_1 = ki_1 + 1
ki_2 = ki_2 + 1

while max_packets > 0:
    i = i + 1

    number_in_queue = len(kolejka1) + len(kolejka2)
    temp_time = sys_time
    next_id = find_next(lista_zdarzen)
    sys_time = lista_zdarzen[next_id].time
    #print(temp_time, lista_zdarzen)
    print(max_packets)
    temp_time = sys_time - temp_time
    qt = qt + (number_in_queue * temp_time)
    qt1 = qt1 + (len(kolejka1)*temp_time)
    qt2 = qt2 + (len(kolejka2) * temp_time)

    if server_busy:
        bt = bt + (temp_time)


    if lista_zdarzen[next_id].type == 1:
        #lista_zdarzen.append(Zdarzenie(0, sys_time + arrival_interval_1, 1))
        lista_zdarzen.append(Zdarzenie(0, ki_1 * arrival_interval_1, 1))
        ki_1 = ki_1 + 1
        if server_busy:
            kolejka1.append(Pakiet(sys_time,True))
            if len(kolejka1) > kolejka_size:
                print("Error")
                break
        else:
            packet_in_server = Pakiet(lista_zdarzen[next_id].time, False)
            lista_zdarzen.append(Zdarzenie(0, sys_time + service_interval, 0))
            delay_counter = delay_counter + 1
            w1_counter = w1_counter + 1
            #print('a')
            max_packets = max_packets - 1
            server_busy = True
            if not wrr_check(W1, w1_counter):
                w1_counter = 0
                #print('k1 waga')
                nastepna_kolejka = 2

    elif lista_zdarzen[next_id].type == 2:
        #lista_zdarzen.append(Zdarzenie(0, lista_zdarzen[next_id].time + arrival_interval_2, 2))
        lista_zdarzen.append(Zdarzenie(0, ki_2 * arrival_interval_2, 2))
        ki_2 = ki_2 + 1
        czy_jest_D = False

        if server_busy:
            kolejka2.append(Pakiet(sys_time, True))
            if len(kolejka2) > kolejka_size:
                print("Error")
                break
        else:
            packet_in_server = Pakiet(lista_zdarzen[next_id].time, False)
            lista_zdarzen.append(Zdarzenie(0, lista_zdarzen[next_id].time + service_interval, 0))
            delay_counter = delay_counter + 1
            w2_counter = w2_counter + 1
            #print('b')
            max_packets = max_packets - 1
            server_busy = True
            if not wrr_check(W2, w2_counter):
                w2_counter = 0
                #print('k2 waga')
                nastepna_kolejka = 1

    if lista_zdarzen[next_id].type == 0:  # nastepna akcja to zakonczenie oblsugi pakietu
        lista_zdarzen.append(Zdarzenie(0, sys_time + service_interval, 0))
        if nastepna_kolejka == 1:
            if not kolejka1:
                w1_counter = 0
                #print('reset')
                nastepna_kolejka = 2
                if not kolejka2:
                    w2_counter = 0
                   #print('k2 pusta')
                    nastepna_kolejka = 1
                    server_busy = False
                    lista_zdarzen.pop()
            else:
                w1_counter = w1_counter + 1
                #print('a')
                packet_in_server = kolejka1[0]
                max_packets = max_packets - 1
                #lista_zdarzen.append(Zdarzenie(0, sys_time + service_interval, 0))
                kolejka1.pop(0)
                if not wrr_check(W1, w1_counter):
                    w1_counter = 0
                    #print('k1 waga')
                    nastepna_kolejka = 2
                if packet_in_server.czy_czekal:
                    delay = sys_time - packet_in_server.time_A
                    total_delay = total_delay + delay
                packet_in_server = packet_in_server
                delay_counter = delay_counter + 1

        elif nastepna_kolejka == 2:
            if not kolejka2:
                w2_counter = 0
                #print('k2 pusta')
                nastepna_kolejka = 1
                if not kolejka1:
                    w1_counter = 0
                    #print('k1 pusta')
                    nastepna_kolejka = 2
                    server_busy = False
                    lista_zdarzen.pop()
            else:
                w2_counter = w2_counter + 1
                #print('b')
                packet_in_server = kolejka2[0]
                max_packets = max_packets - 1
                #lista_zdarzen.append(Zdarzenie(0, sys_time + service_interval, 0))
                kolejka2.pop(0)
                if not wrr_check(W2, w2_counter):
                    w2_counter = 0
                    #print('k2 waga')
                    nastepna_kolejka = 1
                if packet_in_server.czy_czekal:
                    delay = sys_time - packet_in_server.time_A
                    total_delay = total_delay + delay
                packet_in_server = packet_in_server
                delay_counter = delay_counter + 1


    lista_zdarzen.pop(next_id)


#model arytmetyczny
#l = arrival_rate_1 + arrival_rate_2
#u = service_rate
#rho = l / u
#w = (rho / u) / (1 - rho)
#w = 1/(arrival_rate_1*W1) - 1/(arrival_rate_2*W2)

print(kolejka1)
print(kolejka2)
print("=" * 50)
print("Results:")
print("=" * 50)
print("Simulation time: ", sys_time)
print("ilość opóźnień: {1} ".format(max_packets, delay_counter))
print("-" * 50)
print("Calkowite opoznienie: ", total_delay)
dn = total_delay / delay_counter
print("Srednie opóxnienie:", dn)
#print(w)
print("-" * 50)
print("Qc(t): ", qt)
print("Q1(t): ", qt1)
print("Q2(t): ", qt2)
qn = qt / sys_time
print("qn: ", qn)
print("qn1: ", qt1/sys_time)
print("qn2: ", qt2/sys_time)
#qp = w * l
#print("przewidywane qn: ", qp, ' || ', abs(qp-qn)*100/qn,"%")
print("B(t): ", bt)
bn = bt / sys_time
#bp = (arrival_rate_1+arrival_rate_2)/service_rate
#print("przewidywane bn: ", bp, ' || ', abs(bp-bn)*100/bn,"%")
print("bn: ", bn)

print("-" * 50)
