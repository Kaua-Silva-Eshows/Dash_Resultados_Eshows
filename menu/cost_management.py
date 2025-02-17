import streamlit as st
from data.querys_blueme import *
from data.querys_eshows import *
from data.querys_grupoe import *
from menu.page import Page
from utils.components import *
from utils.functions import *
from datetime import date, datetime

def BuildCostManagement(generalRevenue, generalCosts, costDetails, ratingsRank, ratingsRankDetails, generalCostsBlueme, costsBluemeDetails, ratingsRankBlueme, ratingsRankDetailsBlueme):

    row1 = st.columns(6)
    global day_CostManagement1, day_CostManagement2


    with row1[2]:
        day_CostManagement1 = st.date_input('Data Inicio:', value=date(datetime.today().year - 1, 1, 1), format='DD/MM/YYYY', key='day_CostManagement1') 
    with row1[3]:
        day_CostManagement2 = st.date_input('Data Final:', value=date(datetime.today().year, 12, 31), format='DD/MM/YYYY', key='day_CostManagement2')

    generalRevenue = general_revenue(day_CostManagement1, day_CostManagement2, filters='')
    generalCosts = general_costs(day_CostManagement1, day_CostManagement2)
    generalCostsBlueme = general_costs_blueme(day_CostManagement1, day_CostManagement2)

    merged_df = pd.merge(generalCosts, generalRevenue[['Mês/Ano', 'Faturamento Total']], on='Mês/Ano', how='left')

    merged_df = function_merged_and_add_df(merged_df, generalCostsBlueme, column='Mês/Ano')
    merged_df = function_grand_total_line(merged_df)
    merged_df = function_formated_cost(generalCosts, merged_df)

    filtered_copy, count = component_plotDataframe(merged_df, "Custos Gerais")
    function_copy_dataframe_as_tsv(filtered_copy)

    costDetails = cost_details(day_CostManagement1, day_CostManagement2)
    costsBluemeDetails = costs_blueme_details(day_CostManagement1, day_CostManagement2)

    pivot_costDetails = function_marged_pivot_costDetails(costDetails, costsBluemeDetails)

    filtered_copy, count= component_plotDataframe(pivot_costDetails, "Custos Especificos")
    function_copy_dataframe_as_tsv(filtered_copy)


    row2 = st.columns(6)
    global data_ratingsRank

    with row2[1]:
        data_ratingsRank = st.date_input('Escolha Mês e Ano:', value=date(datetime.today().year - 1, 1, 1), format='DD/MM/YYYY', key='data_ratingsRank1')
        data_ratingsRank = data_ratingsRank.strftime('%Y-%m')


    with row2[4]:
        data_ratingsRank2 = st.date_input('Escolha Mês e Ano:', value=date(datetime.today().year, 1, 1), format='DD/MM/YYYY', key='data_ratingsRank2')
        data_ratingsRank2 = data_ratingsRank2.strftime('%Y-%m')

    if data_ratingsRank == data_ratingsRank2:
        st.warning("🚨 As datas não podem ser iguais! Selecione meses diferentes.")

    else:
        row3 = st.columns(2)
        if data_ratingsRank:
            with row3[0]:
                ratingsRank = ratings_rank(data_ratingsRank)
                ratingsRankBlueme = ratings_rank_blueme(data_ratingsRank)
                merged_df1 = pd.merge(ratingsRank,ratingsRankBlueme,on=["Mês/Ano", "ID CUSTO", "CLASSIFICAÇÃO PRIMÁRIA", "VALOR"], how="outer", suffixes=('_ratingsRank', '_ratingsRankBlueme'))
                merged_df1 = merged_df1.sort_values(by="VALOR", ascending=False).drop(columns=["Mês/Ano"])
                merged_df1["VALOR"] = merged_df1["VALOR"].apply(float)
                plotPizzaChart(merged_df1["CLASSIFICAÇÃO PRIMÁRIA"], merged_df1["VALOR"], None)
                merged_df1 = function_format_numeric_columns(merged_df1)
                filtered_copy, count= component_plotDataframe(merged_df1, f"Custos {data_ratingsRank}")
                function_copy_dataframe_as_tsv(filtered_copy)
                
        if data_ratingsRank2:
            with row3[1]:
                ratingsRank2 = ratings_rank(data_ratingsRank2)
                ratingsRankBlueme2 = ratings_rank_blueme(data_ratingsRank2)
                merged_df2 = pd.merge(ratingsRank2,ratingsRankBlueme2,on=["Mês/Ano", "ID CUSTO", "CLASSIFICAÇÃO PRIMÁRIA", "VALOR"], how="outer", suffixes=('_ratingsRank', '_ratingsRankBlueme'))
                merged_df2 = merged_df2.sort_values(by="VALOR", ascending=False).drop(columns=["Mês/Ano"])
                merged_df2["VALOR"] = merged_df2["VALOR"].apply(float)
                plotPizzaChart(merged_df2["CLASSIFICAÇÃO PRIMÁRIA"], merged_df2["VALOR"], None)
                merged_df2 = function_format_numeric_columns(merged_df2)
                filtered_copy, count= component_plotDataframe(merged_df2, f"Custos {data_ratingsRank2}")
                function_copy_dataframe_as_tsv(filtered_copy)

        row4 = st.columns([0.5,1,1,0.5])
        row5 = st.columns(2)

        with row4[1]:
            
            with row5[0]:
                ratingsRankDetails = ratings_rank_details(data_ratingsRank)
                ratingsRankDetailsBlueme = ratings_rank_details_blueme(data_ratingsRank)
                merged_df3 = pd.concat([ratingsRankDetails, ratingsRankDetailsBlueme], ignore_index=True)
                
                with st.expander("Classificação Detalhada"):
                    ratingsRankDetails = function_format_numeric_columns(merged_df3)
                    filtered_copy, count= component_plotDataframe(ratingsRankDetails, f"Classificação Detalhada {data_ratingsRank}")
                    function_copy_dataframe_as_tsv(filtered_copy)


        with row4[2]:
            with row5[1]:
                ratingsRankDetails2 = ratings_rank_details(data_ratingsRank2)
                ratingsRankDetailsBlueme2 = ratings_rank_details_blueme(data_ratingsRank2)
                merged_df4 = pd.concat([ratingsRankDetails2, ratingsRankDetailsBlueme2], ignore_index=True)

                with st.expander("Classificação Detalhada"):
                    ratingsRankDetails2 = function_format_numeric_columns(merged_df4)
                    filtered_copy, count= component_plotDataframe(ratingsRankDetails2, f"Classificação Detalhada {data_ratingsRank2}")
                    function_copy_dataframe_as_tsv(filtered_copy)





class CostManagement():
    def render(self):
        self.data = {}
        day_CostManagement1 = date(datetime.today().year - 1, 1, 1)
        day_CostManagement2 = date(datetime.today().year, 12, 31)
        data_ratingsRank = datetime.today().strftime('%Y-%m')
        self.data['generalRevenue'] = general_revenue(day_CostManagement1, day_CostManagement2, filters='')
        self.data['generalCosts'] = general_costs(day_CostManagement1, day_CostManagement2)
        self.data['costDetails'] = cost_details(day_CostManagement1, day_CostManagement2)
        self.data['ratingsRank'] = ratings_rank(data_ratingsRank)
        self.data['ratingsRankDetails'] = ratings_rank_details(data_ratingsRank)
        self.data['generalCostsBlueme'] = general_costs_blueme(day_CostManagement1, day_CostManagement2)
        self.data['costsBluemeDetails'] = costs_blueme_details(day_CostManagement1, day_CostManagement2)
        self.data['ratingsRankBlueme'] = ratings_rank_blueme(data_ratingsRank)
        self.data['ratingsRankDetailsBlueme'] = ratings_rank_details_blueme(data_ratingsRank)
 
        BuildCostManagement(self.data['generalRevenue'],
                            self.data['generalCosts'],
                            self.data['costDetails'],
                            self.data['ratingsRank'],
                            self.data['ratingsRankDetails'],
                            self.data['generalCostsBlueme'],
                            self.data['costsBluemeDetails'],
                            self.data['ratingsRankBlueme'],
                            self.data['ratingsRankDetailsBlueme'])
