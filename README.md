# Retail Rush

Um simulador de gestão de supermercado em Unity 3D, com multiplayer client–server usando Mirror. No papel de gestor, você administrará estoques, finanças, marketing e logística, em modos cooperativo ou competitivo, em cenários dinâmicos e realistas.

---

## 📋 Sumário

- [Visão Geral](#visão-geral)  
- [Principais Funcionalidades](#principais-funcionalidades)  
- [Arquitetura do Projeto](#arquitetura-do-projeto)  
- [Pré-requisitos](#pré-requisitos)  
- [Instalação e Execução](#instalação-e-execução)  
- [Estrutura de Pastas](#estrutura-de-pastas)  
- [Mecânicas e Sistemas](#mecânicas-e-sistemas)  
  - [Sistema de Produtos](#sistema-de-produtos)  
  - [Sistema de Economia (Dinheiro)](#sistema-de-economia-dinheiro)  
  - [Sistema de Região e Clima](#sistema-de-região-e-clima)  
  - [Outros Sistemas Chave](#outros-sistemas-chave)  
- [Multiplayer com Mirror](#multiplayer-com-mirror)  
- [Como Jogar](#como-jogar)  
- [Testes e Qualidade](#testes-e-qualidade)  
- [Roadmap](#roadmap)  
- [Contribuindo](#contribuindo)  
- [Licença](#licença)  
- [Contato](#contato)

---

## 🎯 Visão Geral

Dawson Miller Supermarket Systems é um jogo de simulação e estratégia em que você assume o papel de gerente de supermercado. Com modos Coop e Concorrência, o título combina:

- **Gestão de Estoque** (produtos, validade, produção interna)  
- **Economia Dinâmica** (notícias, inflação, eleições, marketing)  
- **Perfis Regionais** (cidades dos EUA com clima, demografia e tributos próprios)  
- **Multiplayer Client–Server** via Mirror para competir ou cooperar em tempo real  

---

## 🚀 Principais Funcionalidades

- **Modos de Jogo**: Coop, Concorrência, Mercado livre e Campanha História  
- **Sistema de Produtos**: cadastro, estoque, validade, produção própria  
- **Sistema de Economia**: notícias, inflação, eleições, promoções, mercado ilegal  
- **Sistema de Região**: perfis de cidades (NYC, LA, Chicago, Miami) com sales tax, população, clima  
- **Marketing e Fidelização**: campanhas, programas de pontos e parcerias locais  
- **Logística**: caminhões de entrega, fornecedores dinâmicos e leilões  
- **Segurança**: furtos, câmeras, seguranças e consequências de crime  
- **Eventos e Crises**: greves, falência de fornecedores, desastres climáticos  
- **Progressão e Customização**: evolução de mercado, perks de gestor, decoração de apartamento  
- **Narrativa**: lore nos diálogos, missões temáticas e eventos sazonais  

---

## 🏗️ Arquitetura do Projeto

- **Engine**: Unity 2021.3 LTS (recomendado)  
- **Rede**: Mirror (Client–Server)  
- **Linguagem**: C#  
- **Padrões**: Clean Architecture, SOLID  
- **Serialização/Config**: ScriptableObjects para dados de produtos, regiões e eventos  
- **UI**: Unity UI (Canvas + TextMeshPro)  
- **Persistência**: JSON local ou servidor dedicado (futuro)  

---

## 📦 Pré-requisitos

- Unity 2021.3 LTS ou superior  
- Pacote **Mirror** (versão 53.3.0 ou superior)  
- .NET 4.x Scripting Runtime  
- Git (para controle de versão)  

---

## ⚙️ Instalação e Execução

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/seu-usuario/dawson-supermarket.git
   cd dawson-supermarket
    ```

2. **Abra no Unity**

   * Abra o Unity Hub
   * Adicione a pasta do projeto
   * Selecione Unity 2021.3 LTS

3. **Importe o Mirror**

   * `Window ▶ Package Manager ▶ + ▶ Add package from git URL…`
   * Cole `https://github.com/vis2k/Mirror.git#release`

4. **Execute a Cena Principal**

   * `Assets/Scenes/Main.unity`
   * No Inspector de **NetworkManager**, configure Network Address e Port
   * Para servidor: clique em **Play ▶ Host**
   * Para cliente: clique em **Play ▶ Client**

---

## 📁 Estrutura de Pastas

```
Assets/
├─ Scenes/            # Cenas do jogo
├─ Scripts/           # Todos os scripts C#
│  ├─ Network/        # Gerenciamento Mirror, mensagens e handlers
│  ├─ Economy/        # Lógica de dinheiro, inflação, eleições
│  ├─ Products/       # Cadastro, estoque, validade, produção
│  ├─ Region/         # Perfis de cidades, clima e demografia
│  ├─ UI/             # Canvas, telas e pop-ups
│  └─ Utils/          # Helpers e extensões genéricas
├─ Art/               # Sprites, modelos 3D, ícones
├─ Prefabs/           # Objetos pré-fabricados
└─ Config/            # ScriptableObjects e dados JSON
```

---

## ⚙️ Mecânicas e Sistemas

### Sistema de Produtos

* **Cadastro**: SKU, nome, categoria, fornecedor, preço base, unidade
* **Estoque**: quantidade atual, mínimo, alertas, FIFO para perecíveis
* **Validade**: descarte automático, descontos progressivos, promoções
* **Produção Interna**: padaria, açougue, laticínios com linha de produção
* **Sazonalidade**: ajustes automáticos por estação e eventos climáticos
* **Integração Regional**: mix de produtos recomendados por perfil de cidade

### Sistema de Economia (Dinheiro)

* **Notícias**: modificadores de preço/demanda/disponibilidade por evento externo
* **Eleições**: impostos, regulamentações e subsídios baseados no resultado local
* **Inflação**: variação semanal ou choque de mercado, promoções para “frear” inflação
* **Promoções por E-mail**: ofertas limitadas de fornecedores (descontos e prazo)
* **Marketing**: campanhas locais, redes sociais e patrocínios sazonais
* **Economia Paralela**: contrabando com margem alta e risco de multa
* **Segurança & Furtos**: taxa de perda de estoque, investimento em câmeras/seguranças
* **Fidelidade**: programa de pontos, níveis Bronze/Prata/Ouro e recompensas
* **Crises & Emergências**: menu de ações em greves, quebras de estoque e falências
* **Parcerias Locais**: acordos de revenda com divisão de receita

### Sistema de Região e Clima

Para cada cidade dos EUA (NYC, LA, Chicago, Miami):

* **Eleições**: porcentagem de votos dos principais candidatos
* **Sales Tax**: alíquota local
* **Demografia**: faixa etária e composição étnica
* **Clima**: ensolarado, chuvoso, nevado, nublado
* **Inflação Base & Renda Média**
* **Produtos em Alta**: mix recomendado por estação e perfil do público

### Outros Sistemas Chave

* **Modo Coop & Concorrência**: multiplayer competitivo ou cooperativo
* **Caminhão de Entrega**: logística, custos e imprevistos
* **Fornecedores Dinâmicos**: negociação via leilão e trade-off preço/qualidade
* **Eventos Temáticos**: Black Friday, Natal e datas comemorativas
* **Progressão & Customização**: evolução de loja, perks e decoração de apartamento
* **Lore & Diálogos**: NPCs com histórias, dicas e humor

---

## 🔗 Multiplayer com Mirror

* **NetworkManager** centraliza conexões Client–Server
* **NetworkIdentity** e **NetworkBehaviour** em objetos sincronizados
* **SyncVars**, **Commands** e **RPCs** para atualizar estado de jogo
* **Matchmaking** básico via lobby local ou via Steam (futuro)

---

## ▶️ Como Jogar

1. Inicie como Host ou Client no editor Unity
2. Conecte até 4 jogadores (COOP ou vs CPU)
3. Defina perfil de região e dificuldade
4. Gerencie estoque, finanças e estratégias para superar desafios
5. Complete missões de campanha ou alcance metas de lucro

---

## ✅ Testes e Qualidade

* **Testes Unitários**: NUnit para lógica de produtos, economia e regionais
* **Testes de Integração**: simulações de partidas com Mirror em modo playmode
* **Testes de Mesa**: tabelas com cenários de economia e região (eventos, inflação, demografia)

---

## 🛣️ Roadmap

* [ ] Lobby com Steamworks
* [ ] Servidor dedicado na nuvem
* [ ] Suporte a mods e balanceamento dinâmico
* [ ] IA avançada de concorrência
* [ ] Analytics em tempo real

---

## 🤝 Contribuindo

1. Fork este repositório
2. Crie um branch `feature/nome-da-sua-feature`
3. Commit suas mudanças com mensagens claras
4. Abra um Pull Request detalhando alterações

---

## 📄 Licença

Este projeto está sob a [MIT License](LICENSE).

---

## ✉️ Contato

Desenvolvido por **\[Seu Nome]**

* GitHub: [github.com/seu-usuario](https://github.com/seu-usuario)
* E-mail: [seu.email@exemplo.com](mailto:seu.email@exemplo.com)

Boa sorte e bons negócios! 🚀

