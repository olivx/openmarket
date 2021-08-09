from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=False)
router.register(
    r"open-market", views.OpenMarketViewSet, basename=views.OpenMarketViewSet.name
)
router.register(
    r"neighborhood", views.NeighborhoodViewSet, basename=views.NeighborhoodViewSet.name
)
router.register(
    r"districts", views.DistrictViewSet, basename=views.DistrictViewSet.name
)
router.register(
    r"sub-city-hall",
    views.SubCityHallViewSet,
    basename=views.SubCityHallViewSet.name,
)
router.register(r"regions", views.RegionViewSet, basename=views.RegionViewSet.name)
router.register(
    r"sub-regions", views.SubRegionViewSet, basename=views.SubRegionViewSet.name
)

urlpatterns = router.urls
