from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from funcoes_analise import carregar_e_limpar_dados
import os
from dotenv import load_dotenv

load_dotenv()

# Prepara os dados
df = carregar_e_limpar_dados('dados/receita_2025.xlsx')

# Cria o Agente
llm = ChatOpenAI(model="gpt-4", temperature=0)
agente = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

print("--- Agente BBH Ativo ---")
pergunta = input("O que você quer saber sobre a empresa hoje? ")
agente.invoke(pergunta)
