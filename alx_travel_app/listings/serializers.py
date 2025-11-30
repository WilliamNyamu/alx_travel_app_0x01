from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ListingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing lists"""
    host = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'property_type', 'city', 'country',
            'base_price', 'max_guests', 'bedrooms',
            'bathrooms', 'main_image', 'average_rating', 
            'review_count', 'host', 'is_available'
        ]
        read_only_fields = ['id', 'average_rating', 'review_count']
    
    def get_average_rating(self, obj):
        return obj.average_rating()
    
    def get_review_count(self, obj):
        return obj.reviews.count()


class ListingDetailSerializer(serializers.ModelSerializer):
    """Full serializer for listing details"""
    host = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    amenities_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'host',
            'address', 'city', 'country', 'neighborhood', 
            'latitude', 'longitude', 'base_price', 'max_guests', 'bedrooms',
            'beds', 'bathrooms', 'amenities', 'amenities_list',
            'check_in_time', 'check_out_time', 'cancellation_policy',
            'smoking_allowed', 'pets_allowed', 'main_image', 'status',
            'is_available', 'average_rating', 'review_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'host', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        return round(obj.average_rating(), 2)
    
    def get_review_count(self, obj):
        return obj.reviews.count()
    
    def get_amenities_list(self, obj):
        if obj.amenities:
            return [amenity.strip() for amenity in obj.amenities.split(',')]
        return []


class ListingCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating listings"""
    
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'property_type', 'address', 
            'city', 'country', 'neighborhood', 'latitude', 'longitude',
            'base_price', 'max_guests', 'bedrooms', 'beds', 'bathrooms', 'amenities',
            'check_in_time', 'check_out_time', 'cancellation_policy',
            'smoking_allowed', 'pets_allowed', 'main_image', 'status',
            'is_available'
        ]
    
    def validate_base_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Base price must be greater than 0")
        return value
    
    def validate(self, data):
        if data.get('max_guests', 0) < 1:
            raise serializers.ValidationError("Must accommodate at least 1 guest")
        return data


class BookingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for booking lists"""
    listing = ListingListSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    total_guests = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'guest', 'check_in_date', 'check_out_date',
            'total_guests', 'booking_status', 'total_price', 'nights',
            'confirmation_code', 'created_at'
        ]
        read_only_fields = ['id', 'confirmation_code', 'created_at']


class BookingDetailSerializer(serializers.ModelSerializer):
    """Full serializer for booking details"""
    listing = ListingDetailSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    total_guests = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'guest', 'check_in_date', 'check_out_date',
            'number_of_adults', 'number_of_children', 'number_of_infants',
            'total_guests', 'booking_status', 'total_price', 'nights',
            'payment_status', 'payment_method', 'special_requests',
            'confirmation_code', 'cancelled_at', 'cancellation_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'confirmation_code', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""
    listing_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'listing_id', 'check_in_date', 'check_out_date',
            'number_of_adults', 'number_of_children', 'number_of_infants',
            'special_requests'
        ]
    
    def validate(self, data):
        # Check if check-out is after check-in
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )
        
        # Check if listing exists and is available
        try:
            listing = Listing.objects.get(id=data['listing_id'])
            if not listing.is_available:
                raise serializers.ValidationError("This listing is not available")
        except Listing.DoesNotExist:
            raise serializers.ValidationError("Listing not found")
        
        # Check guest capacity
        total_guests = (
            data.get('number_of_adults', 0) + 
            data.get('number_of_children', 0) + 
            data.get('number_of_infants', 0)
        )
        if total_guests > listing.max_guests:
            raise serializers.ValidationError(
                f"Too many guests. Maximum is {listing.max_guests}"
            )
        
        return data
    
    def create(self, validated_data):
        listing_id = validated_data.pop('listing_id')
        listing = Listing.objects.get(id=listing_id)
        
        # Calculate nights and total price
        check_in = validated_data['check_in_date']
        check_out = validated_data['check_out_date']
        nights = (check_out - check_in).days
        total_price = (
            listing.base_price * nights + 
            listing.cleaning_fee + 
            listing.service_fee
        )
        
        # Generate confirmation code
        import uuid
        confirmation_code = str(uuid.uuid4())[:8].upper()
        
        booking = Booking.objects.create(
            listing=listing,
            guest=self.context['request'].user,
            nights=nights,
            total_price=total_price,
            confirmation_code=confirmation_code,
            **validated_data
        )
        
        return booking


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews"""
    reviewer = UserSerializer(read_only=True)
    listing = ListingListSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'listing', 'booking', 'reviewer', 'overall_rating',
            'cleanliness_rating', 'accuracy_rating', 'communication_rating',
            'location_rating', 'value_rating', 'checkin_rating',
            'average_rating', 'comment', 'host_response',
            'host_response_date', 'helpful_count', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'reviewer', 'host_response', 'host_response_date',
            'helpful_count', 'is_verified', 'created_at', 'updated_at'
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reviews"""
    booking_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = [
            'booking_id', 'overall_rating', 'cleanliness_rating',
            'accuracy_rating', 'communication_rating', 'location_rating',
            'value_rating', 'checkin_rating', 'comment'
        ]
    
    def validate_booking_id(self, value):
        # Check if booking exists and belongs to user
        try:
            booking = Booking.objects.get(id=value)
            if booking.guest != self.context['request'].user:
                raise serializers.ValidationError("This is not your booking")
            if booking.booking_status != 'completed':
                raise serializers.ValidationError("Can only review completed bookings")
            if hasattr(booking, 'review'):
                raise serializers.ValidationError("You already reviewed this booking")
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking not found")
        
        return value
    
    def create(self, validated_data):
        booking_id = validated_data.pop('booking_id')
        booking = Booking.objects.get(id=booking_id)
        
        review = Review.objects.create(
            booking=booking,
            listing=booking.listing,
            reviewer=self.context['request'].user,
            **validated_data
        )
        
        return review


class HostResponseSerializer(serializers.Serializer):
    """Serializer for host responding to reviews"""
    host_response = serializers.CharField(max_length=1000)
    
    def validate(self, data):
        review = self.instance
        if review.listing.host != self.context['request'].user:
            raise serializers.ValidationError("Only the host can respond")
        return data