def qualificar_qualidade_agua(estacao_id):
    parametros = dados_estacao.get(estacao_id, {})
    
    # Limites fictícios para qualificação
    limites = {
        "do": (5, 9),      # Oxigênio Dissolvido entre 5 e 9 mg/L é bom
        "turbidez": (0, 5),  # Turbidez entre 0 e 5 NTU é aceitável
        "temp": (0, 30),   # Temperatura entre 0 e 30 graus é normal
        "cond": (100, 500), # Condutividade entre 100 e 500 mS é aceitável
        "amm": (0, 0.5),   # Amônio entre 0 e 0.5 mg/L é bom
        "ph": (6, 8)       # pH entre 6 e 8 é bom
    }

    # Verificar se os parâmetros estão dentro dos limites
    for parametro, valor in parametros.items():
        if parametro in limites:
            min_limite, max_limite = limites[parametro]
            if not (min_limite <= valor <= max_limite):
                print(f"Qualidade da água na estação {estacao_id} é ruim para {parametro} ({valor})")
                return "Ruim"
    
    print(f"Qualidade da água na estação {estacao_id} é boa.")
    return "Boa"

# Exemplo de chamada
qualificar_qualidade_agua("BREPON")
