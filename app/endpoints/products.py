from typing import Dict

from flask import Blueprint, jsonify, request

from app import db
from app.models.products import Product, Brand, Category
from app.schema.products import ProductCreateRequest, ProductUpdateRequest

from flask_pydantic import validate

products_blueprint = Blueprint('products', __name__)


def build_product_args(data: ProductUpdateRequest) -> Dict:
    """
    Turn ProductSchema into dict for updating Product orm object.
    Result can be used can be used as constructor argument
    or can be iterated through to update field values.

    @param data: request data ProductCreateRequest
    @return: dict with data
    """
    create_args = data.dict(exclude_unset=True)

    if data.brand is not None:
        create_args["brand"] = Brand.get(data.brand)

    if data.categories is not None:
        create_args["categories"] = Category.get_all(data.categories)

    if data.rating is not None:
        create_args["featured"] = data.rating > 8

    return create_args


@products_blueprint.route('/products', methods=['GET'])
def get_products():
    """
    Get full list of products.
    @return: List of product representations.
    """
    return jsonify({
        'results': [p.serialized for p in Product.query.all()]
    })


@products_blueprint.route('/products', methods=['POST'])
def create_product():
    product_create = ProductCreateRequest.parse_raw(request.data)
    product_args = build_product_args(product_create)
    new_product = Product()

    new_product.name = product_args.get('name')
    new_product.rating = product_args.get('rating')
    new_product.featured = product_args.get('featured')
    new_product.expiration_date = product_args.get('expiration_date')
    new_product.brand_id = product_args.get('brand').id
    new_product.categories = product_args.get('categories')
    new_product.items_in_stock = product_args.get('items_in_stock')
    new_product.receipt_date = product_args.get('receipt_date')
    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.serialized), 201


@products_blueprint.route('/products/<int:product_id>', methods=['GET'])
def read_product(product_id: int):
    """
    Get product by its ID.
    @param product_id: ID of wanted product.
    @return: Wanted product representation.
    """
    product: Product = Product.get(product_id)

    return jsonify(product.serialized)


@products_blueprint.route('/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id: int):
    product: Product = Product.get(product_id)

    product_update = ProductUpdateRequest.parse_raw(request.data)
    product_args = build_product_args(product_update)
    if product_args.get('name'):
        product.name = product_args.get('name')
    if product_args.get('rating'):
        product.rating = product_args.get('rating')
    if product_args.get('featured'):
        product.featured = product_args.get('featured')
    if product_args.get('expiration_date'):
        product.expiration_date = product_args.get('expiration_date')
    if product_args.get('brand').id:
        product.brand_id = product_args.get('brand').id
    if product_args.get('categories'):
        product.categories = product_args.get('categories')
    if product_args.get('items_in_stock'):
        product.items_in_stock = product_args.get('items_in_stock')
    if product_args.get('receipt_date'):
        product.receipt_date = product_args.get('receipt_date')
    db.session.add(product)
    db.session.commit()
    return jsonify(product.serialized)


@products_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    """
    Remove product by its ID.

    @param product_id: ID of product we want to delete.
    @return: Simple status message.
    """
    product: Product = Product.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({"status": "ok"})
