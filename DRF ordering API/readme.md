# Food Ordering API

This repository contains the Food Ordering API , which is built using Django REST Framework (DRF). This API facilitates various functionalities related to food ordering and restaurant management.

## Project URLs

The project includes the following URLs and corresponding views:

1. **Admin Interface**:
   - URL: `/admin/`
   - Description: Django Admin interface for managing site administration.

2. **API Endpoints**:
   - URL: `/api/`
   - Description: Includes various API endpoints for managing different aspects of the food ordering system.

3. **User Authentication Endpoints**:
   - URL: `/api/`
   - Description: Endpoints provided by `djoser` for user authentication and management.

4. **Token Authentication Endpoint**:
   - URL: `/token/login/`
   - Description: Endpoint for obtaining authentication tokens using `obtain_auth_token`.

5. **Menu Items Endpoints**:
   - URL: `/menu-items`
   - View: `MenuItemsView`
   - Description: Endpoint for managing restaurant menu items.

6. **Individual Menu Item Endpoint**:
   - URL: `/menu-items/<int:pk>`
   - View: `MenuItemView`
   - Description: Endpoint for retrieving, updating, or deleting individual menu items.

7. **Orders Endpoint**:
   - URL: `/orders`
   - View: `orders_view`
   - Description: Endpoint for managing orders placed by customers.

8. **Individual Order Endpoint**:
   - URL: `/orders/<int:pk>`
   - View: `order_item_view`
   - Description: Endpoint for retrieving, updating, or deleting individual orders.

9. **Shopping Cart Endpoint**:
   - URL: `/cart/menu-items`
   - View: `cart_view`
   - Description: Endpoint for managing the shopping cart, including adding, removing, or updating items.

10. **Categories Endpoint**:
    - URL: `/categories`
    - View: `CategoryView`
    - Description: Endpoint for managing menu categories.

11. **Delivery Crew Group Management Endpoint**:
    - URL: `/groups/delivery-crew/users`
    - Description: Endpoint for managing users belonging to the delivery crew group.

12. **Individual Delivery Crew User Endpoint**:
    - URL: `/groups/delivery-crew/users/<int:pk>`
    - View: `delivery_delete_view`
    - Description: Endpoint for retrieving, updating, or deleting individual users belonging to the delivery crew group.

13. **Manager Group Management Endpoint**:
    - URL: `/groups/manager/users`
    - Description: Endpoint for managing users belonging to the manager group.

14. **Individual Manager User Endpoint**:
    - URL: `/groups/manager/users/<int:pk>`
    - View: `manager_delete_view`
    - Description: Endpoint for retrieving, updating, or deleting individual users belonging to the manager group.

## Installation and Setup

For installation and setup instructions, please refer to the main README file of this repository.

Explore the DRF Food Ordering API and utilize its endpoints for efficient restaurant management and food ordering processes!