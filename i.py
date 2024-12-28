import pandas as pd
import matplotlib.pyplot as plt

def wykres1(df):
    df2=df[df["r_izolacji"]=="losowa"]
    df3=df[df["r_izolacji"]=="stopien"]
    df4=df[df["r_izolacji"]=="posrednictwo"]
    df5=df[df["r_izolacji"]=="bliskosc"]

    df = df.groupby(["krok","r_izolacji"]).mean(numeric_only=True).reset_index()
    df2=df2.groupby(["krok","r_izolacji","p_izolacji"]).mean(numeric_only=True).reset_index()
    df3 = df3.groupby(["krok","r_izolacji","prog"]).mean(numeric_only=True).reset_index()
    df4 = df4.groupby(["krok","r_izolacji","prog"]).mean(numeric_only=True).reset_index()
    df5 = df5.groupby(["krok","r_izolacji","prog"]).mean(numeric_only=True).reset_index()
    ri=df['r_izolacji'].unique()
    pi=df2["p_izolacji"].unique()
    pr=df3["prog"].unique()
    colors = [plt.cm.tab20(i / 20) for i in range(20)]
    color_index = 0
    for r in ri:
        if r=="losowa":
            for i in pi:
                d2=df2[df2["p_izolacji"]==i]
                plt.plot(d2["krok"], d2["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                color_index += 1
        elif r=="stopien":
            for i in pr:
                d3=df3[df3["prog"]==i]
                plt.plot(d3["krok"], d3["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                color_index += 1
        elif r=="posrednictwo":
            for i in pr:
                d4=df4[df4["prog"]==i]
                plt.plot(d4["krok"], d4["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                color_index += 1
        elif r=="bliskosc":
            for i in pr:
                d5=df5[df5["prog"]==i]
                plt.plot(d5["krok"], d5["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                color_index += 1
        else:
            d=df[df["r_izolacji"]==r]
            plt.plot(d["krok"], d["Zakazeni"], label=f'{r}',marker='o',markersize=3, color=colors[color_index % len(colors)])
            color_index += 1
    plt.xlabel("Krok")
    plt.ylabel("Liczba zakażonych")
    plt.title(f"liczba zakażonych dla różnych izolacji")
    # plt.xticks(ticks=df["krok"].unique())
    plt.legend(
        loc='center left',   
        bbox_to_anchor=(1, 0.5), 
        title="rodzaj izolacji", 
        frameon=True, 
        framealpha=1,  
        edgecolor='black'          
    )
    # plt.show()
    plt.savefig(rf"graf_wyniki_10\wykresy\bez.png",dpi=300, bbox_inches="tight")
    plt.clf()


def wykres1_2(df):
    df2=df[df["r_izolacji"]=="losowa"]
    df3=df[df["r_izolacji"]=="stopien"]
    df4=df[df["r_izolacji"]=="posrednictwo"]
    df5=df[df["r_izolacji"]=="bliskosc"]

    df = df.groupby(["krok","r_izolacji","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df2 = df2.groupby(["krok","r_izolacji","p_izolacji","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df3 = df3.groupby(["krok","r_izolacji","prog","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df4 = df4.groupby(["krok","r_izolacji","prog","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df5 = df5.groupby(["krok","r_izolacji","prog","p_zakazenia"]).mean(numeric_only=True).reset_index()
    ri=df['r_izolacji'].unique()
    pi=df2["p_izolacji"].unique()
    pr=df3["prog"].unique()
    pz=df["p_zakazenia"].unique()
    colors = [plt.cm.tab20(i / 20) for i in range(20)]
    color_index = 0
    for jj in pz:
        d1=df[df["p_zakazenia"]==jj]
        d2=df2[df2["p_zakazenia"]==jj]#losowa
        d3=df3[df3["p_zakazenia"]==jj]#stopien
        d4=df4[df4["p_zakazenia"]==jj]#posrednictwo
        d5=df5[df5["p_zakazenia"]==jj]#bliskosc
        
        for r in ri:
            if r=="losowa":
                for i in pi:
                    dd2=d2[d2["p_izolacji"]==i]
                    plt.plot(dd2["krok"], dd2["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                    color_index += 1
            elif r=="stopien":
                for i in pr:
                    dd3=d3[d3["prog"]==i]
                    plt.plot(dd3["krok"], dd3["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                    color_index += 1
            elif r=="posrednictwo":
                for i in pr:
                    dd4=d4[d4["prog"]==i]
                    plt.plot(dd4["krok"], dd4["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                    color_index += 1
            elif r=="bliskosc":
                for i in pr:
                    dd5=d5[d5["prog"]==i]
                    plt.plot(dd5["krok"], dd5["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                    color_index += 1
            else:
                d=d1[d1["r_izolacji"]==r]
                plt.plot(d["krok"], d["Zakazeni"], label=f'{r}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                color_index += 1
        plt.xlabel("Krok")
        plt.ylabel("Liczba zakażonych")
        plt.title(f"liczba zakażonych dla różnych izolacji \n prawdopodobieństwo zakażenia: {jj}")
        # plt.xticks(ticks=df["krok"].unique())
        plt.legend(
            loc='center left',   
            bbox_to_anchor=(1, 0.5), 
            title="rodzaj izolacji", 
            frameon=True, 
            framealpha=1,  
            edgecolor='black'          
        )
        # plt.show()
        plt.savefig(rf"graf_wyniki_10\wykresy\bez_{jj}.png",dpi=300, bbox_inches="tight")
        plt.clf()


def wykres1_3(df,p2="procent_zakazonych"):
    df2=df[df["r_izolacji"]=="losowa"]
    df3=df[df["r_izolacji"]=="stopien"]
    df4=df[df["r_izolacji"]=="posrednictwo"]
    df5=df[df["r_izolacji"]=="bliskosc"]

    df = df.groupby(["krok",p2,"r_izolacji","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df2=df2.groupby(["krok",p2,"r_izolacji","p_izolacji","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df3 = df3.groupby(["krok",p2,"r_izolacji","prog","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df4 = df4.groupby(["krok",p2,"r_izolacji","prog","p_zakazenia"]).mean(numeric_only=True).reset_index()
    df5 = df5.groupby(["krok",p2,"r_izolacji","prog","p_zakazenia"]).mean(numeric_only=True).reset_index()
    
    ri=df['r_izolacji'].unique()
    pi=df2["p_izolacji"].unique()
    pr=df3["prog"].unique()
    pz=df["p_zakazenia"].unique()
    ppz=df[p2].unique()
    colors = [plt.cm.tab20(i / 20) for i in range(20)]
    color_index = 0

    for j in ppz:
        dff1=df[df[p2]==j]
        dff2=df2[df2[p2]==j]
        dff3=df3[df3[p2]==j]
        dff4=df4[df4[p2]==j]
        dff5=df5[df5[p2]==j]
        for jj in pz:
            d1=dff1[dff1["p_zakazenia"]==jj]
            d2=dff2[dff2["p_zakazenia"]==jj]#losowa
            d3=dff3[dff3["p_zakazenia"]==jj]#stopien
            d4=dff4[dff4["p_zakazenia"]==jj]#posrednictwo
            d5=dff5[dff5["p_zakazenia"]==jj]#bliskosc
            for r in ri:
                if r=="losowa":
                    for i in pi:
                        dd2=d2[d2["p_izolacji"]==i]
                        plt.plot(dd2["krok"], dd2["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                        color_index += 1
                elif r=="stopien":
                    for i in pr:
                        dd3=d3[d3["prog"]==i]
                        plt.plot(dd3["krok"], dd3["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                        color_index += 1
                elif r=="posrednictwo":
                    for i in pr:
                        dd4=d4[d4["prog"]==i]
                        plt.plot(dd4["krok"], dd4["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                        color_index += 1
                elif r=="bliskosc":
                    for i in pr:
                        dd5=d5[d5["prog"]==i]
                        plt.plot(dd5["krok"], dd5["Zakazeni"], label=f'{r},{i}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                        color_index += 1
                else:
                    d=d1[d1["r_izolacji"]==r]
                    plt.plot(d["krok"], d["Zakazeni"], label=f'{r}',marker='o',markersize=3, color=colors[color_index % len(colors)])
                    color_index += 1
            plt.xlabel("Krok")
            plt.ylabel("Liczba zakażonych")
            plt.title(f"liczba zakażonych dla różnych izolacji \nprawdopodobieństwo zakażenia:{jj} ,{p2}:{j} ")
            # plt.xticks(ticks=df["krok"].unique())
            plt.legend(
                loc='center left',   
                bbox_to_anchor=(1, 0.5), 
                title="rodzaj izolacji", 
                frameon=True, 
                framealpha=1,  
                edgecolor='black'          
            )
            # plt.show()
            plt.savefig(rf"graf_wyniki_10\wykresy\bez_pzakazenia{jj}_{p2}{j}.png",dpi=300, bbox_inches="tight")
            plt.clf()



#zwraca tabele z srednimi wynikami dla dwoch parametrów p1-prawdopodobienstwo zakazenia i p2-rodzaj izolacji w okreslonym kroku
def tabela(df,krok=1,p1="p_zakazenia",p2="r_izolacji"):
    if(krok==1): #jeśli ostatni krok
        krok=df["krok"].max()
        df=df[df["krok"]==krok]
    else:
        df=df[df["krok"]==krok]

    df1 = df[~df["r_izolacji"].isin(["losowa", "stopien", "posrednictwo", "bliskosc"])]    
    df2=df[df["r_izolacji"]=="losowa"]
    for p in df["p_izolacji"].unique():
        df2.loc[(df2["r_izolacji"] == "losowa") & (df2["p_izolacji"] == p),"r_izolacji"]=f"losowa_{p}"
    df3=df[df["r_izolacji"]=="stopien"]
    df5=df[df["r_izolacji"]=="bliskosc"]
    df4=df[df["r_izolacji"]=="posrednictwo"]
    for s in df["prog"].unique():
        df3.loc[(df3["r_izolacji"] == "stopien") & (df3["prog"] == s),"r_izolacji"]=f"stopien_{s}"
        df4.loc[(df4["r_izolacji"] == "posrednictwo") & (df4["prog"] == s),"r_izolacji"]=f"posrednictwo_{s}"
        df5.loc[(df5["r_izolacji"] == "bliskosc") & (df5["prog"] == s),"r_izolacji"]=f"bliskosc_{s}"    

    df1 = df1.groupby([p2,p1]).mean(numeric_only=True).reset_index()
    df2 = df2.groupby([p2,p1]).mean(numeric_only=True).reset_index()
    df3 = df3.groupby([p2,p1]).mean(numeric_only=True).reset_index()
    df4 = df4.groupby([p2,p1]).mean(numeric_only=True).reset_index()
    df5 = df5.groupby([p2,p1]).mean(numeric_only=True).reset_index()
    d=pd.concat([df1,df2, df3,df4,df5], ignore_index=True)    

    result = d.pivot_table(index=p1,columns=p2,values="Zakazeni",aggfunc="mean")
    result["średnia"] = result.mean(axis=1).round(1)
    result.loc["średnia"] = result.mean(axis=0).round(1)
    print(result.round())
    return result.round()


df1=pd.read_excel("graf_wyniki_10\wyniki_zdrowienie1.xlsx")
df1=df1[df1["c_zdrowienie"]==1]
df2=pd.read_excel("graf_wyniki_10\wyniki_zdrowienie2.xlsx")
df2=df2[df2["c_zdrowienie"]==1]
df3=pd.read_excel("graf_wyniki_10\wyniki_zdrowienie3.xlsx")
df3=df3[df3["c_zdrowienie"]==1]
df=pd.concat([df1,df2, df3], ignore_index=True)
# df=pd.read_excel("graf_wyniki_10\wyniki_bez.xlsx")
# wykres1(df)
# wykres1_2(df)
# wykres1_3(df)
print("krok 10\n")
tabela(df,krok=10)
print("krok 20\n")
tabela(df,krok=20)
print("krok ostatni\n")
tabela(df)