# eBay-like E-Commerce Auction Site

## Demonstration
Watch the [YouTube video](https://youtu.be/nUbgh1810Ig) to see the application in action.

## Project Overview
This project involves the development of an eBay-like e-commerce auction site using Django. Users can post auction listings, place bids on listings, comment on listings, and add listings to a watchlist. The application is designed to facilitate online auctions, providing a platform for users to buy and sell items through bidding.

### Features
- **Create Listing**: Users can create new auction listings with details such as title, description, starting bid, optional image URL, and category.
- **Active Listings Page**: Display all active auction listings with essential details like title, description, current price, and photo.
- **Listing Page**: View specific details of each listing, including current price, option to add to watchlist, bid functionality, ability to close auction, and display of comments.
- **Watchlist**: Users can add listings to their watchlist and view them on a dedicated page.
- **Categories**: Display a list of all listing categories with links to view active listings in each category.
- **Django Admin Interface**: Site administrator can manage listings, comments, and bids via the Django admin interface.

## Getting Started

### Prerequisites
- Python 3.x
- Django 2.x or 3.x

### Installation
1. Clone the project 
2. Open a terminal and navigate to the `commerce` directory.
3. Run the following commands to set up the application:
   ```sh
   python manage.py makemigrations auctions
   python manage.py migrate
   python manage.py createsuperuser  # Create a superuser account for admin access
   ```
4. Start the Django development server:
   ```sh
   python manage.py runserver
   ```
5. Open a web browser and go to `http://127.0.0.1:8000` to access the application.

## Usage
- **Creating a Listing**: Visit the create listing page to add a new auction listing.
- **Viewing Active Listings**: Explore all active auction listings on the homepage.
- **Viewing Listing Details**: Click on a listing to view its details, place bids, add to watchlist, and comment.
- **Managing Watchlist**: Access the watchlist page to view all listings added to your watchlist.
- **Exploring Categories**: Browse listings by category to find items of interest.
- **Admin Interface**: Access the Django admin interface at `/admin` to manage listings, comments, and bids.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments
- Harvard University's CS50 course for the project idea and initial guidelines.
- Django and Python communities for their support and resources.
