from data.dbconnect import get_dataframe_from_query
import streamlit as st

@st.cache_data
def general_costs(day1, day2):
    return get_dataframe_from_query(f"""
SELECT
    DATE_FORMAT(CEC.Primeiro_Dia_Mes_Vencimento, '%m/%Y') AS 'Mês/Ano',
    SUM(CASE WHEN CEC.ID_Categoria = 100 THEN CEC.Valor END) AS 'C1 Impostos',
    SUM(CASE WHEN CEC.ID_Categoria = 104 THEN CEC.Valor END) AS 'C2 Custos de Ocupação',
    SUM(CASE WHEN CEC.ID_Categoria = 101 THEN CEC.Valor END) AS 'C3 Despesas com Pessoal Interno',
    SUM(CASE WHEN CEC.ID_Categoria = 105 THEN CEC.Valor END) AS 'C4 Despesas com Pessoal Terceirizado',
    SUM(CASE WHEN CEC.ID_Categoria = 102 THEN CEC.Valor END) AS 'C5 Despesas Operacionais com Shows',
    SUM(CASE WHEN CEC.ID_Categoria = 103 THEN CEC.Valor END) AS 'C6 Despesas com Clientes',
    SUM(CASE WHEN CEC.ID_Categoria = 108 THEN CEC.Valor END) AS 'C7 Despesas com Softwares e Licenças',
    SUM(CASE WHEN CEC.ID_Categoria = 107 THEN CEC.Valor END) AS 'C8 Despesas com Marketing',
    SUM(CASE WHEN CEC.ID_Categoria = 106 THEN CEC.Valor END) AS 'C9 Despesas Financeiras',
    SUM(CEC.Valor) AS 'Custos Totais'
FROM View_Custos_Eshows_Consolidados CEC
WHERE CEC.Primeiro_Dia_Mes_Vencimento >= '{day1}'
AND CEC.Primeiro_Dia_Mes_Vencimento <= '{day2}'
GROUP BY DATE_FORMAT(CEC.Primeiro_Dia_Mes_Vencimento, '%m/%Y')
ORDER BY STR_TO_DATE('Mês/Ano', '%m/%Y') DESC;
""", use_grupoe=True)

@st.cache_data
def cost_details(day1, day2):
    return get_dataframe_from_query(F"""
SELECT 
CEC.Categoria_de_Custo AS 'CATEGORIA DE CUSTO', 
CEC.Classificacao_Primaria AS 'CLASSIFICAÇÃO PRIMÁRIA', 
CEC.Valor AS 'VALOR', 
DATE_FORMAT(CEC.Primeiro_Dia_Mes_Vencimento, '%Y/%m') AS 'DATA'
FROM View_Custos_Eshows_Consolidados CEC
WHERE CEC.Primeiro_Dia_Mes_Vencimento >= '{day1}'
AND CEC.Primeiro_Dia_Mes_Vencimento <= '{day2}'
""", use_grupoe=True)

@st.cache_data
def ratings_rank(data):
    return get_dataframe_from_query(f"""
SELECT
DATE_FORMAT(CEC.Data_Vencimento, '%m/%Y') AS 'Mês/Ano',
CEC.Classificacao_Primaria AS 'CLASSIFICAÇÃO PRIMÁRIA', 
SUM(CEC.Valor) AS 'VALOR'

FROM View_Custos_Eshows_Consolidados CEC
WHERE CEC.Primeiro_Dia_Mes_Vencimento LIKE '{data}%'

GROUP BY CEC.Classificacao_Primaria, CEC.Primeiro_Dia_Mes_Vencimento
ORDER BY SUM(CEC.Valor) DESC
""", use_grupoe=True)

@st.cache_data
def ratings_rank_details(data):
    return get_dataframe_from_query(f"""
SELECT 
CEC.Classificacao_Primaria AS 'CLASSIFICAÇÃO PRIMÁRIA', 
CEC.Descricao_da_Despesa AS 'DESCRIÇÃO DA DESPESA',
CEC.Valor AS 'VALOR'
FROM View_Custos_Eshows_Consolidados CEC

JOIN 
(SELECT Classificacao_Primaria, SUM(Valor) AS Total_Valor
FROM View_Custos_Eshows_Consolidados CEC

WHERE CEC.Primeiro_Dia_Mes_Vencimento LIKE '{data}%'
GROUP BY CEC.Classificacao_Primaria) AS Total_Custos
ON 
CEC.Classificacao_Primaria = Total_Custos.Classificacao_Primaria

WHERE CEC.Primeiro_Dia_Mes_Vencimento LIKE '{data}%'

ORDER BY Total_Custos.Total_Valor DESC, CEC.Valor DESC;
""", use_grupoe=True)