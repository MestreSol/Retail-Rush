from typing import List, Callable, Optional
from .game_date import GameDate
from .season import Season


class GameCalendar:
    def __init__(self, current_date: GameDate, current_season: Season, seasons: List[Season]):
        """
        Inicializa o calendário do jogo.
        
        Args:
            current_date: Data atual do jogo
            current_season: Estação atual
            seasons: Lista de estações disponíveis
        """
        self.current_date = current_date
        self._current_season = current_season
        self._seasons = seasons
        
        # Events - usando listas de callbacks para simular events do C#
        self._on_date_changed_callbacks: List[Callable[[GameDate], None]] = []
        self._on_season_changed_callbacks: List[Callable[[Season], None]] = []
    
    @property
    def current_date(self) -> GameDate:
        """Data atual do calendário."""
        return self._current_date
    
    @current_date.setter
    def current_date(self, value: GameDate):
        self._current_date = value
    
    @property
    def current_season(self) -> Season:
        """Estação atual do calendário."""
        return self._current_season
    
    @property
    def seasons(self) -> List[Season]:
        """Lista de estações disponíveis."""
        return self._seasons
    
    def add_date_changed_listener(self, callback: Callable[[GameDate], None]):
        """Adiciona um listener para mudanças de data."""
        self._on_date_changed_callbacks.append(callback)
    
    def remove_date_changed_listener(self, callback: Callable[[GameDate], None]):
        """Remove um listener de mudanças de data."""
        if callback in self._on_date_changed_callbacks:
            self._on_date_changed_callbacks.remove(callback)
    
    def add_season_changed_listener(self, callback: Callable[[Season], None]):
        """Adiciona um listener para mudanças de estação."""
        self._on_season_changed_callbacks.append(callback)
    
    def remove_season_changed_listener(self, callback: Callable[[Season], None]):
        """Remove um listener de mudanças de estação."""
        if callback in self._on_season_changed_callbacks:
            self._on_season_changed_callbacks.remove(callback)
    
    def _invoke_date_changed(self, date: GameDate):
        """Invoca todos os callbacks de mudança de data."""
        for callback in self._on_date_changed_callbacks:
            callback(date)
    
    def _invoke_season_changed(self, season: Season):
        """Invoca todos os callbacks de mudança de estação."""
        for callback in self._on_season_changed_callbacks:
            callback(season)
    
    def advance_time(self, years: int = 0, months: int = 0, days: int = 0, 
                    hours: int = 0, minutes: int = 0):
        """
        Avança o tempo do calendário.
        
        Args:
            years: Anos a avançar
            months: Meses a avançar
            days: Dias a avançar
            hours: Horas a avançar
            minutes: Minutos a avançar
        """
        new_date = self.current_date.add(years, months, days, hours, minutes)
        
        # Se a data não mudou, não faz nada
        if self._dates_equal(new_date, self.current_date):
            return
            
        self.current_date = new_date
        self._invoke_date_changed(self.current_date)
        
        # Verifica se a estação mudou
        new_season = self._get_season_for_date(self.current_date)
        if (new_season is None or 
            (self._current_season is not None and 
             new_season.season_name == self._current_season.season_name)):
            return
            
        self._current_season = new_season
        self._invoke_season_changed(self._current_season)
    
    def set_date(self, target: GameDate):
        """
        Define a data do calendário diretamente.
        
        Args:
            target: Data alvo a ser definida
        """
        # Garante normalização da data
        new_date = target.add()
        
        # Se a data não mudou, não faz nada
        if self._dates_equal(new_date, self.current_date):
            return
            
        self.current_date = new_date
        self._invoke_date_changed(self.current_date)
        
        # Verifica se a estação mudou
        new_season = self._get_season_for_date(self.current_date)
        if (new_season is None or 
            (self._current_season is not None and 
             new_season.season_name == self._current_season.season_name)):
            return
            
        self._current_season = new_season
        self._invoke_season_changed(self._current_season)
    
    def _get_season_for_date(self, date: GameDate) -> Optional[Season]:
        """
        Retorna a estação correspondente à data informada.
        
        Args:
            date: Data para verificar a estação
            
        Returns:
            Estação correspondente ou None se não encontrada
        """
        for season in self._seasons:
            if hasattr(season, 'is_in_season') and season.is_in_season(date):
                return season
        return None
    
    def _dates_equal(self, date1: GameDate, date2: GameDate) -> bool:
        """
        Verifica se duas datas são iguais.
        
        Args:
            date1: Primeira data
            date2: Segunda data
            
        Returns:
            True se as datas são iguais, False caso contrário
        """
        return (date1.years == date2.years and
                date1.months == date2.months and
                date1.days == date2.days and
                date1.hours == date2.hours and
                date1.minutes == date2.minutes)
