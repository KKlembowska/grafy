import igraph as ig
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd
import multiprocessing as mp
from tqdm import tqdm

# Funkcja propagacji
def propagacja(graf,df,wyswietlanie=1,zakazeni=[],procent_zakazonych=0.01,lp_kroków=20,p_zakazenia=0.5,czy_zdrowienie=0,p_zdrowienia=0.1,czy_izolacja=0,r_izolacji="",p_izolacji="",czas_izolacji=10,prog=75):
    graph=graf.copy()
    n=graph.vcount()#liczba wezłów w grafie
    graph.vs["zakazony"] = np.zeros(n) # czy wezeł zakazony 
    graph.vs["izolacja"]=np.zeros(n) #długość trwania izolacji
    graph.vs["dlugosc"]=np.zeros(n)#czas trwania choroby
    
    krok=1
    chorzy=[] #lista zakazonych wezłow
    nowychory=[]#lista nowych zakazonych wezlów w kroku biezacym
    if(czy_izolacja):
        lp_izolacji=0
        stopien=graph.degree()
        progi_stopien = np.percentile(stopien,prog)# 25 50 75
        bliskosc=graph.closeness()
        bliskosc = np.nan_to_num(bliskosc, nan=0.0)
        progi_bliskosc = np.percentile(bliskosc,prog)
        posrednictwo=graph.betweenness()
        progi_posrednictwo = np.percentile(posrednictwo, prog)
    if(len(zakazeni)!=0):#dodanie wezłów zakażonych wybranych wcześniej by były takie same w każdym wariancie
        for i in zakazeni:
            chorzy.append(i)
            graph.vs[i]["zakazony"] = 1
            graph.vs[i]["dlugosc"]=1
    else:
        for i in range (int(n*procent_zakazonych)): #wylosowanie osob zakazonych 
            rr=random.randint(0,n-1)
            while rr in chorzy:
                rr=random.randint(0,n-1)
            chorzy.append(rr)
            graph.vs[rr]["zakazony"] = 1
            graph.vs[rr]["dlugosc"]=1
    indeksy=graph.neighborhood(chorzy[0],3)+[chorzy[0]] #indeksy dla wycinka 
    if(wyswietlanie):
        fig, ax = plt.subplots(figsize=(15,15)) 
    while krok<=lp_kroków :
        # if(czy_zdrowienie==0 and len(chorzy)==graph.vcount()):#zakoncz szybciej jesli bez zdrowienia a wszyscy zachorowali
        #     df = pd.concat([df, pd.DataFrame([{"krok":krok,"procent_zakazonych":procent_zakazonych,"c_zdrowienie":czy_zdrowienie,"c_izolacja":czy_izolacja,"p_zakazenia":p_zakazenia,"p_izolacji":p_izolacji,"Zakazeni":len(graph.vs.select(zakazony=1)),"Zdrowi":graph.vcount()-len(graph.vs.select(zakazony=1)),"izolacja":len(graph.vs.select(izolacja_gt=0)),"r_izolacji":r_izolacji,"czas_izolacji":czas_izolacji,"prog":prog,"p_zdrowienia":p_zdrowienia}])],ignore_index=True)
        #     df = pd.concat([df, pd.DataFrame([{"krok":lp_kroków,"procent_zakazonych":procent_zakazonych,"c_zdrowienie":czy_zdrowienie,"c_izolacja":czy_izolacja,"p_zakazenia":p_zakazenia,"p_izolacji":p_izolacji,"Zakazeni":len(graph.vs.select(zakazony=1)),"Zdrowi":graph.vcount()-len(graph.vs.select(zakazony=1)),"izolacja":len(graph.vs.select(izolacja_gt=0)),"r_izolacji":r_izolacji,"czas_izolacji":czas_izolacji,"prog":prog,"p_zdrowienia":p_zdrowienia}])],ignore_index=True)
        #     break
        df = pd.concat([df, pd.DataFrame([{"krok":krok,"procent_zakazonych":procent_zakazonych,"c_zdrowienie":czy_zdrowienie,"c_izolacja":czy_izolacja,"p_zakazenia":p_zakazenia,"p_izolacji":p_izolacji, "Zakazeni": len(graph.vs.select(zakazony=1)), "Zdrowi":graph.vcount()-len(graph.vs.select(zakazony=1)),"izolacja":len(graph.vs.select(izolacja_gt=0)),"r_izolacji":r_izolacji,"czas_izolacji":czas_izolacji,"prog":prog,"p_zdrowienia":p_zdrowienia}])],ignore_index=True)
        if(wyswietlanie):# wyswietlenie kroku na grafie
            ax.clear()  
            czesc=graph.subgraph(indeksy)
            ig.plot(
                czesc,
                vertex_color = ["green" if z == 0 else "red" for z in czesc.vs["zakazony"]],
                vertex_shape=["circle" if i == 0 else "triangle-up" for i in czesc.vs["izolacja"]],
                vertex_size=20,
                edge_width=1,
                target=ax,        
                layout="kk",
            )
            plt.title(f'Krok: {krok}\n'
                    f'dane dla fragmentu:zakażone: {len(czesc.vs.select(zakazony=1))},zdrowe: {len(czesc.vs.select(zakazony=0))},izolacja: {len(czesc.vs.select(izolacja_gt=0))}\n'
                    f'dane dla całego grafu:zakażone: {len(graph.vs.select(zakazony=1))},zdrowe: {n-len(graph.vs.select(zakazony=1))},izolacja:{ len(graph.vs.select(izolacja_gt=0))}'
                    )        
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='zdrowy'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='zakażony'),
                plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='grey', markersize=10, label='izolacja'),
            ]
            ax.legend(handles=legend_elements, loc='upper right')

            dane = f"Dane wejściowe:\n- Populacja: {graph.vcount()}\n- Liczba kroków: {lp_kroków}\n- Prawdopodobieństwo zakażenia: {p_zakazenia}\n- Czy zdrowienie: {czy_zdrowienie}\n- Czy izolacja: {czy_izolacja}\n- Rodzaj izolacji: {r_izolacji}\n- Prawdopodobieństwo izolacji: {p_izolacji}\n- Czas izolacji: {czas_izolacji}"
            ax.text(0.01, 0.99,dane,transform=ax.transAxes,fontsize=8,verticalalignment='top',horizontalalignment='left')

            plt.pause(0.5)

        for i in chorzy:
            if(czy_zdrowienie): 
                rr=random.random()
                # if(random.random()<graph.vs[i]["dlugosc"]/100):
                if(random.random()<p_zdrowienia):
                    chorzy.remove(i)# usuniecie z listy chorych
                    graph.vs[i]["zakazony"] = 0 # zmiana na zdrowego
                    graph.vs[i]["dlugosc"]=0
                    continue
        
            if(czy_izolacja):
                if(graph.vs[i]["izolacja"]>0):
                    graph.vs[i]["izolacja"]+=1
                    if(graph.vs[i]["izolacja"]>czas_izolacji):
                        graph.vs[i]["izolacja"]=0
                    else:
                        continue
                        
                elif(r_izolacji=="losowa"):#izolowanie losowych wezłów chorych
                    rr=random.random()
                    if(rr<p_izolacji):
                        graph.vs[i]["izolacja"]=1
                        lp_izolacji+=1
                        continue
                        
                elif(r_izolacji=="stopien" and stopien[i]>=progi_stopien):#izolacja chorych o najwyzszych stopniach wierzcholkow(najwiekszej liczbie sasiadow)
                    graph.vs[i]["izolacja"] = 1
                    lp_izolacji+=1
                    continue

                elif(r_izolacji=="bliskosc" and bliskosc[i]>=progi_bliskosc):#izolacja chorych o najwyzszej centralnosci bliskosc 
                    graph.vs[i]["izolacja"] = 1
                    lp_izolacji+=1
                    continue
        
                elif(r_izolacji=="posrednictwo" and posrednictwo[i]>=progi_posrednictwo):#izolacja chorych o najwyzszyej centralnosci posrednictwa
                    graph.vs[i]["izolacja"] = 1
                    lp_izolacji+=1
                    continue

                elif(r_izolacji=="czas"):#izoluj jesli jest chory dluzej niz x dni
                    if(graph.vs[i]["dlugosc"]>5):
                        graph.vs[i]["izolacja"] = 1
                        lp_izolacji+=1
                        continue
                
                elif(r_izolacji=="kaskadowa"):
                    procent_z=len(chorzy)/graph.vcount()
                    if procent_z <= 0.3 :
                        if stopien[i]>=progi_stopien:
                            graph.vs[i]["izolacja"] = 1
                            lp_izolacji+=1
                            continue
                    elif procent_z>0.3  and procent_z<=0.6 :
                        graph.vs[i]["izolacja"] = 1
                        lp_izolacji+=1
                        for ii in graph.neighbors(i):
                            if graph.vs[ii]["zakazony"]==0 and graph.vs[ii]["izolacja"]==0:
                                graph.vs[ii]["izolacja"] = 1
                                lp_izolacji+=1
                        continue
                    elif procent_z>0.6:
                        graph.vs[i]["izolacja"] = 1
                        lp_izolacji+=1
                        for ii in graph.neighborhood(i,2):
                            if graph.vs[ii]["zakazony"]==0 and graph.vs[ii]["izolacja"]==0:
                                graph.vs[ii]["izolacja"] = 1
                                lp_izolacji+=1
                        continue
                    
            graph.vs[i]["dlugosc"]+=1
            s=graph.neighbors(i) #wyszukanie sąsiadów węzła zakazonego i
            for j in s:
                if(graph.vs[i]["izolacja"]>0):# jesli jest na izolacji pomin 
                    continue
                if(graph.vs[j]["izolacja"]>0):# Jeśli sąsiad jest na izolacji, pomiń
                        continue
                if(j in chorzy):# jeśli sasiad już zakażony pomiń
                    continue
                #proba zakazenia
                if(graph.vs[j]["zakazony"]==0 and random.random()<p_zakazenia):# jeśli rr mniejsze prawdopodobieństwo zakażenia zmień na zakażonego i dodaj do listy
                    graph.vs[j]["zakazony"]=1 
                    graph.vs[j]["dlugosc"]=1 #pierwszy dzien choroby
                    nowychory.append(j)
        chorzy=list(set(chorzy+nowychory))
        nowychory=[]
        # if(krok==lp_kroków):#wpisywanie ostatniego kroku do dataframa
        #     df = pd.concat([df, pd.DataFrame([{"krok":krok,"procent_zakazonych":procent_zakazonych,"c_zdrowienie":czy_zdrowienie,"c_izolacja":czy_izolacja,"p_zakazenia":p_zakazenia,"p_izolacji":p_izolacji, "Zakazeni": len(graph.vs.select(zakazony=1)), "Zdrowi":graph.vcount()-len(graph.vs.select(zakazony=1)),"izolacja":len(graph.vs.select(izolacja_gt=0)),"r_izolacji":r_izolacji,"czas_izolacji":czas_izolacji}])],ignore_index=True)
        krok+=1

    return df

# g = ig.Graph.Barabasi(5000,5)
# g.write_gml("graf_5000_5krawedzie.gml")
# g = ig.Graph.Read_GML("graf_5000_4krawedzie.gml")
# df = pd.DataFrame(columns=["krok", "procent_zakazonych", "c_zdrowienie", "c_izolacja", "p_zakazenia", "p_izolacji", "Zakazeni", "Zdrowi", "izolacja", "r_izolacji", "czas_izolacji","prog","p_zdrowienia"])
# df=propagacja(g,df,wyswietlanie=1,procent_zakazonych=0.1,p_zakazenia=0.4,czy_izolacja=1,czy_zdrowienie=0,r_izolacji="stopien",czas_izolacji=5)
# plt.show()
def run_propagation_parallel(args):
    graf, procent_zakazonych, r_izolacji, p_zakazenia,czy_izolacja, czas_izolacji, osoby_zarazone, czy_zdrowienie, p_izolacji,prog,p_zdrowienia = args
    df = pd.DataFrame(columns=["krok", "procent_zakazonych", "c_zdrowienie", "c_izolacja", "p_zakazenia", "p_izolacji", "Zakazeni", "Zdrowi", "izolacja", "r_izolacji", "czas_izolacji","prog","p_zdrowienia"])
    df = propagacja(
        graf.copy(), 
        df,
        lp_kroków=100,
        wyswietlanie=0,
        zakazeni=osoby_zarazone,
        procent_zakazonych=procent_zakazonych,
        p_zakazenia=p_zakazenia,
        czy_izolacja=czy_izolacja,
        r_izolacji=r_izolacji,
        p_izolacji=p_izolacji,
        czas_izolacji=czas_izolacji,
        czy_zdrowienie=czy_zdrowienie,
        prog=prog,
        p_zdrowienia=p_zdrowienia
    )
    return df

def prepare_and_run_multiprocessing():
    v = 5000
    graf = ig.Graph.Read_GML("grafy\graf_5000_3krawedzie.gml")
    procent = [0.1,0.2,0.4,0.5,0.7]
    r_izolacji = ["stopien","bliskosc","posrednictwo","losowa","czas","kaskadowa"]#"stopien","bliskosc","posrednictwo","losowa","czas","kaskadowa"
    p_zakazenia =[0.1,0.2,0.3,0.4,0.5]
    p_izolacji = [0.25,0.50,0.75]
    czas_izolacji = [4,6,8,10]
    p_zdrowienia=[0.1,0.2,0.3]
    progi=[75,50,25]
    df_results = pd.DataFrame(columns=["krok", "procent_zakazonych", "c_zdrowienie", "c_izolacja", "p_zakazenia", "p_izolacji", "Zakazeni", "Zdrowi", "izolacja", "r_izolacji", "czas_izolacji","prog","p_zdrowienia"])
    wykonania=0
    tasks = []
    for procent_zakazonych in procent:
        osoby_zarazone = random.sample(range(v), int(v * procent_zakazonych))
        for _ in range(5):                                                                                                                                                                                                                                                                             
            for i in p_zakazenia:
                tasks.append((graf, procent_zakazonych, "bez_izolacji", i,0,0, osoby_zarazone, 0, 0,0,0))
                wykonania+=1
                for izolacja in r_izolacji:
                    for t in czas_izolacji:
                        if(izolacja=="losowa"):
                            for p in p_izolacji:
                                tasks.append((graf, procent_zakazonych, izolacja,i,1, t, osoby_zarazone, 0, p,0,0))
                                wykonania+=1
                        elif(izolacja=="czas"):
                            tasks.append((graf, procent_zakazonych, izolacja, i,1, t, osoby_zarazone, 0,0,0,0))
                            wykonania+=1
                        else:
                            for prog in progi:
                                tasks.append((graf, procent_zakazonych, izolacja, i,1, t, osoby_zarazone, 0,0,prog,0))
                                wykonania+=1
            
            # for p_z in p_zdrowienia:
            #     for i in p_zakazenia:
            #         tasks.append((graf, procent_zakazonych, "bez_izolacji", i,0,0, osoby_zarazone, 1, 0,0,p_z))
            #         wykonania+=1
            #         for izolacja in r_izolacji:
            #             for t in czas_izolacji:
            #                 if(izolacja=="losowa"):
            #                     for p in p_izolacji:
            #                         tasks.append((graf, procent_zakazonych, izolacja,i,1, t, osoby_zarazone, 1, p,0,p_z))
            #                         wykonania+=1
            #                 elif(izolacja=="czas"):
            #                     tasks.append((graf, procent_zakazonych, izolacja, i,1, t, osoby_zarazone, 1,0,0,p_z))
            #                     wykonania+=1
            #                 else:
            #                     for prog in progi:
            #                         tasks.append((graf, procent_zakazonych, izolacja, i,1, t, osoby_zarazone, 1,0,prog,p_z))
            #                         wykonania+=1
    print("liczba petli",wykonania)

    with mp.Pool(mp.cpu_count()) as pool:
        results = list(tqdm(pool.imap(run_propagation_parallel, tasks), total=len(tasks)))
    
    for result in results:
        df_results = pd.concat([df_results, result], ignore_index=True)
    df_results.to_excel("graf_wyniki_3\wyniki_bez.xlsx", index=False)
    
    # rows = len(df_results)
    # size = rows // 3

    # df_results.iloc[:size].to_excel("graf_wyniki_10\wyniki_zdrowienie1.xlsx", index=False)
    # df_results.iloc[size:size * 2].to_excel("graf_wyniki_10\wyniki_zdrowienie2.xlsx", index=False)
    # df_results.iloc[size * 2:].to_excel("graf_wyniki_10\wyniki_zdrowienie3.xlsx", index=False)
    print("koniec!!")

if __name__ == "__main__":
    prepare_and_run_multiprocessing()