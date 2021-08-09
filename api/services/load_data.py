from dataclasses import dataclass

import pandas as pd
from django.contrib.gis.geos import fromstr

from api.models import (
    District,
    Neighborhood,
    OpenMarket,
    Region,
    SubCityHall,
    SubRegion,
)


@dataclass
class LoadData:
    file: str

    def execute(self):
        """handle load_data"""
        df = pd.read_csv(self.file)
        df = self.rename_columns(df)
        df = self.format_location_point(df)
        self._create_districts(df[["DISTRICT_CODE", "DISTRICT"]])
        self._create_sub_city_hall(df[["COD_SUB_CITY_HALL", "SUB_CITY_HALL"]])
        self._create_regions(df[["REGION_O5"]])
        self._create_sub_regions(df[["REGION_O5", "REGION_O8"]])
        self._create_neighborhoods(df[["NEIGHBORHOOD"]])
        self._create_open_markets(
            df[
                [
                    "LOCATION",
                    "SECTOR",
                    "AREA",
                    "DISTRICT_CODE",
                    "COD_SUB_CITY_HALL",
                    "REGION_O8",
                    "NOME_OPEN_MARKET",
                    "REGISTER",
                    "PUBLIC_PLACE",
                    "NUMBER",
                    "NEIGHBORHOOD",
                    "REF",
                ]
            ]
        )

    @staticmethod
    def format_location_point(df):
        """help function to create location column and drp LAT and LONG column"""
        df["LOCATION"] = df.apply(
            lambda row: fromstr(f'POINT({row["LAT"]} {row["LONG"]})', srid=4326), axis=1
        )
        df.drop(["LAT", "LONG"], axis=1, inplace=True)
        return df

    @staticmethod
    def rename_columns(df):
        """rename columns in data frame"""
        original_columns = list(df.columns)
        rename_columns = [
            "ID",
            "LONG",
            "LAT",
            "SECTOR",
            "AREA",
            "DISTRICT_CODE",
            "DISTRICT",
            "COD_SUB_CITY_HALL",
            "SUB_CITY_HALL",
            "REGION_O5",
            "REGION_O8",
            "NOME_OPEN_MARKET",
            "REGISTER",
            "PUBLIC_PLACE",
            "NUMBER",
            "NEIGHBORHOOD",
            "REF",
        ]
        df.rename(columns=dict(zip(original_columns, rename_columns)), inplace=True)
        return df

    def _create_districts(self, df):
        """help function to create district model"""
        unique_districts = df.drop_duplicates()
        unique_districts.columns = ["district_code", "name"]

        list_district = []
        for _, row in unique_districts.iterrows():
            row = self.to_upper(row)
            list_district.append(District(**row))

        District.objects.bulk_create(list_district)

    def _create_sub_city_hall(self, df):
        """help function to create city hall"""
        unique_sub_city_hall = df.drop_duplicates()
        unique_sub_city_hall.columns = ["cod_sub_city_hall", "name"]

        list_sub_city_hall = []
        for _, row in unique_sub_city_hall.iterrows():
            row = self.to_upper(row)
            list_sub_city_hall.append(SubCityHall(**row))
        SubCityHall.objects.bulk_create(list_sub_city_hall)

    def _create_regions(self, df):
        """help function to create regions model"""
        unique_regions = df.drop_duplicates()
        unique_regions.columns = ["name"]

        list_regions = []
        for _, row in unique_regions.iterrows():
            row = self.to_upper(row)
            list_regions.append(Region(**row))
        Region.objects.bulk_create(list_regions)

    def _create_sub_regions(self, df):
        """help function to create sub regions model"""
        unique_sub_regions = df.drop_duplicates()
        unique_sub_regions.columns = ["region", "name"]

        list_sub_regions = []
        for _, row in unique_sub_regions.iterrows():
            row = self.to_upper(row)
            row["region"] = Region.objects.get(name=row["region"])
            list_sub_regions.append(SubRegion(**row))
        SubRegion.objects.bulk_create(list_sub_regions)

    def _create_neighborhoods(self, df):
        """help function to create neighborhood"""
        unique_neighborhoods = df.drop_duplicates()
        unique_neighborhoods.columns = ["name"]
        list_neighborhoods = []
        for _, row in unique_neighborhoods.iterrows():
            row = self.to_upper(row)
            list_neighborhoods.append(Neighborhood(**row))
        Neighborhood.objects.bulk_create(list_neighborhoods)

    def _create_open_markets(self, df):
        """help function to create open markets"""
        unique_open_markets = df.drop_duplicates(subset="REGISTER")
        unique_open_markets.columns = [
            "location",
            "sector",
            "area",
            "district",
            "sub_city_hall",
            "sub_region",
            "name",
            "register",
            "public_place",
            "number",
            "neighborhood",
            "ref",
        ]

        list_open_market = []
        for _, row in unique_open_markets.iterrows():
            row = self.to_upper(row)
            row["number"] = self.parse_number(row["number"])
            row["district"] = District.objects.get(district_code=row["district"])
            row["sub_city_hall"] = SubCityHall.objects.get(
                cod_sub_city_hall=row["sub_city_hall"]
            )
            row["sub_region"] = SubRegion.objects.get(name=row["sub_region"])
            row["neighborhood"] = Neighborhood.objects.get(name=row["neighborhood"])
            row["ref"] = row["ref"][: OpenMarket._meta.get_field("ref").max_length]
            list_open_market.append(OpenMarket(**row))
        OpenMarket.objects.bulk_create(list_open_market)

    @staticmethod
    def to_upper(row):
        """help functo to upper case"""
        return {k: str(v).upper().strip() for k, v in row.items()}

    @staticmethod
    def parse_number(nb):
        """help function to parse number"""
        try:
            return str(int(float(nb)))
        except ValueError:
            return str(nb)
