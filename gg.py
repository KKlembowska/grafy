import igraph as ig
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd

# Funkcja propagacji
def propagacja(graf,df,wyswietlanie=1,zakazeni=[],procent_zakazonych=0.01,lp_kroków=20,p_zakazenia=0.5,czy_zdrowienie=0,p_zdrowienia=0.1,czy_izolacja=0,r_izolacji="",p_izolacji="",czas_izolacji=10):
    graph=graf.copy()
    n=graph.vcount()#liczba wezłów w grafie
    graph.vs["zakazony"] = np.zeros(n) # czy wezeł zakazony 
    graph.vs["izolacja"]=np.zeros(n) #długość trwania izolacji
    graph.vs["dlugosc"]=np.zeros(n)#czas trwania choroby
    
    krok=1
    chorzy=[] #zakazone wezły
    nowychory=[]
    
    if(czy_izolacja):
        do_izolacji=[]
        lp_izolacji=0
        stopien=graph.degree()
        bliskosc=graph.closeness()
        bliskosc = np.nan_to_num(bliskosc, nan=0.0)
        posrednictwo=graph.betweenness()
    if(len(zakazeni)!=0):#dodanie wezłów zakażonych wybranych wcześniej by były takie same w każdym wariancie
        for i in zakazeni:
            chorzy.append(i)
            graph.vs[i]["zakazony"] = 1
    else:
        for i in range (int(n*procent_zakazonych)): #wylosowanie osob zakazonych 
            rr=random.randint(0,n-1)
            while rr in chorzy:
                rr=random.randint(0,n-1)
            chorzy.append(rr)
            graph.vs[rr]["zakazony"] = 1
    indeksy=graph.neighborhood(chorzy[0],3)+[chorzy[0]] #indeksy dla wycinka 
    if(wyswietlanie):
        fig, ax = plt.subplots(figsize=(15,15)) 
    while krok<=lp_kroków :
        
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
                    f'dane dla fragmentu: liczba wezłów:{czesc.vcount()}, zakażone: {len(czesc.vs.select(zakazony=1))},zdrowe: {len(czesc.vs.select(zakazony=0))},izolacja: {len(czesc.vs.select(izolacja_gt=0))}\n'
                    f'dane dla całego grafu:liczba wezłów:{graph.vcount()},zakażone: {len(graph.vs.select(zakazony=1))},zdrowe: {n-len(graph.vs.select(zakazony=1))},izolacja:{ len(graph.vs.select(izolacja_gt=0))}'
                    )        
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='zdrowy'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='zakażony'),
                plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='grey', markersize=10, label='izolacja'),
            ]
            ax.legend(handles=legend_elements, loc='upper right')

            dane = f"Dane wejściowe:\n- Populacja: {graph.vcount()}\n- Liczba kroków: {lp_kroków}\n- Prawdopodobieństwo zakażenia: {p_zakazenia}\n- Czy zdrowienie: {czy_zdrowienie}\n- Prawdopodobieństwo zdrowienia: {p_zdrowienia}\n- Czy izolacja: {czy_izolacja}\n- Prawdopodobieństwo izolacji: {p_izolacji}\n- Czas izolacji: {czas_izolacji}"
            ax.text(0.01, 0.99,dane,transform=ax.transAxes,fontsize=8,verticalalignment='top',horizontalalignment='left')

            plt.pause(0.5)

        for i in chorzy:
            if(czy_zdrowienie): 
                rr=random.random()
                if(rr<p_zdrowienia):
                    chorzy.remove(i)# usuniecie z listy chorych
                    graph.vs[i]["zakazony"] = 0 #zmiana na zdrowego
                    continue
        
            if(czy_izolacja):
                # for j in do_izolacji:
                #     graph.vs[j]["izolacja"]=1
                #     lp_izolacji+=1
                # do_izolacji=[]
                if(graph.vs[i]["izolacja"]>0):
                    graph.vs[i]["izolacja"]=graph.vs[i]["izolacja"]+1
                    if(graph.vs[i]["izolacja"]>czas_izolacji):
                        graph.vs[i]["izolacja"]=0
                    else:
                        continue
        
                elif(r_izolacji=="losowa"):
                    rr=random.random()
                    if(rr<p_izolacji):
                        graph.vs[i]["izolacja"]=1
                        lp_izolacji+=1
                        continue
        
                elif(r_izolacji=="stopien"):
                    if stopien[i]>=np.percentile(stopien,75):#izolacja chorych o najwyzszych stopniach wierzcholka
                        graph.vs[i]["izolacja"] = 1
                        lp_izolacji+=1
                        continue
        
                elif(r_izolacji=="bliskosc"):
                    if bliskosc[i]>=np.percentile(bliskosc,75):
                        graph.vs[i]["izolacja"] = 1
                        lp_izolacji+=1
                        continue
        
                elif(r_izolacji=="posrednictwo"):
                    if posrednictwo[i]>=np.percentile(posrednictwo,75):
                        graph.vs[i]["izolacja"] = 1
                        lp_izolacji+=1
                        continue

            graph.vs[i]["dlugosc"]=graph.vs[i]["dlugosc"]+1
            s=graph.neighbors(i) #wyszukanie sąsiadów węzła zakazonego i
            for j in s:
                if(graph.vs[i]["izolacja"]>0):# jesli jest na izolacji pomin 
                    continue
                rr=random.random()    
                if(graph.vs[j]["izolacja"]>0):
                        continue
                if(j in chorzy):# jeśli już zakażony pomiń
                    continue
                if(rr<p_zakazenia):# jeśli rr mniejsze prawdopodobieństwo zakażenia zmień na zakażonego i dodaj do listy
                    graph.vs[j]["zakazony"] = 1 
                    graph.vs[i]["dlugosc"]=1 #pierwszy dzien choroby
                    nowychory.append(j)

        chorzy=list(set(chorzy+nowychory))
        nowychory=[]
        # df = pd.concat([df, pd.DataFrame([{"krok":krok,"c_zdrowienie":czy_zdrowienie,"c_izolacja":czy_izolacja,"p_zakazenia":p_zakazenia,"p_izolacji":p_izolacji, "Zakazeni": len(graph.vs.select(zakazony=1)), "Zdrowi":graph.vcount()-len(graph.vs.select(zakazony=1)),"izolacja":len(graph.vs.select(izolacja_gt=0))}])],ignore_index=True)
        if(krok==lp_kroków):#wpisywanie ostatniego kroku do dataframa
            df = pd.concat([df, pd.DataFrame([{"krok":krok,"c_zdrowienie":czy_zdrowienie,"c_izolacja":czy_izolacja,"p_zakazenia":p_zakazenia,"p_izolacji":p_izolacji,"Zakazeni":len(graph.vs.select(zakazony=1)),"Zdrowi":graph.vcount()-len(graph.vs.select(zakazony=1)),"izolacja":len(graph.vs.select(izolacja_gt=0)),"r_izolacji":r_izolacji,"czas_izolacji":czas_izolacji}])],ignore_index=True)
        krok+=1
    # plt.close()
    return df

#funkcja do tworzenia krawędzi
def create_edges(v, e):
    edges = []
    i = 0
    while i < e:
        v1 = random.randint(0, v - 1)
        v2 = random.randint(0, v - 1)
        if v1 == v2 or (v1, v2) in edges or (v2, v1) in edges:
            continue
        edges.append((v1, v2))
        i += 1
    return edges

v=5000      #liczba węzłów
# e=8000 #liczba krawędzi
# edges=create_edges(v,e)# graf losowy
#g = ig.Graph(v, edges)
# g = ig.Graph.Barabasi(v,3)
# g.write_gml("graf_5000_1.gml")
g=ig.Graph.Read_GML("graf_5000_2.gml")
procent_zakazonych=0.1
osoby_zarazone=[]
for i in range(int(v*procent_zakazonych)):
    rr=random.randint(0,v-1)
    while rr in osoby_zarazone:
        rr=random.randint(0,v-1)
    osoby_zarazone.append(rr)

p_zakazenia=[0.05,0.1,0.15,0.2,0.3,0.4]
p_izolacji=[0.1,0.2,0.3,0.4,0.5]
r_izolacji=["losowa","stopien","bliskosc","posrednictwo"]
czas_izolacji=[3,4,5,6,7]
grafy=["graf_5000_1.gml","graf_5000_2.gml","graf_5000_3.gml","graf_5000_4.gml","graf_5000_5.gml"]
df = pd.DataFrame(columns=["krok","c_zdrowienie","c_izolacja","p_zakazenia","p_izolacji","Zakazeni","Zdrowi","izolacja","r_izolacji","czas_izolacji"])
# for y in grafy:
print(osoby_zarazone)
for x in range(5):
    for i in p_zakazenia:
        df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i)
        df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_zdrowienie=1)
        for t in czas_izolacji:
            df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_izolacja=1 ,r_izolacji="stopien",czas_izolacji=t)
            df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_zdrowienie=1,czy_izolacja=1 ,r_izolacji="stopien",czas_izolacji=t)
            df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_izolacja=1,r_izolacji="bliskosc",czas_izolacji=t)
            df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_zdrowienie=1,czy_izolacja=1 ,r_izolacji="bliskosc",czas_izolacji=t)
            df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_izolacja=1,r_izolacji="posrednictwo",czas_izolacji=t)
            df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_zdrowienie=1,czy_izolacja=1,r_izolacji="posrednictwo",czas_izolacji=t)
            for j in p_izolacji:
                df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_izolacja=1,p_izolacji=j,r_izolacji="losowa",czas_izolacji=t)
                df=propagacja(g,df,wyswietlanie=0,zakazeni=osoby_zarazone,procent_zakazonych=procent_zakazonych,p_zakazenia=i,czy_zdrowienie=1,czy_izolacja=1,p_izolacji=j,r_izolacji="losowa",czas_izolacji=t)
        print(i)
    print(x)
    df.to_excel(f'graf_5000_2_{x}.xlsx', index=False)

print(df)
df.to_excel('graf_5000_2.xlsx', index=False)