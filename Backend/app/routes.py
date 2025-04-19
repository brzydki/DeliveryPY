from flask import request
from flask_restful import Api, Resource
from app.services import RestaurantService, MenuService, OrderService
from app.models import Restaurant, MenuItem, Order

api = Api()

class RestaurantListResource(Resource):
    def get(self):
        restaurants = RestaurantService.get_all_restaurants()
        return [{
            'id': r.id,
            'name': r.name,
            'address': r.address,
            'phone': r.phone
        } for r in restaurants]

    def post(self):
        data = request.get_json()
        restaurant = RestaurantService.create_restaurant(data)
        return {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'phone': restaurant.phone
        }, 201

class RestaurantResource(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'phone': restaurant.phone
        }

class MenuListResource(Resource):
    def get(self, restaurant_id):
        menu_items = MenuService.get_restaurant_menu(restaurant_id)
        return [{
            'id': m.id,
            'name': m.name,
            'description': m.description,
            'price': m.price
        } for m in menu_items]

    def post(self, restaurant_id):
        data = request.get_json()
        menu_item = MenuService.add_menu_item(restaurant_id, data)
        return {
            'id': menu_item.id,
            'name': menu_item.name,
            'description': menu_item.description,
            'price': menu_item.price
        }, 201

class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        return [{
            'id': o.id,
            'customer_name': o.customer_name,
            'customer_address': o.customer_address,
            'customer_phone': o.customer_phone,
            'status': o.status,
            'items': [{
                'id': i.id,
                'menu_item_id': i.menu_item_id,
                'quantity': i.quantity
            } for i in o.items]
        } for o in orders]

    def post(self):
        data = request.get_json()
        order = OrderService.create_order(data)
        return {
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_address': order.customer_address,
            'customer_phone': order.customer_phone,
            'status': order.status,
            'items': [{
                'id': i.id,
                'menu_item_id': i.menu_item_id,
                'quantity': i.quantity
            } for i in order.items]
        }, 201

class OrderResource(Resource):
    def get(self, order_id):
        order = OrderService.get_order(order_id)
        return {
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_address': order.customer_address,
            'customer_phone': order.customer_phone,
            'status': order.status,
            'items': [{
                'id': i.id,
                'menu_item_id': i.menu_item_id,
                'quantity': i.quantity,
                'menu_item': {
                    'id': i.menu_item.id,
                    'name': i.menu_item.name,
                    'price': i.menu_item.price
                }
            } for i in order.items]
        }

    def patch(self, order_id):
        data = request.get_json()
        if 'status' not in data:
            return {'message': 'Status is required'}, 400
        order = OrderService.update_order_status(order_id, data['status'])
        return {
            'id': order.id,
            'status': order.status
        }

def register_resources(api):
    api.add_resource(RestaurantListResource, '/api/restaurants')
    api.add_resource(RestaurantResource, '/api/restaurants/<int:restaurant_id>')
    api.add_resource(MenuListResource, '/api/restaurants/<int:restaurant_id>/menu')
    api.add_resource(OrderListResource, '/api/orders')
    api.add_resource(OrderResource, '/api/orders/<int:order_id>')

register_resources(api)