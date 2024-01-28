from math import radians, cos, sin, asin, sqrt


class FutsalFinder:
    @classmethod
    def calc_dist(cls, lat1, long1, lat2, long2):
        """
            lat1: your lalatitude
            long1: your longitude
            lat2: futsal lalatitude
            long2: futsal lalatitude
        """
        # convert decimal degrees to radians 
        lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
        # haversine formula 
        dlon = long2 - long1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        # Radius of earth in kilometers is 6371
        km = 6371* c
        return km

