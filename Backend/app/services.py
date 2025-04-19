from app import db
from app.models import Restaurant, MenuItem, Order, OrderItem


class RestaurantService:
    @staticmethod
    def create_restaurant(data):
        restaurant = Restaurant(
            name=data['name'],
            address=data['address'],
            phone=data['phone']
        )
        db.session.add(restaurant)
        db.session.commit()
        return restaurant

    @staticmethod
    def get_all_restaurants():
        return Restaurant.query.all()


class MenuService:
    @staticmethod
    def add_menu_item(restaurant_id, data):
        menu_item = MenuItem(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            restaurant_id=restaurant_id
        )
        db.session.add(menu_item)
        db.session.commit()
        return menu_item

    @staticmethod
    def get_restaurant_menu(restaurant_id):
        return MenuItem.query.filter_by(restaurant_id=restaurant_id).all()


class OrderService:
    @staticmethod
    def create_order(data):
        order = Order(
            customer_name=data['customer_name'],
            customer_address=data['customer_address'],
            customer_phone=data['customer_phone']
        )
        db.session.add(order)

        for item in data['items']:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item['menu_item_id'],
                quantity=item.get('quantity', 1)
            )
            db.session.add(order_item)

        db.session.commit()
        return order

    @staticmethod
    def get_order(order_id):
        return Order.query.get_or_404(order_id)

    @staticmethod
    def update_order_status(order_id, status):
        order = Order.query.get_or_404(order_id)
        order.status = status
        db.session.commit()
        return order