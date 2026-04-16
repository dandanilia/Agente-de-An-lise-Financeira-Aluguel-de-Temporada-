import pandas as pd

def carregar_e_limpar_dados(caminho):
    # 1. Carrega o Excel pulando as 2 linhas iniciais de título (como vimos na sua planilha)
    df = pd.read_excel(caminho, skiprows=2)
    
    # 2. Limpeza de nomes de colunas
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    # 3. Mapeamento de meses (garantindo que encontre as colunas)
    meses_alvo = ['jan', 'fev', 'março', 'abril', 'maio', 'jun', 'julho', 'ago', 'set', 'out', 'nov', 'dez']
    meses_existentes = [m for m in meses_alvo if m in df.columns]
    
    # 4. Converte valores para número (limpa "-" ou campos vazios)
    for col in meses_existentes:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # 5. Define seus apartamentos próprios
    proprios = ['garden', 'montblanc', 'varandas']
    
    # 6. Identifica a coluna com os nomes dos apartamentos (KITS)
    col_nome = 'kits' if 'kits' in df.columns else df.columns[0]

    # 7. CALCULO CORRIGIDO: 100% para os seus, 20% para terceiros
    def calcular_regra(linha):
        # Soma a receita da linha atual (apenas os meses)
        receita_da_linha = linha[meses_existentes].sum()
        
        # Verifica se o nome do kit está na sua lista de próprios
        nome_kit = str(linha[col_nome]).strip().lower()
        if nome_kit in proprios:
            return receita_da_linha # 100% seu
        else:
            return receita_da_linha * 0.20 # 20% comissão

    # Aplica a função linha por linha para criar a nova coluna
    df['lucro_efetivo_bbh'] = df.apply(calcular_regra, axis=1)
    
    # 8. Custo de Oportunidade (Exemplo: 1.2M e CDI 11%)
    valor_patrimonio = 1200000 
    df['meta_cdi_anual'] = valor_patrimonio * 0.11

    # Remove linhas que não são de kits (como totais ou linhas vazias no fim)
    df = df.dropna(subset=[col_nome])

    # ... código anterior (carregamento e cálculos) ...

    # 1. Remove linhas totalmente vazias
    df = df.dropna(subset=[col_nome])

    # 2. LISTA DE EXCLUSÃO: Vamos tirar tudo que não é apartamento real
    palavras_para_excluir = [
        'TOTAL', 'RECEITA', 'PRÓPRIA', 'TERCEIROS', 
        'SUBTOTAL', 'PROPRIA', 'COMISSÃO', 'TAXA'
    ]
    
    # Cria um filtro que remove qualquer linha que contenha essas palavras
    for palavra in palavras_para_excluir:
        df = df[~df[col_nome].str.contains(palavra, case=False, na=False)]

    # 3. Limpa espaços extras que sobraram nos nomes
    df[col_nome] = df[col_nome].str.strip()

    return df
