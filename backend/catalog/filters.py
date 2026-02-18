from rest_framework import filters
from rest_framework.exceptions import ValidationError
from .models import Film


class FilmFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        title = request.query_params.get("title")
        rating = request.query_params.get("rating")
        year = request.query_params.get("release_year")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if rating:
            rating_choices = Film.Rating.values

            if rating in rating_choices:
                queryset = queryset.filter(rating=rating)
            else:
                raise ValidationError(
                    {
                        "rating": f"Invalid value. Allowed values: {', '.join(rating_choices)}"
                    }
                )

        if year:
            if str(year).isdigit():
                queryset = queryset.filter(release_year=year)
            else:
                raise ValidationError({"release_year": "This must be a numeric year."})

        return queryset
