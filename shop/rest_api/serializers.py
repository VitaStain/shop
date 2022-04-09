from rest_framework import serializers

from main.models import (Category, Product, Shop_Product, Stock, Value,
                         ValueName)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ValueNameSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='value_type_id.name')

    class Meta:
        model = Value
        fields = ['name', 'value']


class Shop_ProductSerializer(serializers.ModelSerializer):
    address = serializers.ReadOnlyField(source='shop.address')

    class Meta:
        model = Shop_Product
        fields = ['address', 'number_products']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    shop = Shop_ProductSerializer(source='shop_product_set', many=True, read_only=True)
    characteristic = ValueNameSerializer(source='value_set', many=True, read_only=True)

    def create(self, validated_data):
        characteristics_data = validated_data.pop('characteristic')
        categories_data = validated_data.pop('category')
        product = Product.objects.create(**validated_data)

        for category_data in categories_data:
            category, q = Category.objects.get_or_create(**category_data)
            product.category.add(category)

        for characteristic_data in characteristics_data:
            characteristic, q = ValueName.objects.get_or_create(**characteristic_data)
            product.characteristic.add(characteristic)

        return product

    class Meta:
        model = Product
        fields = '__all__'


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class StockSerializer(serializers.ModelSerializer):
    product = ProductStockSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'
