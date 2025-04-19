import React, { useState, useEffect } from 'react';

function App() {
    const [restaurants, setRestaurants] = useState([]);
    const [menu, setMenu] = useState([]);
    const [orders, setOrders] = useState([]);
    const [selectedRestaurant, setSelectedRestaurant] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchRestaurants = () => {
        setLoading(true);
        setError(null);
        fetch('/api/restaurants')
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                setRestaurants(data);
                setLoading(false);
            })
            .catch(error => {
                setError(error.message);
                setLoading(false);
                console.error('Error fetching restaurants:', error);
            });
    };

    useEffect(() => {
        fetchRestaurants(); 

        fetch('/api/orders')
            .then(res => res.json())
            .then(data => setOrders(data))
            .catch(error => console.error('Error fetching orders:', error));
    }, []);

    const loadMenu = (restaurantId) => {
        setSelectedRestaurant(restaurantId);
        fetch(`/api/restaurants/${restaurantId}/menu`)
            .then(res => res.json())
            .then(data => setMenu(data))
            .catch(error => console.error('Error fetching menu:', error));
    };

    const createOrder = () => {
        const newOrder = {
            customer_name: "John Doe",
            customer_address: "123 Main St",
            customer_phone: "555-1234",
            items: [{ menu_item_id: 1, quantity: 2 }]
        };

        fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newOrder),
        })
            .then(res => res.json())
            .then(data => {
                setOrders([...orders, data]);
            })
            .catch(error => console.error('Error creating order:', error));
    };

    return (
        <div className="App">
            <h1>Food Delivery App</h1>

            <section>
                <h2>Restaurants</h2>
                <button onClick={fetchRestaurants} disabled={loading}>
                    {loading ? 'Loading...' : 'Refresh Restaurants'}
                </button>
                {error && <p style={{ color: 'red' }}>Error: {error}</p>}
                <ul>
                    {restaurants.map(restaurant => (
                        <li key={restaurant.id} onClick={() => loadMenu(restaurant.id)}>
                            {restaurant.name} - {restaurant.address}
                        </li>
                    ))}
                </ul>
            </section>

            {selectedRestaurant && (
                <section>
                    <h2>Menu</h2>
                    <ul>
                        {menu.map(item => (
                            <li key={item.id}>
                                {item.name} - ${item.price}
                            </li>
                        ))}
                    </ul>
                    <button onClick={createOrder}>Place Order</button>
                </section>
            )}

            <section>
                <h2>Orders</h2>
                <ul>
                    {orders.map(order => (
                        <li key={order.id}>
                            Order #{order.id} - Status: {order.status}
                        </li>
                    ))}
                </ul>
            </section>
        </div>
    );
}

export default App;