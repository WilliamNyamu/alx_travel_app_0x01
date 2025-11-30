from django.db import models

# Create your models here.
# Create models: Listing, Booking, Review
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Listing(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('hotel', 'Hotel Room'),
        ('villa', 'Villa'),
        ('cabin', 'Cabin'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    
    # Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Capacity
    max_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bedrooms = models.PositiveIntegerField(default=1)
    beds = models.PositiveIntegerField(default=1)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    
    # Amenities (using simple text field; could be many-to-many with Amenity model)
    amenities = models.TextField(help_text="Comma-separated amenities", blank=True)
    
    # House Rules
    check_in_time = models.TimeField(default='15:00')
    check_out_time = models.TimeField(default='11:00')
    cancellation_policy = models.CharField(max_length=50, default='flexible')
    smoking_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    
    # Images (simplified; could be separate Image model)
    main_image = models.URLField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_available = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([review.overall_rating for review in reviews]) / len(reviews)
        return 0


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    # References
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    
    # Dates
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    
    # Guests
    number_of_adults = models.PositiveIntegerField(default=1)
    number_of_children = models.PositiveIntegerField(default=0)
    number_of_infants = models.PositiveIntegerField(default=0)
    
    # Status
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    nights = models.PositiveIntegerField()
    
    # Payment
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Additional
    special_requests = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=20, unique=True)
    
    # Cancellation
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Booking {self.confirmation_code} - {self.listing.title}"
    
    @property
    def total_guests(self):
        return self.number_of_adults + self.number_of_children + self.number_of_infants


class Review(models.Model):
    # References
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    # Ratings (1-5 scale)
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    accuracy_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    checkin_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Review Content
    comment = models.TextField()
    
    # Host Response
    host_response = models.TextField(blank=True)
    host_response_date = models.DateTimeField(null=True, blank=True)
    
    # Engagement
    helpful_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['booking', 'reviewer']  # One review per booking per user
        
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.listing.title}"
    
    @property
    def average_rating(self):
        return (
            self.cleanliness_rating + 
            self.accuracy_rating + 
            self.communication_rating + 
            self.location_rating + 
            self.value_rating + 
            self.checkin_rating
        ) / 6