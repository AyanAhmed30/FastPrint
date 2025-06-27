from rest_framework import serializers
from .models import (
    ComicTrimSize,
    ComicInteriorColor,
    ComicPaperType,
    ComicCoverFinish,
    ComicBindingType,
)


class ComicTrimSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicTrimSize
        fields = '__all__'


class ComicInteriorColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicInteriorColor
        fields = '__all__'


class ComicPaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicPaperType
        fields = '__all__'


class ComicCoverFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicCoverFinish
        fields = '__all__'


class ComicBindingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicBindingType
        fields = '__all__'
