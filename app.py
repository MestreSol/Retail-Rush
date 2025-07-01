import os
import sys
import streamlit as st

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
    tab_names = ["📅 Calendário", "💰 Mercado Financeiro", "🧪 Testes de Mesa", "📊 Comparação", "ℹ️ Sobre"]
    selected_tab = st.sidebar.selectbox("Escolha uma seção:", tab_names)
  
    if selected_tab == "📅 Calendário":
        st.title(selected_tab)
        st.markdown("Este é um teste de conceito para o calendário.")
        st.write("Aqui você pode adicionar funcionalidades relacionadas ao calendário.")
    elif selected_tab == "💰 Mercado Financeiro":
        st.title(selected_tab)
        st.markdown("Este é um teste de conceito para o mercado financeiro.")
        st.write("Aqui você pode adicionar funcionalidades relacionadas ao mercado financeiro.")
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