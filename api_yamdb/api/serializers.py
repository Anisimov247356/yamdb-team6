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
    """Сериализатор для чтения произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    # Временно.
    # rating = serializers.IntegerField( read_only=True, default=None,)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения произведений.
    """

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )

    def validate_year(self, value):
        """Проверка года выпуска."""
        if not isinstance(value, int):
            raise serializers.ValidationError(
                'Год выпуска должен быть целым числом.'
            )
        return value

    def validate_name(self, value):
        """Проверка длины названия."""
        if len(value) > 256:
            raise serializers.ValidationError(
                'Название произведения не может быть длиннее 256 символов.'
            )
        return value
