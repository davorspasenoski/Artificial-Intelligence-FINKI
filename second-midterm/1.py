# Целта на оваа вежба е оптимизација на поставување безбедносни камери во музеј со користење на Генетски алгоритми.
# Музејот се состои од повеќе изложбени простории поврзани меѓусебно. Секоја просторија содржи артефакти и експонати со различни проценети вредности.
# Управата на музејот сака да постави ограничен број безбедносни камери со цел да ја максимизира вкупната заштитена вредност на музејот.

# Во почетниот код, променливата rooms е дадена со информации за имињата на просториите, листа од соседни простории и паричната вредност што ја претставува важноста на експонатите во просторијата.

# Во прикажаната слика, просториите означени со црвен текст се сметаат за големи простории, додека просториите означени со црн текст се сметаат за мали простории.

# Камера поставена во просторија ја зголемува безбедносната покриеност на таа просторија и делумно придонесува кон покриеноста на соседните простории.

# Мала просторија станува целосно покриена (100% покриеност) доколку во неа е поставена барем една камера. Дополнителни камери поставени во истата мала просторија не ја зголемуваат дополнително покриеноста и се бескорисни/нефункционални.

# Големите простории бараат дополнителен надзор. Една камера обезбедува 60% покриеност, додека 2 камери обезбедуваат 100% покриеност. Дополнителни камери по втората не ја зголемуваат понатаму покриеноста на просторијата и се нефункционални.

# Доколку просторијата содржи камери, тие делумно ја зголемуваат и покриеноста на соседните простории. Секоја камера поставена во просторија придонесува со +10% покриеност на секоја соседна просторија. Вредностите за покриеност никогаш не смеат да надминат 100%.

# Заштитената вредност на една просторија е пропорционална на процентот на нејзината покриеност. Вкупната заштитена вредност на музејот е еднаква на збирот од заштитените вредности на сите простории.

# На пример, просторија со вредност 200 и покриеност 100% придонесува со 200 заштитени единици, додека просторија со вредност 200 и покриеност 60% придонесува со 200 * 60% = 120 заштитени единици.

# Од стандарден влез се чита фиксен број K на безбедносни камери.

# Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете како да се распределат камерите низ музејот со цел да се максимизира вкупната заштитена вредност.

# Испечатете ја најдобрата проценета вкупна заштитена вредност.

# Забелешка: Локално, направете го следниот повик ga.best_solution(ga.last_generation_fitness) за да го добиете оптималното решение пронајдено во текот на сите генерации. Дополнително, можни се неконзистентности на типот (листа/numpy низа) на променливата chromosome/solution. 

# """- 1 camera in Prehistory
# - 1 camera in Medieval Times
# - 1 camera in Arts of Africa, Oceania and the Americas"""
# 3
# Optimal protected value: 471.0M$


import pygad
import random
random.seed(0)

rooms = {
    1: {'name': 'Modern & Contemporary Art', 'adjacent': [2, 7], 'value': 110},
    2: {'name': 'European History', 'adjacent': [1, 3, 4, 5, 7], 'value': 130},
    3: {'name': 'Seasonal Exhibitions', 'adjacent': [2], 'value': 100},
    4: {'name': 'Prehistory', 'adjacent': [2, 6, 10], 'value': 140},
    5: {'name': 'Medieval Times', 'adjacent': [2, 6, 9], 'value': 120},
    6: {'name': 'Arms and Armor', 'adjacent': [4, 5], 'value': 150},
    7: {'name': 'Arts of Africa, Oceania and the Americas', 'adjacent': [1, 2, 8], 'value': 90},
    8: {'name': 'Greek and Roman History', 'adjacent': [7, 9], 'value': 180},
    9: {'name': 'The Great Hall', 'adjacent': [5, 8, 10], 'value': 30},
    10: {'name': 'Egyptian History', 'adjacent': [4, 9], 'value': 200}
}

K = int(input())


def fitness_func(ga, solution, idx):
    chromosome = [int(gene) for gene in solution]
    score = 0
    security = [0,0,0,0,0,0,0,0,0,0]
    cameras_used = 0
    for i in range(len(chromosome)):
        room_id = i + 1
        cameras_used += chromosome[i]
        if room_id in (2,8,9,10):
            if chromosome[i] == 1:
                security[i] += 60
            elif chromosome[i] == 2:
                security[i] += 100

        else:
            if chromosome[i] == 1 or chromosome[i] == 2:
                security[i] += 100

        for sosed_room in rooms[room_id]["adjacent"]:
            security[sosed_room - 1] += 10 * chromosome[i]

    for i in range(len(security)):
        room_id= i + 1
        if security[i] > 100:
            security[i] = 100

        score += security[i] / 100 * rooms[room_id]["value"]

    if cameras_used > K:
        return score * (K / cameras_used)
    else:
        return score

params = {
    'num_generations': 1000,
    'sol_per_pop': 100,
    'num_parents_mating': 40,

    'num_genes': 10,
    'gene_space': [0,1,2],

    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
    'random_state': 0
}

ga = pygad.GA(**params)

ga.run()

best_solution, _, _ = ga.best_solution()
best_fitness = fitness_func(None, best_solution, 0)

print(f'Optimal protected value: {best_fitness}M$')
