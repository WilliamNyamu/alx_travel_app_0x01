from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone
import uuid

fake = Faker()

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, default=10, help='Number of records to create')

    def handle(self, *args, **options):
        number = options['number']
        
        self.stdout.write('Seeding Users...')
        users = []
        for _ in range(number):
            user = User.objects.create_user(
                username=fake.user_name() + str(random.randint(1, 9999)),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='password123'
            )
            users.append(user)
        
        self.stdout.write('Seeding Listings...')
        listings = []
        property_types = ['apartment', 'house', 'hotel', 'villa', 'cabin']
        for _ in range(number):
            listing = Listing.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=500),
                property_type=random.choice(property_types),
                host=random.choice(users),
                address=fake.street_address(),
                city=fake.city(),
                country=fake.country(),
                neighborhood=fake.city_suffix(),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                base_price=random.randint(50, 500),
                max_guests=random.randint(1, 8),
                bedrooms=random.randint(1, 5),
                beds=random.randint(1, 6),
                bathrooms=random.randint(1, 3),
                amenities='wifi,kitchen,parking,pool',
                smoking_allowed=random.choice([True, False]),
                pets_allowed=random.choice([True, False]),
                main_image=fake.image_url(),
                status='active',
                is_available=True
            )
            listings.append(listing)
        
        self.stdout.write('Seeding Bookings...')
        bookings = []
        for _ in range(number):
            check_in = timezone.now().date() + timedelta(days=random.randint(1, 60))
            check_out = check_in + timedelta(days=random.randint(2, 14))
            nights = (check_out - check_in).days
            listing = random.choice(listings)
            
            booking = Booking.objects.create(
                listing=listing,
                guest=random.choice(users),
                check_in_date=check_in,
                check_out_date=check_out,
                number_of_adults=random.randint(1, 4),
                number_of_children=random.randint(0, 2),
                number_of_infants=random.randint(0, 1),
                booking_status='completed',
                nights=nights,
                total_price=listing.base_price,
                payment_status='paid',
                confirmation_code=str(uuid.uuid4())[:8].upper()
            )
            bookings.append(booking)
        
        self.stdout.write('Seeding Reviews...')
        for booking in bookings:
            Review.objects.create(
                listing=booking.listing,
                booking=booking,
                reviewer=booking.guest,
                overall_rating=random.randint(3, 5),
                cleanliness_rating=random.randint(3, 5),
                accuracy_rating=random.randint(3, 5),
                communication_rating=random.randint(3, 5),
                location_rating=random.randint(3, 5),
                value_rating=random.randint(3, 5),
                checkin_rating=random.randint(3, 5),
                comment=fake.text(max_nb_chars=200),
                is_verified=True
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {number} records!'))