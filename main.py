import os # Importamos para limpar a tela se quiser, mas é opcional

print("=== 🏃‍♂️ Diário de Corrida v3.0 (Leitura e Escrita) ===")
print("-" * 40)
print("HISTÓRICO DE TREINOS:")

# --- PARTE 1: LENDO O ARQUIVO ---
try:
    # 'r' significa READ (ler)
    with open("meus_treinos.txt", "r", encoding="utf-8") as arquivo:
        # readlines() pega cada linha do arquivo e coloca numa lista
        lista_de_treinos = arquivo.readlines()
        
        # Se a lista estiver vazia
        if not lista_de_treinos:
            print("Nenhum treino registrado ainda.")
        else:
            # Mostra linha por linha
            for treino in lista_de_treinos:
                # .strip() remove a quebra de linha extra para não ficar com espaços demais
                print(treino.strip())
                
except FileNotFoundError:
    print("Nenhum arquivo encontrado. Seu diário vai começar hoje!")

print("-" * 40)

# --- PARTE 2: ADICIONANDO NOVOS TREINOS (CÓDIGO ANTERIOR) ---
while True:
    print("\nAdicionar novo treino (ou digite '0' na distância para sair):")
    
    distancia = float(input("Distância (km): "))
    
    if distancia == 0:
        break
    
    print("Quanto tempo durou?")
    horas = int(input("Horas: "))
    minutos = int(input("Minutos: "))
    
    tempo_total_em_minutos = (horas * 60) + minutos
    
    if distancia > 0:
        pace = tempo_total_em_minutos / distancia
    else:
        pace = 0
    
    with open("meus_treinos.txt", "a", encoding="utf-8") as arquivo:
        linha = f"Distancia: {distancia}km | Tempo: {horas}h {minutos}min | Pace: {pace:.2f} min/km\n"
        arquivo.write(linha)
    
    print(f"✅ Salvo! Pace: {pace:.2f} min/km")

print("\nAté a próxima corrida!")