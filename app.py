import os
import sys
import streamlit as st

from mechanics.calendar_mechanics import CalendarMechanics
from mechanics.news_mechanics import NewsMechanics
from mechanics.election_mechanics import ElectionMechanics
from mechanics.currency_mechanics import CurrencyMechanics
from mechanics.product_mechanics import ProductMechanics
from mechanics.inflation_mechanics import InflationMechanics
from mechanics.region_mechanics import RegionMechanics

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    st.set_page_config(
        page_title="Retail Rush - Teste de conceito",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("🧪 Testes")
    st.sidebar.markdown("---")
    tab_names = [
        "📅 Calendário",
        "💰 Mercado Financeiro",
        "💱 Moedas",
        "📈 Inflação",
        "📦 Produtos",
        "📰 Eventos",
        "🗳 Eleições",
        "🌐 Regiões",
        "🧪 Testes de Mesa",
        "📊 Comparação",
        "ℹ️ Sobre",
    ]
    selected_tab = st.sidebar.selectbox("Escolha uma seção:", tab_names)
  
    if selected_tab == "📅 Calendário":
        st.title(selected_tab)
        st.header("📅 Sistema de Calendário")
        st.markdown("Teste do sistema de calendário com 365 dias, estações e previsão do tempo.")
        
        calendar_mechanics = CalendarMechanics()
        calendar_mechanics.run()

    elif selected_tab == "💰 Mercado Financeiro":
        st.title(selected_tab)
        st.markdown("Este é um teste de conceito para o mercado financeiro.")
        st.write("Aqui você pode adicionar funcionalidades relacionadas ao mercado financeiro.")
    elif selected_tab == "💱 Moedas":
        st.title(selected_tab)
        currency_mechanics = CurrencyMechanics()
        currency_mechanics.run()
    elif selected_tab == "📈 Inflação":
        st.title(selected_tab)
        inflation_mechanics = InflationMechanics()
        # Simple placeholder interface
        st.markdown("### Índice de Inflação")
        if "inflation_system" not in st.session_state:
            st.session_state["inflation_system"] = inflation_mechanics
        else:
            inflation_mechanics = st.session_state["inflation_system"]

        col1, col2 = st.columns(2)
        with col1:
            shock = st.checkbox("Choque de Oferta/Demanda (+3%)", key="shock")
            promo = st.number_input("Promoção (-%)", min_value=0.0, max_value=0.5, value=0.0, step=0.01, key="promo")
            if st.button("Avançar Dia"):
                inflation_mechanics.advance_day(shock=shock, promotion_effect=promo)
        with col2:
            st.metric("Índice Atual", f"{inflation_mechanics.current_index:.3f}")
            history = [rec.index for rec in inflation_mechanics.history]
            if history:
                st.line_chart(history)
    elif selected_tab == "📦 Produtos":
        st.title(selected_tab)
        product_mechanics = ProductMechanics()
        product_mechanics.run()
    elif selected_tab == "📰 Eventos":
        st.title(selected_tab)
        news_mechanics = NewsMechanics()
        news_mechanics.run()
    elif selected_tab == "🗳 Eleições":
        st.title(selected_tab)
        election_mechanics = ElectionMechanics()
        election_mechanics.run()
    elif selected_tab == "🌐 Regiões":
        st.title(selected_tab)
        region_mechanics = RegionMechanics()
        region_mechanics.run()
    elif selected_tab == "🧪 Testes de Mesa":
        st.title(selected_tab)
        st.markdown("Este é um teste de conceito para testes de mesa.")
        st.write("Aqui você pode adicionar funcionalidades relacionadas aos testes de mesa.")
    elif selected_tab == "📊 Comparação":
        st.title(selected_tab)
        st.markdown("Este é um teste de conceito para comparação.")
        st.write("Aqui você pode adicionar funcionalidades relacionadas à comparação.")
    elif selected_tab == "ℹ️ Sobre":
        st.title(selected_tab)
        st.markdown("Este é um teste de conceito para informações sobre o projeto.")
        st.write("Aqui você pode adicionar informações sobre o Retail Rush.")

if __name__ == "__main__":
    main()
