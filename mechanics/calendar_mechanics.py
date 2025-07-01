import datetime
import os
import random
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

from Domain.Entity.Calendar.forecast import forecast
from Domain.Entity.Calendar.game_date import GameDate
from Domain.Entity.Calendar.season import Season

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class CalendarMechanics:
    def __init__(self):
        self.season_colors = {
            "Spring": "#00FF00", 
            "Summer": "#FFFF00",  
            "Autumn": "#FFA500",  
            "Winter": "#FFFFFF"   
        }

        self.weather_symbols = {
            forecast.Sunny: "☀️",
            forecast.Cloudy: "☁️",
            forecast.Snow: "❄️",
            forecast.Rain: "🌧️"
        }

        self.weather_names = {
            forecast.Sunny: "Ensolarado",
            forecast.Cloudy: "Nublado",
            forecast.Snow: "Nevando",
            forecast.Rain: "Chuvoso"
        }

    def create_seasons(self, season_config=None):
        # Default four seasons if nothing passed
        if not season_config:
            return [
                Season("Spring", 90),
                Season("Summer", 90),
                Season("Autumn", 90),
                Season("Winter", 95),
            ]

        seasons = []

        if isinstance(season_config, dict):
            iterator = season_config.items()
        else:  # list/tuple
            iterator = [
                (entry[0], entry[1])
                for entry in season_config
                if len(entry) >= 2
            ]

        for season_name, days in iterator:
            seasons.append(Season(season_name, days))

        return seasons
    
    def _get_season_for_date(self, date, seasons):
        for season in seasons:
            if season.is_in_season(date):
                return season
        return seasons[0]
    
    def generate_calendar_data(self, days=365, season_config=None, show_debug=False):
        calendar_data = []
        current_date = GameDate(years=1, months=0, days=1)
        
        seasons = self.create_seasons(season_config)
        
        if season_config:
            for name, days, symbol in season_config:
                if name not in self.season_colors:
                    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"]
                    self.season_colors[name] = random.choice(colors)
        
        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        
        current_month = 0  
        current_day_of_month = 1
        
        season_transitions = []
        accumulated_days = 0
        for season in seasons:
            season_transitions.append(accumulated_days)
            accumulated_days += season.season_duration  
        
        season_transitions.append(accumulated_days)
        
        if show_debug:
            print(f"🔍 Debug: Criadas {len(seasons)} estações:")
            for i, season in enumerate(seasons):
                print(f"  {i+1}. {season.season_name}: {season.season_duration} dias")
            
            print(f"🔍 Debug: Transições de estações:")
            for i, season in enumerate(seasons):
                season_start = season_transitions[i] + 1 if i > 0 else 1
                season_end = season_transitions[i + 1]
                print(f"  {season.season_name}: dias {season_start} a {season_end}")
            
            print(f"🔍 Debug: Total de dias para gerar: {days}")
            print(f"🔍 Debug: Total de dias das estações: {accumulated_days}")
        
        if days > accumulated_days and show_debug:
            print(f"⚠️ Debug: Dias solicitados ({days}) > Total estações ({accumulated_days}). Irá repetir ciclo de estações.")
        elif days < accumulated_days and show_debug:
            print(f"⚠️ Debug: Dias solicitados ({days}) < Total estações ({accumulated_days}). Algumas estações serão parciais.")
        
        for day in range(days):
            current_season_name = "Spring"  
            current_day_1_based = day + 1  
            
            cycle_day = ((current_day_1_based - 1) % accumulated_days) + 1
            
            for i, season in enumerate(seasons):
                season_start = season_transitions[i] + 1 if i > 0 else 1
                season_end = season_transitions[i + 1]
                
                if season_start <= cycle_day <= season_end:
                    current_season_name = season.season_name
                    break
            
            if show_debug and (day < 10 or day >= days - 5):
                cycle_info = f" (ciclo dia {cycle_day})" if days > accumulated_days else ""
                print(f"  Dia {current_day_1_based}: Estação = {current_season_name}{cycle_info}, Mês = {month_names[current_month]}, Dia do mês = {current_day_of_month}")
            
            weather_options = [forecast.Sunny, forecast.Cloudy, forecast.Rain]
            weather = random.choice(weather_options)
            weather_name = self.weather_names.get(weather, "Desconhecido")
            weather_symbol = self.weather_symbols.get(weather, "?")
            
            base_temp = {
                "Spring": 18, "Summer": 28, "Autumn": 15, "Winter": 8
            }.get(current_season_name, 18)
            
            weather_modifier = {
                forecast.Sunny: 5, forecast.Cloudy: 0, forecast.Rain: -3
            }.get(weather, 0)
            
            temperature = base_temp + weather_modifier + random.randint(-5, 5)
            
            calendar_data.append({
                'Dia': day + 1,
                'Data': f"{current_month + 1:02d}/{current_day_of_month:02d}",
                'Mes': month_names[current_month],
                'Mes_Numero': current_month + 1,
                'Dia_Mes': current_day_of_month,
                'Estacao': current_season_name,
                'Cor_Estacao': self.season_colors.get(current_season_name, "#FFFFFF"),
                'Previsao_Tempo': weather_name,
                'Tempo_Simbolo': weather_symbol,
                'Tempo_Codigo': weather,
                'Temperatura': temperature,
                'Temperatura_Texto': f"{temperature}°C"
            })
            
            current_day_of_month += 1
            
            if current_day_of_month > days_per_month[current_month]:
                current_month += 1
                current_day_of_month = 1
                
                if current_month >= 12:
                    current_month = 0
        
        df_result = pd.DataFrame(calendar_data)
        if show_debug:
            print(f"🔍 Debug: DataFrame criado com {len(df_result)} linhas")
            print(f"  Colunas: {df_result.columns.tolist()}")
            if not df_result.empty:
                print(f"  Primeiras estações: {df_result['Estacao'].head().tolist()}")
        
        return df_result
    
    def create_interactive_calendar(self, df):
        """Cria um calendário interativo usando Plotly com layout simplificado por estações."""
        
        # Verificar se há dados
        if df.empty:
            st.error("❌ Nenhum dado para exibir no calendário")
            return None
        
        print(f"🔍 Debug: Criando calendário visual com {len(df)} dias") if hasattr(st, 'session_state') and st.session_state.get('show_debug', False) else None
        
         # Verificar se há dados
        if df.empty:
            st.error("❌ Nenhum dado para exibir no calendário")
            return None
        
        print(f"🔍 Debug: Criando calendário visual com {len(df)} dias") if hasattr(st, 'session_state') and st.session_state.get('show_debug', False) else None
        
        try:
            if df.empty:
                st.error("❌ Nenhum dado para exibir no calendário")
                return None

            # Garantir que todos os dados estejam presentes
            cols = ['Dia', 'Data', 'Mes', 'Mes_Numero', 'Dia_Mes', 'Estacao',
                'Cor_Estacao', 'Previsao_Tempo', 'Tempo_Simbolo', 
                'Tempo_Codigo', 'Temperatura', 'Temperatura_Texto']
            df = df[cols]

            # Exibir tabela interativa no Streamlit
            st.dataframe(df, use_container_width=True)
            return None

        except Exception as e:
            st.error(f"❌ Erro ao exibir tabela do calendário: {str(e)}")
            print(f"❌ Debug: Erro na tabela do calendário: {str(e)}") if hasattr(st, 'session_state') and st.session_state.get('show_debug', False) else None
            return None
    
    def create_monthly_calendar(self, df):
        """Cria um calendário mensal tradicional usando Plotly."""
        
        if df.empty:
            st.error("❌ Nenhum dado para exibir no calendário mensal")
            return None
        
        print(f"🔍 Debug: Criando calendário mensal com {len(df)} dias") if hasattr(st, 'session_state') and st.session_state.get('show_debug', False) else None
        
        try:
            # Configuração dos meses
            months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                     'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
            
            # Criar subplots - 4 linhas x 3 colunas para 12 meses
            fig = make_subplots(
                rows=4, cols=3,
                subplot_titles=months,
                vertical_spacing=0.12,
                horizontal_spacing=0.08
            )
            
            # Processar dados por mês
            for month_num in range(1, 13):
                month_data = df[df['Mes_Numero'] == month_num]
                
                if month_data.empty:
                    continue
                
                # Calcular posição do subplot
                row = ((month_num - 1) // 3) + 1
                col = ((month_num - 1) % 3) + 1
                
                # Organizar dados em grade de calendário (assumindo início em domingo)
                # Para simplificar, vamos usar uma grade 6x7 (6 semanas x 7 dias)
                for _, day_data in month_data.iterrows():
                    day_of_month = day_data['Dia_Mes']
                    
                    # Posição simplificada: dia da semana baseado no dia do mês
                    # (Esta é uma aproximação, idealmente usaríamos datetime para calcular corretamente)
                    week = (day_of_month - 1) // 7
                    day_of_week = (day_of_month - 1) % 7
                    
                    x_pos = day_of_week
                    y_pos = 5 - week  # Inverter para que primeira semana fique no topo
                    
                    # Hover text detalhado
                    hover_text = (f"📅 <b>{day_data['Data']}</b><br>"
                                 f"🌍 Estação: <b>{day_data['Estacao']}</b><br>"
                                 f"🌤️ Tempo: <b>{day_data['Previsao_Tempo']} {day_data['Tempo_Simbolo']}</b><br>"
                                 f"🌡️ Temperatura: <b>{day_data['Temperatura_Texto']}</b><br>"
                                 f"📊 Dia do ano: {day_data['Dia']}")
                    
                    # Adicionar marcador para o dia
                    fig.add_trace(
                        go.Scatter(
                            x=[x_pos],
                            y=[y_pos],
                            mode='markers+text',
                            text=f"{day_of_month}<br>{day_data['Tempo_Simbolo']}",
                            textfont=dict(size=8, color="white"),
                            marker=dict(
                                size=25,
                                color=day_data['Cor_Estacao'],
                                opacity=0.8,
                                line=dict(color="white", width=1)
                            ),
                            hovertemplate=hover_text + "<extra></extra>",
                            showlegend=False,
                            name=""
                        ),
                        row=row, col=col
                    )
                
                # Configurar eixos para cada subplot
                fig.update_xaxes(
                    range=[-0.5, 6.5],
                    tickmode='array',
                    tickvals=list(range(7)),
                    ticktext=['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
                    showgrid=True,
                    gridcolor="lightgray",
                    row=row, col=col
                )
                
                fig.update_yaxes(
                    range=[-0.5, 5.5],
                    showticklabels=False,
                    showgrid=True,
                    gridcolor="lightgray",
                    row=row, col=col
                )
            
            # Configurar layout geral
            fig.update_layout(
                title={
                    'text': f"📅 Calendário Mensal Tradicional - {len(df)} Dias<br><sub style='font-size:12px'>🌍 Estações | 🌤️ Clima | 🌡️ Temperatura</sub>",
                    'x': 0.5,
                    'font': {'size': 16, 'color': 'darkblue'}
                },
                height=1000,
                width=1400,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='#f8f9fa',
                margin=dict(l=50, r=50, t=120, b=50)
            )
            
            print(f"✅ Debug: Calendário mensal criado com sucesso!") if hasattr(st, 'session_state') and st.session_state.get('show_debug', False) else None
            return fig
            
        except Exception as e:
            st.error(f"❌ Erro ao criar calendário mensal: {str(e)}")
            print(f"❌ Debug: Erro no calendário mensal: {str(e)}") if hasattr(st, 'session_state') and st.session_state.get('show_debug', False) else None
            return None
    
    def create_summary_charts(self, df):
        """Cria gráficos resumo do calendário."""
        
        # Contagem por estação e tempo
        season_counts = df['Estacao'].value_counts()
        weather_counts = df['Previsao_Tempo'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza - Estações
            fig_season = go.Figure(data=[go.Pie(
                labels=season_counts.index,
                values=season_counts.values,
                marker_colors=[self.season_colors[season] for season in season_counts.index],
                title="Distribuição por Estações"
            )])
            fig_season.update_layout(height=400)
            st.plotly_chart(fig_season, use_container_width=True)
        
        with col2:
            # Gráfico de pizza - Tempo
            weather_colors = {'Ensolarado': '#FFD700', 'Nublado': '#87CEEB', 'Chuvoso': '#4682B4'}
            fig_weather = go.Figure(data=[go.Pie(
                labels=weather_counts.index,
                values=weather_counts.values,
                marker_colors=[weather_colors.get(weather, '#CCCCCC') for weather in weather_counts.index],
                title="Distribuição do Tempo"
            )])
            fig_weather.update_layout(height=400)
            st.plotly_chart(fig_weather, use_container_width=True)
        
        # Gráfico de linha - Temperaturas ao longo do ano
        st.markdown("##### 🌡️ Variação de Temperatura ao Longo do Ano")
        temp_fig = go.Figure()
        temp_fig.add_trace(go.Scatter(
            x=df['Dia'],
            y=df['Temperatura'],
            mode='lines',
            name='Temperatura',
            line=dict(color='red', width=2),
            hovertemplate="Dia %{x}<br>Temperatura: %{y}°C<extra></extra>"
        ))
        temp_fig.update_layout(
            title="Temperatura Diária",
            xaxis_title="Dia do Ano",
            yaxis_title="Temperatura (°C)",
            height=400
        )
        st.plotly_chart(temp_fig, use_container_width=True)
    
    def get_summary(self):
        """Retorna um resumo dos dados do calendário."""
        df = self.generate_calendar_data(365)
        
        season_counts = df['Estacao'].value_counts().to_dict()
        weather_counts = df['Previsao_Tempo'].value_counts().to_dict()
        
        return {
            "total_dias": len(df),
            "distribuicao_estacoes": season_counts,
            "distribuicao_tempo": weather_counts,
            "primeiro_dia": df.iloc[0]['Data'],
            "ultimo_dia": df.iloc[-1]['Data'],
            "temperatura_media": df['Temperatura'].mean(),
            "temperatura_min": df['Temperatura'].min(),
            "temperatura_max": df['Temperatura'].max()
        }
    
    def run(self):
        st.markdown("#### 🎛️ Configurações")
        
        st.markdown("##### 🌍 Configuração das Estações")
        
        season_mode = st.radio(
            "Modo de configuração das estações:",
            ["🎯 Estações Padrão", "⚙️ Estações Customizadas"],
            horizontal=True
        )
        
        if season_mode == "🎯 Estações Padrão":
            col_season1, col_season2, col_season3, col_season4 = st.columns(4)
            
            with col_season1:
                spring_days = st.number_input("🌱 Primavera (dias)", min_value=1, max_value=365, value=90, step=1)
            
            with col_season2:
                summer_days = st.number_input("☀️ Verão (dias)", min_value=1, max_value=365, value=90, step=1)
            
            with col_season3:
                autumn_days = st.number_input("🍂 Outono (dias)", min_value=1, max_value=365, value=90, step=1)
            
            with col_season4:
                winter_days = st.number_input("❄️ Inverno (dias)", min_value=1, max_value=365, value=95, step=1)
            
            season_config = [
                ("Spring", spring_days, "🌱"),
                ("Summer", summer_days, "☀️"),
                ("Autumn", autumn_days, "🍂"),
                ("Winter", winter_days, "❄️")
            ]
        
        else:  # Estações Customizadas
            st.markdown("**Configure suas próprias estações:**")
            
            if 'custom_seasons' not in st.session_state:
                st.session_state['custom_seasons'] = [
                    {"name": "Primavera", "days": 90, "symbol": "🌱"},
                    {"name": "Verão", "days": 90, "symbol": "☀️"},
                    {"name": "Outono", "days": 90, "symbol": "🍂"},
                    {"name": "Inverno", "days": 95, "symbol": "❄️"}
                ]
            
            col_add1, col_add2 = st.columns([3, 1])
            with col_add1:
                new_season_name = st.text_input("Nome da nova estação", placeholder="Ex: Estação das Chuvas")
            with col_add2:
                if st.button("➕ Adicionar Estação") and new_season_name:
                    st.session_state['custom_seasons'].append({
                        "name": new_season_name,
                        "days": 30,
                        "symbol": "🌍"
                    })
                    st.success(f"Estação '{new_season_name}' adicionada!")
                    st.rerun()
            
            season_config = []
            for i, season in enumerate(st.session_state['custom_seasons']):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
                
                with col1:
                    season_name = st.text_input(f"Nome", value=season['name'], key=f"season_name_{i}")
                
                with col2:
                    season_days = st.number_input(f"Dias", min_value=1, max_value=365, 
                                                value=season['days'], step=1, key=f"season_days_{i}")
                
                with col3:
                    season_symbol = st.text_input(f"Símbolo", value=season['symbol'], 
                                                max_chars=2, key=f"season_symbol_{i}")
                
                with col4:
                    if st.button("🗑️", key=f"delete_season_{i}", help="Remover estação"):
                        st.session_state['custom_seasons'].pop(i)
                        st.rerun()
                
                st.session_state['custom_seasons'][i] = {
                    "name": season_name,
                    "days": season_days,
                    "symbol": season_symbol
                }
                
                season_config.append((season_name, season_days, season_symbol))
            
            spring_days = season_config[0][1] if len(season_config) > 0 else 90
            summer_days = season_config[1][1] if len(season_config) > 1 else 90
            autumn_days = season_config[2][1] if len(season_config) > 2 else 90
            winter_days = season_config[3][1] if len(season_config) > 3 else 95
        
        total_season_days = sum([config[1] for config in season_config])
        
        if total_season_days != 365:
            if total_season_days < 365:
                st.warning(f"⚠️ Total de dias das estações: {total_season_days}. Faltam {365 - total_season_days} dias para completar um ano.")
            else:
                st.warning(f"⚠️ Total de dias das estações: {total_season_days}. Excedem {total_season_days - 365} dias de um ano padrão.")
        else:
            st.success(f"✅ Total de dias das estações: {total_season_days} (ano completo!)")
        
        # Controles principais
        col_config1, col_config2, col_config3 = st.columns([2, 2, 1])
        
        with col_config1:
            max_days = max(365, total_season_days)
            default_days = 365 if total_season_days >= 365 else total_season_days
            days_to_generate = st.slider("📅 Dias para simular", 30, max_days, default_days)
        
        with col_config2:
            show_charts = st.checkbox("📊 Mostrar análises detalhadas", value=True)
        
        with col_config3:
            show_debug = st.checkbox("🔧 Debug", value=False, help="Mostrar informações de debug no console")
            if show_debug:
                st.session_state['show_debug'] = True
            else:
                st.session_state['show_debug'] = False
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            generate_data = st.button("🚀 Gerar Calendário", type="primary", use_container_width=True)
        
        if generate_data:
            with st.spinner("🔄 Gerando dados do calendário..."):
                df = self.generate_calendar_data(
                    days_to_generate, 
                    season_config=season_config,
                    show_debug=show_debug
                )
                st.session_state['calendar_data'] = df
                st.session_state['days_count'] = days_to_generate
                st.session_state['season_config'] = season_config
                st.success(f"✅ Calendário de {len(df)} dias gerado com sucesso!")
        
        # Mostrar dados se existirem
        if 'calendar_data' in st.session_state:
            df = st.session_state['calendar_data']
            
            # Verificar se o DataFrame não está vazio
            if df.empty:
                st.error("❌ Erro: DataFrame vazio. Tente gerar novamente.")
                return
            
            # Métricas principais em destaque
            st.markdown("---")
            st.markdown("### 📊 Resumo do Calendário")
            
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("📅 Total de Dias", len(df))
            with col_m2:
                most_common_season = df['Estacao'].value_counts().index[0]
                season_count = df['Estacao'].value_counts().iloc[0]
                st.metric("🌍 Estação Principal", most_common_season, f"{season_count} dias")
            with col_m3:
                most_common_weather = df['Previsao_Tempo'].value_counts().index[0]
                weather_count = df['Previsao_Tempo'].value_counts().iloc[0]
                st.metric("🌤️ Tempo Predominante", most_common_weather, f"{weather_count} dias")
            with col_m4:
                avg_temp = df['Temperatura'].mean()
                st.metric("🌡️ Temperatura Média", f"{avg_temp:.1f}°C")
            
            # CALENDÁRIO VISUAL - SEMPRE MOSTRADO
            st.markdown("---")
            st.markdown("### 📅 Calendário Visual Interativo")
            st.markdown("*Navegue pelo calendário para ver detalhes de cada dia: estação, clima e temperatura*")
            
            # Opções de visualização
            calendar_type = st.radio(
                "Escolha o tipo de visualização:",
                ["📊 Timeline por Estações", "📆 Calendário Mensal Tradicional"],
                horizontal=True
            )
            
            try:
                if calendar_type == "📊 Timeline por Estações":
                    calendar_fig = self.create_interactive_calendar(df)
                else:
                    calendar_fig = self.create_monthly_calendar(df)
                
                if calendar_fig is not None:
                    st.plotly_chart(calendar_fig, use_container_width=True)
                else:
                    st.error("❌ Erro ao gerar o calendário visual")
            except Exception as e:
                st.error(f"❌ Erro ao criar calendário: {str(e)}")
                st.write("Debug - DataFrame info:")
                st.write(f"Shape: {df.shape}")
                st.write(f"Columns: {df.columns.tolist()}")
                if not df.empty:
                    st.write("Primeiras linhas:")
                    st.dataframe(df.head())
            
            # Distribuição das estações
            st.markdown("---")
            st.markdown("### 🌍 Distribuição por Estações")
            
            season_data = df['Estacao'].value_counts()
            num_seasons = len(season_data)
            
            # Criar colunas dinâmicas baseadas no número de estações
            if num_seasons <= 4:
                season_cols = st.columns(num_seasons)
                for i, (season, count) in enumerate(season_data.items()):
                    with season_cols[i]:
                        percentage = (count / len(df)) * 100
                        # Tentar obter símbolo das estações configuradas
                        symbol = "🌍"  # Default
                        if 'season_config' in st.session_state:
                            for name, days, sym in st.session_state['season_config']:
                                if name == season:
                                    symbol = sym
                                    break
                        else:
                            # Símbolos padrão
                            default_symbols = {"Spring": "🌱", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"}
                            symbol = default_symbols.get(season, "🌍")
                        
                        st.metric(f"{symbol} {season}", f"{count} dias", f"{percentage:.1f}%")
            else:
                # Para mais de 4 estações, usar múltiplas linhas
                cols_per_row = 4
                rows_needed = (num_seasons + cols_per_row - 1) // cols_per_row
                
                season_items = list(season_data.items())
                for row in range(rows_needed):
                    start_idx = row * cols_per_row
                    end_idx = min(start_idx + cols_per_row, num_seasons)
                    season_cols = st.columns(end_idx - start_idx)
                    
                    for i, (season, count) in enumerate(season_items[start_idx:end_idx]):
                        with season_cols[i]:
                            percentage = (count / len(df)) * 100
                            # Tentar obter símbolo das estações configuradas
                            symbol = "🌍"  # Default
                            if 'season_config' in st.session_state:
                                for name, days, sym in st.session_state['season_config']:
                                    if name == season:
                                        symbol = sym
                                        break
                            else:
                                # Símbolos padrão
                                default_symbols = {"Spring": "🌱", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"}
                                symbol = default_symbols.get(season, "🌍")
                            
                            st.metric(f"{symbol} {season}", f"{count} dias", f"{percentage:.1f}%")
            
            # Gráficos de análise (opcional)
            if show_charts:
                st.markdown("---")
                st.markdown("### 📈 Análises Detalhadas")
                self.create_summary_charts(df)
            
            # Downloads e dados tabulares
            st.markdown("---")
            st.markdown("### 💾 Exportar Dados")
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv,
                    file_name=f"calendario_{len(df)}_dias.csv",
                    mime="text/csv",
                    use_container_width=True,
                    help="Baixar dados em formato CSV (texto separado por vírgulas)"
                )
            
            with col_d2:
                # Botão para exportar JSON (mais simples que Excel)
                try:
                    json_data = df.to_json(orient='records', indent=2)
                    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = f"calendario_simulacao_{len(df)}dias_{current_time}.json"
                    
                    st.download_button(
                        label="📊 Download JSON",
                        data=json_data,
                        file_name=file_name,
                        mime="application/json",
                        use_container_width=True,
                        help="Baixar dados em formato JSON com estrutura completa"
                    )
                except Exception as e:
                    st.error(f"❌ Erro ao gerar JSON: {str(e)}")
                    if st.button("🔄 Tentar Novamente", use_container_width=True):
                        st.rerun()
            
            with col_d3:
                if st.button("📋 Ver Dados Tabulares", use_container_width=True):
                    st.session_state['show_table'] = not st.session_state.get('show_table', False)
            
            # Mostrar tabela se solicitado
            if st.session_state.get('show_table', False):
                st.markdown("#### 📋 Dados Completos")
                st.dataframe(df, use_container_width=True)
        
        else:
            # Primeira vez - instruções
            st.markdown("---")
            st.info("👆 **Configure os parâmetros acima e clique em 'Gerar Calendário' para começar!**")
            
            # Mostrar exemplo do que será gerado
            st.markdown("### 🎯 O que você verá:")
            st.markdown("""
            - **📅 Calendário Visual**: Layout mensal com 365 dias
            - **🌍 Estações**: Cores diferentes para cada estação do ano (configuráveis)
            - **🌤️ Clima**: Símbolos e informações do tempo para cada dia
            - **🌡️ Temperatura**: Simulação realista baseada na estação e clima
            - **📊 Estatísticas**: Distribuição de estações, clima e métricas
            - **📈 Análises**: Gráficos interativos com insights
            - **💾 Exportação**: Download em CSV e visualização tabular
            """)
