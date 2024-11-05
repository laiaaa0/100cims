import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class SummitList:
    def __init__(self, summits: pd.DataFrame):
        self._summits = summits
        self._parse_coordinates()
        self._geolocator = Nominatim(user_agent="100cims_bot")

    def _parse_coordinate(self, coord: str):
        """
        Given a coordinate string such as
         42° 04′ 34″ N
         2° 24′ 26″ E

        return the value of the actual coordinate in decimal values
        """
        first_num_str = coord[: coord.find("°")]
        second_num_str = coord[coord.find("°") + 1 : coord.find("′")]
        third_num_str = coord[coord.find("′") + 1 : coord.find("″")]
        whole_num = (
            int(first_num_str) + int(second_num_str) / 60 + int(third_num_str) / 3600
        )
        return whole_num

    def _parse_coordinates_text(self, coord: str):
        """
        After receiving a coordinate string such as 42° 04′ 34″ N, 2° 24′ 26″ E
        return a tuple of (latitude, longitude) in decimal values
        """
        split_coord = coord.split(",")
        latitude_str = split_coord[0]
        longitude_str = split_coord[1]

        return self._parse_coordinate(latitude_str), self._parse_coordinate(
            longitude_str
        )

    def _parse_coordinates(self):

        lat_long = self._summits["Coordenades"].apply(self._parse_coordinates_text)
        self._summits["Coordinates"] = lat_long

    def get_closest_summits(
        self, location_name: str, *, limit_num: int = 5, max_distance_km: float = 40
    ):
        """
        Return the closest summits to a specified location

        :param str location_name: The name of the location around which to find the peaks
        :param int limit_num: Number of summits to return
        :param float max_distance_km: Maximum distance from the peaks allowed

        """
        location = self._geolocator.geocode(location_name)
        if location is None:
            return pd.DataFrame()
        filtered_df = pd.DataFrame()

        self._summits["Distance"] = self._summits["Coordinates"].map(
            lambda x: geodesic(x, (location.latitude, location.longitude)).km
        )

        filtered_df = self._summits[
            self._summits["Distance"] < max_distance_km
        ].sort_values(by="Distance")

        print(filtered_df)

        return filtered_df.head(limit_num)

    def size(self):
        return self._summits.shape[0]


def load_from_file(file_path: str) -> SummitList:
    return SummitList(pd.read_csv(file_path))


def message_from_df(df: pd.DataFrame) -> str:
    peak_list = [
        f'{x["Nom"]} ({x["Elevació s.n.m. en m"]}m) a {x["Distance"]:.1f} km'
        for _, x in df.iterrows()
    ]
    return "\n".join(peak_list)
