import streamlit as st
from datetime import date
from Domain.Entity.Product import Product, Inventory


class ProductMechanics:
    """Minimal interface for managing products and inventory."""

    def __init__(self):
        if "inventory" not in st.session_state:
            st.session_state["inventory"] = Inventory()

    def run(self):
        st.markdown("### 🛒 Sistema de Produtos")
        with st.expander("Cadastrar Produto"):
            sku = st.text_input("SKU")
            name = st.text_input("Nome")
            category = st.text_input("Categoria")
            supplier = st.text_input("Fornecedor")
            cost = st.number_input("Custo", value=0.0)
            price = st.number_input("Preço", value=0.0)
            unit = st.text_input("Unidade", value="un")
            if st.button("Adicionar Produto") and sku and name:
                prod = Product(sku, name, category, supplier, cost, price, unit)
                st.session_state[sku] = prod
                st.success(f"Produto {name} cadastrado")

        inv: Inventory = st.session_state["inventory"]
        st.markdown("---")
        st.markdown("#### Controle de Estoque")
        if st.session_state:
            skus = [k for k in st.session_state.keys() if isinstance(st.session_state[k], Product)]
        else:
            skus = []
        if skus:
            selected = st.selectbox("Produto", skus)
            qty = st.number_input("Quantidade", min_value=1, value=1)
            exp_date = st.date_input("Validade", value=date.today())
            if st.button("Adicionar ao Estoque"):
                prod = st.session_state[selected]
                inv.add_stock(prod, qty, exp_date)
                st.success("Estoque atualizado")
        else:
            st.info("Nenhum produto cadastrado")

        st.markdown("### Níveis de Estoque")
        for sku, entries in inv._stock.items():
            total = inv.get_quantity(sku)
            st.write(f"{sku}: {total} unidades")
