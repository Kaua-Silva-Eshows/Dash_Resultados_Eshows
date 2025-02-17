from data.dbconnect import get_dataframe_from_query
import streamlit as st

def general_costs_blueme(day1, day2):
    return get_dataframe_from_query(f"""
SELECT 
    DATE_FORMAT(DR.VENCIMENTO, '%m/%Y') AS 'Mês/Ano',
    
    SUM(CASE WHEN G1.DESCRICAO IN ('Impostos e Taxas') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C1 Impostos',
    SUM(CASE WHEN G1.DESCRICAO IN ('Eventos','Locação de Equipamentos Eventos','Locações','Manutenção','Ocupação','Utilidades', 'Insumos - A&B', 'Ocupação - Eventos') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C2 Custos de Ocupação',
    SUM(CASE WHEN G1.DESCRICAO IN ('Mão de obra','Transporte') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C3 Despesas com Pessoal Interno',
    SUM(CASE WHEN G1.DESCRICAO IN ('Serviço de Terceiros', 'Adiantamento a Fornecedores') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C4 Despesas com Pessoal Terceirizado',
    SUM(CASE WHEN G1.DESCRICAO IN ('Problemas Operacionais') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C5 Despesas Operacionais com Shows',
    SUM(CASE WHEN G1.DESCRICAO IN ('Visitas a Clientes') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C6 Despesas com Clientes',
    SUM(CASE WHEN G1.DESCRICAO IN ('Informática e TI') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C7 Despesas com Softwares e Licenças',
    SUM(CASE WHEN G1.DESCRICAO IN ('Artístico', 'Marketing', 'Patrocínio') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C8 Despesas com Marketing',
    SUM(CASE WHEN G1.DESCRICAO IN ('Despesas Financeiras', 'Receitas Financeiras', 'Receita Bruta', 'Deduções sobre Receita', 'Endividamento', 'Investimento - Capex') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C9 Despesas Financeiras'
    
FROM T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1
LEFT JOIN T_VERSOES_PLANO_CONTABIL VPC ON VPC.ID = G1.FK_VERSAO_PLANO_CONTABIL
LEFT JOIN T_DESPESA_RAPIDA DR ON DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = G1.ID
WHERE G1.FK_VERSAO_PLANO_CONTABIL = '102'
AND DR.VENCIMENTO >= '2025-01-01'
AND DR.VENCIMENTO >= '{day1}'
AND DR.VENCIMENTO <= '{day2}'
GROUP BY YEAR(DR.VENCIMENTO), MONTH(DR.VENCIMENTO)
ORDER BY STR_TO_DATE(DATE_FORMAT(DR.VENCIMENTO, '%m/%Y'), '%m/%Y');
""", use_blueme=True)

def costs_blueme_details(day1, day2):
    return get_dataframe_from_query(f"""
SELECT
    CASE 
        WHEN G1.DESCRICAO IN ('Impostos e Taxas') THEN 'c1_Impostos'
        WHEN G1.DESCRICAO IN ('Eventos','Locação de Equipamentos Eventos','Locações','Manutenção','Ocupação','Utilidades', 'Insumos - A&B', 'Ocupação - Eventos') THEN 'c2_Custos_de_Ocupacao'
        WHEN G1.DESCRICAO IN ('Mão de obra','Transporte') THEN 'c3_Despesas_com_Pessoal_Interno'
        WHEN G1.DESCRICAO IN ('Serviço de Terceiros', 'Adiantamento a Fornecedores') THEN 'c4_Despesas_com_Pessoal_Terceirizado'
        WHEN G1.DESCRICAO IN ('Problemas Operacionais') THEN 'c5_Problemas_Operacionais'
        WHEN G1.DESCRICAO IN ('Visitas a Clientes') THEN 'c6_Despesas_com_Clientes'
        WHEN G1.DESCRICAO IN ('Informática e TI') THEN 'c7_Despesas_com_Softwares_e_Licencas'
        WHEN G1.DESCRICAO IN ('Artístico', 'Marketing', 'Patrocínio') THEN 'c8_Despesas_com_Marketing'
        WHEN G1.DESCRICAO IN ('Despesas Financeiras', 'Receitas Financeiras', 'Receita Bruta', 'Deduções sobre Receita', 'Endividamento', 'Investimento - Capex') THEN 'c9_Despesas_Financeiras'
    END AS `CATEGORIA DE CUSTO`,
    G1.DESCRICAO AS 'CLASSIFICAÇÃO PRIMÁRIA',
    SUM(DR.VALOR_LIQUIDO) AS 'VALOR',
    DATE_FORMAT(DR.VENCIMENTO, '%Y/%m') AS 'DATA'
FROM T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1
LEFT JOIN T_VERSOES_PLANO_CONTABIL VPC ON VPC.ID = G1.FK_VERSAO_PLANO_CONTABIL
LEFT JOIN T_DESPESA_RAPIDA DR ON DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = G1.ID
WHERE G1.FK_VERSAO_PLANO_CONTABIL = '102'
AND DR.VENCIMENTO >= '2025-01-01'
AND DR.VENCIMENTO >= '{day1}'
AND DR.VENCIMENTO <= '{day2}'
GROUP BY YEAR(DR.VENCIMENTO), MONTH(DR.VENCIMENTO), `CATEGORIA DE CUSTO`
ORDER BY `CATEGORIA DE CUSTO`
""", use_blueme=True)

def ratings_rank_blueme(day):
    return get_dataframe_from_query(f"""
SELECT 
    DATE_FORMAT(DR.VENCIMENTO, '%m/%Y') AS 'Mês/Ano',
    G1.DESCRICAO AS 'CLASSIFICAÇÃO PRIMÁRIA',
    SUM(DR.VALOR_LIQUIDO) AS 'VALOR'
FROM T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1
LEFT JOIN T_VERSOES_PLANO_CONTABIL VPC ON VPC.ID = G1.FK_VERSAO_PLANO_CONTABIL
LEFT JOIN T_DESPESA_RAPIDA DR ON DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = G1.ID
WHERE G1.FK_VERSAO_PLANO_CONTABIL = '102'
AND DR.VENCIMENTO >= '2025-01-01'
AND DR.VENCIMENTO LIKE '{day}%'
GROUP BY G1.DESCRICAO, YEAR(DR.VENCIMENTO), MONTH(DR.VENCIMENTO)
""", use_blueme=True)

def ratings_rank_details_blueme(data):
   return get_dataframe_from_query(f"""
SELECT 
    G1.DESCRICAO AS 'CLASSIFICAÇÃO PRIMÁRIA',
    G2.DESCRICAO AS 'DESCRIÇÃO DA DESPESA',
    DR.VALOR_LIQUIDO AS 'VALOR'
FROM T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 G2 ON G2.FK_GRUPO_1 = G1.ID
LEFT JOIN T_DESPESA_RAPIDA DR ON DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_2 = G2.ID
LEFT JOIN (
    -- Subquery para calcular o total de valor por CLASSIFICAÇÃO PRIMÁRIA
    SELECT 
        G1.ID AS Grupo1_ID,
        SUM(DR.VALOR_LIQUIDO) AS Total_Valor
    FROM T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1
    LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 G2 ON G2.FK_GRUPO_1 = G1.ID
    LEFT JOIN T_DESPESA_RAPIDA DR ON DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_2 = G2.ID
    WHERE G1.FK_VERSAO_PLANO_CONTABIL = '102'
    AND DR.VENCIMENTO >= '2025-01-01'
    AND DR.VENCIMENTO LIKE '{data}%'
    GROUP BY G1.ID
) AS Total_Custos ON G1.ID = Total_Custos.Grupo1_ID
WHERE G1.FK_VERSAO_PLANO_CONTABIL = '102'
AND DR.VENCIMENTO >= '2025-01-01'
AND DR.VENCIMENTO LIKE '{data}%'
ORDER BY Total_Custos.Total_Valor DESC, DR.VALOR_LIQUIDO DESC;
""", use_blueme=True)