# Retail Rush

Este repositório reúne toda a documentação pública e os scripts de testes automatizados para o projeto **Dawson Miller Supermarket Systems**. Aqui você encontrará:

- Especificações de cada sistema (Produtos, Economia, Região, Clima, etc.)  
- Prompts e templates para geração de testes de mesa via GitHub Copilot  
- Testes unitários e de integração para validação das mecânicas  
- Guias de estilo e contribuição para documentação  

---

## 📂 Estrutura de Pastas

```text
/
├─ docs/                   # Documentação de sistemas e guides
│   ├─ sistema-produtos.md
│   ├─ sistema-economia.md
│   ├─ sistema-regiao.md
│   ├─ sistema-clima.md
│   └─ prompts-copilot.md
├─ tests/
│   ├─ unit/               # Testes unitários (NUnit)
│   │   ├─ ProductsTests.cs
│   │   ├─ EconomyTests.cs
│   │   └─ RegionTests.cs
│   ├─ integration/        # Testes de integração / playmode
│   │   ├─ MultiplayerTests.cs
│   │   └─ EndToEndScenarios.cs
│   └─ mesa/               # Testes de mesa (ASCII/Markdown tables)
│       ├─ economia-mesa.md
│       └─ regiao-mesa.md
├─ .github/
│   └─ workflows/          # GitHub Actions para CI (dotnet test)
├─ README.md               # (este arquivo)
└─ LICENSE
````

---

## 🚀 Começando

1. **Clone este repositório**

   ```bash
   git clone https://github.com/mestresol/retail-rush.git
   cd retail-rush
   ```

2. **Instale dependências de testes**

   * Requer [.NET SDK 6.0+](https://dotnet.microsoft.com/download)
   * No Windows/macOS/Linux:

     ```bash
     dotnet restore
     ```

3. **Executar todos os testes**

   ```bash
   dotnet test
   ```

4. **Gerar/Atualizar testes de mesa**

   * Veja exemplos em `tests/mesa/`
   * Use os prompts em `docs/prompts-copilot.md` para expandir cenários com Copilot.

---

## 📖 Documentação

Em `docs/` estão as especificações detalhadas de cada subsistema:

* **Sistema de Produtos** (`sistema-produtos.md`)
  Cadastro, atributos, validade, estoque e produção interna.

* **Sistema de Economia** (`sistema-economia.md`)
  Notícias, inflação, eleições, promoções, mercado paralelo e segurança.

* **Sistema de Região** (`sistema-regiao.md`)
  Perfis de cidades (demografia, tributos, clima) e suas interações.

* **Sistema de Clima & Sazonalidade** (`sistema-clima.md`)
  Tipos climáticos, estações e impacto na demanda.

* **Prompts Copilot** (`prompts-copilot.md`)
  Templates para geração automática de testes de mesa via GitHub Copilot.

---

## ✅ Testes

* **Unitários** (`tests/unit/`):
  Cobrem regras de negócio isoladas (ex.: cálculo de inflação, descontos de validade).

* **Integração** (`tests/integration/`):
  Cenários de ponta a ponta (ex.: ciclo de pedido → entrega → venda → reposição).

* **Mesa** (`tests/mesa/`):
  Tabelas de cenários manuais para validar lógica antes da implementação.

---

## 🤝 Como Contribuir

1. Fork este repositório.
2. Crie uma branch: `feature/atualiza-docs` ou `feature/novo-teste`.
3. Faça commits claros e descritivos.
4. Abra um Pull Request referenciando as issues relacionadas.
5. Siga o guia de estilo em `docs/CONTRIBUTING.md`.

---

## 🔒 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

Obrigado por colaborar!


