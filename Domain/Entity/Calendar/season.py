from .season_type import SeasonType

class Season:
    def __init__(self, season_name="", season_duration=0):
        self.season_name = season_name
        self.season_duration = season_duration  # Fixed typo: was 'season_duraiton'
        self.active = False  # Initialize 'active' attribute

    @property
    def season_type(self):
        mapping = {
            "Spring": SeasonType.Spring,
            "Summer": SeasonType.Summer,
            "Autumn": SeasonType.Autumn,
            "Winter": SeasonType.Winter
        }
        return mapping.get(self.season_name, None)

    def season_start(self):
        print(f"Iniciando a temporada: {self.season_name} ({self.season_type}) por {self.season_duration} dias.")
        self.active = True

    def season_end(self):
        print(f"Finalizando a temporada: {self.season_name}")
        self.active = False

    def is_in_season(self, date):
        """
        Verifica se uma data está dentro desta estação.
        Para simplificar, vamos usar uma lógica baseada em meses:
        - Spring: meses 2, 3, 4 (Março, Abril, Maio)
        - Summer: meses 5, 6, 7 (Junho, Julho, Agosto)  
        - Autumn: meses 8, 9, 10 (Setembro, Outubro, Novembro)
        - Winter: meses 11, 0, 1 (Dezembro, Janeiro, Fevereiro)
        """
        month = date.months
        if self.season_name == "Spring":
            return month in [2, 3, 4]
        elif self.season_name == "Summer":
            return month in [5, 6, 7]
        elif self.season_name == "Autumn":
            return month in [8, 9, 10]
        elif self.season_name == "Winter":
            return month in [11, 0, 1]
        return False
