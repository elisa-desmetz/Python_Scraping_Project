import pandas as pd

class Ladder:
    def __init__(self, name:str, df:pd.DataFrame) -> None:
        """
            Ladder class constructor
        
        Args:
            name (str): Ladder's caption
            df (pd.DataFrame): Ladder's data DataFrame
        """
        self.name = name
        self.df = df
        
    @staticmethod
    def to_dict(name:str, df:pd.DataFrame) -> dict:
        """
            Returns a dictionnary built with parameters' value.
        
        Args:
            name (str): Ladder's caption
            df (pd.DataFrame): Ladder's data DataFrame
        
        Returns:
            dict: Dictionnary of parameters' value.
        """
        return dict(name=name, df=df)