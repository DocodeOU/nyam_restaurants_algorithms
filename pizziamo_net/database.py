from nyam_restaurants_algorithms.app.abstract_database import AbstractDatabase


class DatabasePizziamoNet(AbstractDatabase):
    
    def __init__(self, json):
        super().__init__(json=json)
