# Listings Models Documentation

## Overview

This document provides comprehensive documentation for the data models used in the ALX Travel App listings application. The models are designed to support a property rental platform similar to Airbnb, handling listings, bookings, and reviews.

## Table of Contents

- [Listing Model](#listing-model)
- [Booking Model](#booking-model)
- [Review Model](#review-model)
- [Model Relationships](#model-relationships)

---

## Listing Model

The `Listing` model represents a property available for rent on the platform.

### Fields

#### Basic Information

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `title` | CharField | Property title/name | max_length=200, required |
| `description` | TextField | Detailed property description | required |
| `property_type` | CharField | Type of property | max_length=20, choices from PROPERTY_TYPES |
| `host` | ForeignKey | Reference to User (property owner) | CASCADE delete, related_name='listings' |

#### Location

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `address` | CharField | Street address | max_length=255, required |
| `city` | CharField | City name | max_length=100, required |
| `country` | CharField | Country name | max_length=100, required |
| `neighborhood` | CharField | Neighborhood/district | max_length=100, optional |
| `latitude` | DecimalField | Geographic latitude | max_digits=9, decimal_places=6, optional |
| `longitude` | DecimalField | Geographic longitude | max_digits=9, decimal_places=6, optional |

#### Pricing

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `base_price` | DecimalField | Nightly rate in currency | max_digits=10, decimal_places=2, min=0 |

#### Capacity

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `max_guests` | PositiveIntegerField | Maximum number of guests | min=1, required |
| `bedrooms` | PositiveIntegerField | Number of bedrooms | default=1 |
| `beds` | PositiveIntegerField | Number of beds | default=1 |
| `bathrooms` | DecimalField | Number of bathrooms | max_digits=3, decimal_places=1, default=1 |

#### Amenities & Features

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `amenities` | TextField | Comma-separated amenities list | optional |
| `main_image` | URLField | URL to primary property image | optional |

#### House Rules

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `check_in_time` | TimeField | Check-in time | default='15:00' |
| `check_out_time` | TimeField | Check-out time | default='11:00' |
| `cancellation_policy` | CharField | Cancellation policy type | max_length=50, default='flexible' |
| `smoking_allowed` | BooleanField | Whether smoking is permitted | default=False |
| `pets_allowed` | BooleanField | Whether pets are permitted | default=False |

#### Status

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `status` | CharField | Listing status | choices from STATUS_CHOICES, default='active' |
| `is_available` | BooleanField | Availability flag | default=True |

#### Timestamps

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `created_at` | DateTimeField | Creation timestamp | auto_now_add=True |
| `updated_at` | DateTimeField | Last update timestamp | auto_now=True |

### Choices

#### PROPERTY_TYPES
- `apartment` - Apartment
- `house` - House
- `hotel` - Hotel Room
- `villa` - Villa
- `cabin` - Cabin
- `other` - Other

#### STATUS_CHOICES
- `active` - Active (visible and bookable)
- `inactive` - Inactive (hidden from listings)
- `pending` - Pending (awaiting approval)

### Methods

#### `__str__()`
Returns the listing title as string representation.

#### `average_rating()`
Calculates and returns the average overall rating from all reviews.
- Returns: `float` - Average rating or 0 if no reviews exist

### Meta Options

- **Ordering**: `-created_at` (newest first)

### Related Names

- `bookings` - All bookings for this listing (Booking model)
- `reviews` - All reviews for this listing (Review model)

---

## Booking Model

The `Booking` model represents a reservation made by a guest for a specific listing.

### Fields

#### References

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `listing` | ForeignKey | Reference to Listing | CASCADE delete, related_name='bookings' |
| `guest` | ForeignKey | Reference to User (booking guest) | CASCADE delete, related_name='bookings' |

#### Dates

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `check_in_date` | DateField | Check-in date | required |
| `check_out_date` | DateField | Check-out date | required |

#### Guests

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `number_of_adults` | PositiveIntegerField | Number of adult guests | default=1 |
| `number_of_children` | PositiveIntegerField | Number of children | default=0 |
| `number_of_infants` | PositiveIntegerField | Number of infants | default=0 |

#### Status

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `booking_status` | CharField | Current booking status | choices from STATUS_CHOICES, default='pending' |

#### Pricing

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `total_price` | DecimalField | Total booking cost | max_digits=10, decimal_places=2, required |
| `nights` | PositiveIntegerField | Number of nights | required |

#### Payment

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `payment_status` | CharField | Payment status | choices from PAYMENT_STATUS_CHOICES, default='pending' |
| `payment_method` | CharField | Payment method used | max_length=50, optional |

#### Additional Information

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `special_requests` | TextField | Guest special requests | optional |
| `confirmation_code` | CharField | Unique booking confirmation code | max_length=20, unique=True |

#### Cancellation

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `cancelled_at` | DateTimeField | Cancellation timestamp | optional |
| `cancellation_reason` | TextField | Reason for cancellation | optional |

#### Timestamps

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `created_at` | DateTimeField | Creation timestamp | auto_now_add=True |
| `updated_at` | DateTimeField | Last update timestamp | auto_now=True |

### Choices

#### STATUS_CHOICES
- `pending` - Pending (awaiting confirmation)
- `confirmed` - Confirmed (active booking)
- `cancelled` - Cancelled
- `completed` - Completed (stay finished)

#### PAYMENT_STATUS_CHOICES
- `pending` - Pending payment
- `paid` - Payment completed
- `refunded` - Payment refunded

### Methods

#### `__str__()`
Returns a string with confirmation code and listing title.

### Properties

#### `total_guests`
Calculates the total number of guests (adults + children + infants).
- Returns: `int` - Total guest count

### Meta Options

- **Ordering**: `-created_at` (newest first)

### Related Names

- `review` - Associated review for this booking (Review model)

---

## Review Model

The `Review` model represents guest feedback and ratings for a completed booking.

### Fields

#### References

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `listing` | ForeignKey | Reference to Listing | CASCADE delete, related_name='reviews' |
| `booking` | OneToOneField | Reference to Booking | CASCADE delete, related_name='review' |
| `reviewer` | ForeignKey | Reference to User (reviewer) | CASCADE delete, related_name='reviews' |

#### Ratings (1-5 Scale)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `overall_rating` | PositiveIntegerField | Overall experience rating | min=1, max=5 |
| `cleanliness_rating` | PositiveIntegerField | Cleanliness rating | min=1, max=5 |
| `accuracy_rating` | PositiveIntegerField | Listing accuracy rating | min=1, max=5 |
| `communication_rating` | PositiveIntegerField | Host communication rating | min=1, max=5 |
| `location_rating` | PositiveIntegerField | Location rating | min=1, max=5 |
| `value_rating` | PositiveIntegerField | Value for money rating | min=1, max=5 |
| `checkin_rating` | PositiveIntegerField | Check-in experience rating | min=1, max=5 |

#### Review Content

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `comment` | TextField | Written review text | required |

#### Host Response

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `host_response` | TextField | Host's response to review | optional |
| `host_response_date` | DateTimeField | Host response timestamp | optional |

#### Engagement

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `helpful_count` | PositiveIntegerField | Number of "helpful" votes | default=0 |
| `is_verified` | BooleanField | Verified review flag | default=True |

#### Timestamps

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `created_at` | DateTimeField | Creation timestamp | auto_now_add=True |
| `updated_at` | DateTimeField | Last update timestamp | auto_now=True |

### Methods

#### `__str__()`
Returns a string with reviewer username and listing title.

### Properties

#### `average_rating`
Calculates the average of all six category ratings (excluding overall_rating).
- Returns: `float` - Average of cleanliness, accuracy, communication, location, value, and check-in ratings

### Meta Options

- **Ordering**: `-created_at` (newest first)
- **Unique Together**: `['booking', 'reviewer']` - One review per booking per user

---

## Model Relationships

### Entity Relationship Diagram

```
User (Django Auth)
  |
  |-- (1:N) Listing (as host)
  |     |
  |     |-- (1:N) Booking
  |     |     |
  |     |     |-- (1:1) Review
  |     |
  |     |-- (1:N) Review
  |
  |-- (1:N) Booking (as guest)
  |
  |-- (1:N) Review (as reviewer)
```

### Relationship Details

1. **User → Listing (One-to-Many)**
   - A user (host) can have multiple listings
   - Each listing belongs to one host
   - Delete cascade: Deleting a user deletes all their listings

2. **Listing → Booking (One-to-Many)**
   - A listing can have multiple bookings
   - Each booking is for one listing
   - Delete cascade: Deleting a listing deletes all its bookings

3. **User → Booking (One-to-Many)**
   - A user (guest) can make multiple bookings
   - Each booking is made by one guest
   - Delete cascade: Deleting a user deletes all their bookings

4. **Booking → Review (One-to-One)**
   - Each booking can have one review
   - Each review is associated with one booking
   - Delete cascade: Deleting a booking deletes its review

5. **Listing → Review (One-to-Many)**
   - A listing can have multiple reviews
   - Each review is for one listing
   - Delete cascade: Deleting a listing deletes all its reviews

6. **User → Review (One-to-Many)**
   - A user can write multiple reviews
   - Each review is written by one user
   - Delete cascade: Deleting a user deletes all their reviews

---

## Usage Examples

### Creating a Listing

```python
from django.contrib.auth.models import User
from listings.models import Listing

host = User.objects.get(username='john_doe')
listing = Listing.objects.create(
    title='Cozy Beach House',
    description='Beautiful oceanfront property with stunning views',
    property_type='house',
    host=host,
    address='123 Ocean Drive',
    city='Miami',
    country='USA',
    base_price=150.00,
    max_guests=6,
    bedrooms=3,
    beds=4,
    bathrooms=2.5,
    amenities='WiFi, Pool, Kitchen, Parking',
    status='active'
)
```

### Creating a Booking

```python
from datetime import date
from listings.models import Booking
import secrets

guest = User.objects.get(username='jane_smith')
listing = Listing.objects.get(id=1)

booking = Booking.objects.create(
    listing=listing,
    guest=guest,
    check_in_date=date(2025, 12, 20),
    check_out_date=date(2025, 12, 27),
    number_of_adults=2,
    number_of_children=1,
    nights=7,
    total_price=1050.00,
    confirmation_code=secrets.token_hex(10).upper(),
    booking_status='confirmed',
    payment_status='paid'
)
```

### Creating a Review

```python
from listings.models import Review

review = Review.objects.create(
    listing=booking.listing,
    booking=booking,
    reviewer=guest,
    overall_rating=5,
    cleanliness_rating=5,
    accuracy_rating=5,
    communication_rating=4,
    location_rating=5,
    value_rating=4,
    checkin_rating=5,
    comment='Amazing property! Clean, spacious, and exactly as described.'
)
```

### Querying Data

```python
# Get all active listings in a city
miami_listings = Listing.objects.filter(city='Miami', status='active')

# Get all bookings for a user
user_bookings = Booking.objects.filter(guest__username='jane_smith')

# Get average rating for a listing
listing = Listing.objects.get(id=1)
avg_rating = listing.average_rating()

# Get all confirmed bookings for a listing
confirmed_bookings = listing.bookings.filter(booking_status='confirmed')

# Get reviews with rating above 4
high_rated = Review.objects.filter(overall_rating__gte=4)
```

---

## Database Considerations

### Indexes

Consider adding indexes for frequently queried fields:
- `Listing.city`, `Listing.country`, `Listing.status`
- `Booking.check_in_date`, `Booking.check_out_date`, `Booking.booking_status`
- `Review.overall_rating`, `Review.created_at`

### Data Validation

- Ensure `check_out_date` is after `check_in_date` in Booking model
- Validate that total guests doesn't exceed listing's `max_guests`
- Ensure reviews can only be created for completed bookings
- Validate that `base_price` and `total_price` are positive

### Future Enhancements

1. **Amenities**: Convert to separate Amenity model with Many-to-Many relationship
2. **Images**: Create separate Image model for multiple property photos
3. **Availability**: Add Calendar/Availability model to manage booking dates
4. **Pricing**: Implement dynamic pricing with seasonal rates
5. **Messages**: Add messaging system between hosts and guests
6. **Wishlists**: Allow users to save favorite listings

---

## Notes

- All timestamps are automatically managed by Django
- The `confirmation_code` should be generated uniquely for each booking
- Reviews enforce one review per booking per user through `unique_together`
- All cascade deletes maintain referential integrity
- Currency fields use DecimalField for precise calculations

---

**Last Updated**: November 30, 2025  
**Django Version**: 5.2.6  
**Python Version**: 3.x
