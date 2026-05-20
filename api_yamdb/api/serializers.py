from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    """

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.
    """

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализотор для чтония произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения произведений.
    """

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_fields='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        quryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        madel = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
