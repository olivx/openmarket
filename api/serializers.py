from rest_framework import serializers

from api.models import (
    District,
    Neighborhood,
    OpenMarket,
    Region,
    SubCityHall,
    SubRegion,
)


class NeighborhoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Neighborhood
        fields = "__all__"


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class SubCityHallSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCityHall
        fields = "__all__"


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class SubRegionSerializer(serializers.HyperlinkedModelSerializer):
    region_id = serializers.IntegerField(write_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = SubRegion
        fields = "__all__"


class OpenMarketSerializer(serializers.HyperlinkedModelSerializer):
    neighborhood = NeighborhoodSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    sub_city_hall = SubCityHallSerializer(read_only=True)
    sub_region = SubRegionSerializer(read_only=True)

    neighborhood_id = serializers.IntegerField(write_only=True)
    district_id = serializers.IntegerField(write_only=True)
    sub_city_hall_id = serializers.IntegerField(write_only=True)
    sub_region_id = serializers.IntegerField(write_only=True)

    def upper_case(self, validated_data):
        upper_case_dt = {
            k: v.upper() for k, v in validated_data.items() if isinstance(v, str)
        }
        return validated_data.update(upper_case_dt)

    def create(self, validated_data):
        self.upper_case(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.upper_case(validated_data)

        return super().update(instance, validated_data)

    class Meta:
        model = OpenMarket
        fields = "__all__"
        # geo_field = 'location'
