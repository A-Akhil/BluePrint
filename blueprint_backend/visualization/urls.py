from django.urls import path
from . import views

urlpatterns = [
    path('diversity-map/', views.species_diversity_map, name='diversity_map'),
    path('taxonomic-composition/', views.taxonomic_composition_chart, name='taxonomic_composition'),
    path('confidence-distribution/', views.confidence_distribution, name='confidence_distribution'),
]
