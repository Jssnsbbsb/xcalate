"""
Seed the Xcalate database with Manipur travel data.

Run: python manage.py seed_all
"""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from regions.models import Region
from places.models import Place
from homestays.models import Homestay
from marketplace.models import Listing

User = get_user_model()


# ============================================================
# REGIONS
# ============================================================
REGIONS = [
    {
        "slug": "imphal", "name": "Imphal",
        "description": "The capital of Manipur — home to Kangla Fort, Ema Keithel (Asia's largest all-women market), and the seat of Manipuri culture.",
        "cover_image": "https://picsum.photos/seed/imphal/1200/800",
        "latitude": 24.8170, "longitude": 93.9368, "zoom": 12, "size_mb": 2.5,
    },
    {
        "slug": "loktak", "name": "Loktak",
        "description": "Loktak Lake — the largest freshwater lake in Northeast India, famous for its floating phumdis and the world's only floating national park.",
        "cover_image": "https://picsum.photos/seed/loktak/1200/800",
        "latitude": 24.5500, "longitude": 93.8000, "zoom": 11, "size_mb": 1.8,
    },
    {
        "slug": "bishnupur", "name": "Bishnupur",
        "description": "Historic lake basin with WWII sites, eco-parks, and wetlands connecting to Loktak.",
        "cover_image": "https://picsum.photos/seed/bishnupur/1200/800",
        "latitude": 24.6167, "longitude": 93.7667, "zoom": 12, "size_mb": 1.5,
    },
    {
        "slug": "thoubal", "name": "Thoubal",
        "description": "Agricultural heartland of Manipur — site of the historic Khongjom War Memorial.",
        "cover_image": "https://picsum.photos/seed/thoubal/1200/800",
        "latitude": 24.6333, "longitude": 94.0167, "zoom": 12, "size_mb": 0.9,
    },
    {
        "slug": "ukhrul", "name": "Ukhrul",
        "description": "Hill town famous for the rare Shirui Lily that grows nowhere else on Earth, plus stunning Tangkhul Naga culture.",
        "cover_image": "https://picsum.photos/seed/ukhrul/1200/800",
        "latitude": 25.0500, "longitude": 94.3600, "zoom": 11, "size_mb": 1.2,
    },
    {
        "slug": "churachandpur", "name": "Churachandpur",
        "description": "Second-largest town in Manipur, known for vibrant tribal culture and the Thangjing Hill.",
        "cover_image": "https://picsum.photos/seed/churachandpur/1200/800",
        "latitude": 24.3333, "longitude": 93.6833, "zoom": 11, "size_mb": 1.0,
    },
    {
        "slug": "senapati", "name": "Senapati",
        "description": "Mountain district and gateway to Mao — lush pine forests and Mao Naga culture.",
        "cover_image": "https://picsum.photos/seed/senapati/1200/800",
        "latitude": 25.2667, "longitude": 94.0167, "zoom": 11, "size_mb": 0.9,
    },
    {
        "slug": "tamenglong", "name": "Tamenglong",
        "description": "Land of the Zeliangrong Nagas — famous for the Orange Festival, caves, and untouched forests.",
        "cover_image": "https://picsum.photos/seed/tamenglong/1200/800",
        "latitude": 24.9833, "longitude": 93.5000, "zoom": 11, "size_mb": 0.8,
    },
]


# ============================================================
# PLACES — Tourist Spots
# ============================================================
PLACES = [
    # ---- Tourist Spots ----
    {
        "name": "Loktak Lake", "category": "nature", "region": "loktak",
        "short_description": "Largest freshwater lake in Northeast India, famous for floating phumdis.",
        "description": "The largest freshwater lake in Northeast India, famous for its phumdis (floating islands of vegetation) and the world's only floating national park, Keibul Lamjao, which protects the endangered Sangai deer.",
        "latitude": 24.5500, "longitude": 93.7833,
        "address": "Moirang, Bishnupur District",
        "opening_hours": "08:00 AM - 06:00 PM (Daily)",
        "price_range": "budget", "tags": ["lake", "nature", "boating", "photography"],
        "rating": 4.8, "rating_count": 342, "is_featured": True,
    },
    {
        "name": "Kangla Fort", "category": "heritage", "region": "imphal",
        "short_description": "Ancient fortified palace of Manipuri kings, with historic moats and Kangla Sha guardians.",
        "description": "An ancient fortified palace that served as the traditional seat of power for the monarchs of Manipur, featuring historic moats, ramparts, and the sacred dragon-lion guardian statues called Kangla Sha.",
        "latitude": 24.8080, "longitude": 93.9420,
        "address": "Central Imphal",
        "opening_hours": "09:00 AM - 05:00 PM (Closed on Mondays)",
        "price_range": "budget", "tags": ["heritage", "fort", "history", "architecture"],
        "rating": 4.7, "rating_count": 218, "is_featured": True,
    },
    {
        "name": "Ema Keithel", "category": "market", "region": "imphal",
        "short_description": "Asia's largest all-women market, run exclusively by 5,000+ women traders.",
        "description": "Also known as the 'Mother's Market', it is a unique commercial hub completely managed and run exclusively by over 5,000 women traders, making it the largest all-women market in Asia.",
        "latitude": 24.8055, "longitude": 93.9388,
        "address": "Khwairamband Bazar, Imphal",
        "opening_hours": "04:00 AM - 09:00 PM (Daily)",
        "price_range": "budget", "tags": ["market", "shopping", "culture", "women"],
        "rating": 4.6, "rating_count": 187, "is_featured": True,
    },
    {
        "name": "Kangla Nongpok Thong", "category": "heritage", "region": "imphal",
        "short_description": "Historic eastern gate of Kangla Fort, reconstructed to fulfill an ancient prophecy of peace.",
        "description": "The historic Eastern Gate Bridge across the Imphal River, reconstructed to fulfill an ancient prophecy of peace. It serves as the primary auspicious pedestrian entrance to the fort complex.",
        "latitude": 24.8065, "longitude": 93.9490,
        "address": "New Checkon Road, Imphal East",
        "opening_hours": "05:00 AM - 09:00 PM (Daily)",
        "price_range": "budget", "tags": ["heritage", "spiritual", "riverfront"],
        "rating": 4.5, "rating_count": 92, "is_featured": False,
    },
    {
        "name": "Shri Govindajee Temple", "category": "temple", "region": "imphal",
        "short_description": "Majestic Hindu temple with twin gold-plated domes and Ras Leela performances.",
        "description": "A majestic Hindu temple dedicated to Lord Krishna and Radha, featuring a beautiful structure with two gold-plated domes and serving as a major center for cultural performances like the Ras Leela.",
        "latitude": 24.8020, "longitude": 93.9515,
        "address": "Palace Compound, Imphal",
        "opening_hours": "05:00 AM - 12:00 PM, 04:00 PM - 08:30 PM (Daily)",
        "price_range": "budget", "tags": ["temple", "spiritual", "culture"],
        "rating": 4.7, "rating_count": 156, "is_featured": True,
    },
    {
        "name": "Keibul Lamjao National Park", "category": "nature", "region": "loktak",
        "short_description": "The only floating national park in the world — last refuge of the Sangai deer.",
        "description": "The only floating national park in the entire world, consisting of thick floating mats of organic mass called phumdis. It is the last natural refuge of the critically endangered Sangai (brow-antlered deer).",
        "latitude": 24.5000, "longitude": 93.8500,
        "address": "Southern part of Loktak Lake, Bishnupur",
        "opening_hours": "07:30 AM - 05:30 PM (Closed on Mondays)",
        "price_range": "budget", "tags": ["wildlife", "national-park", "sangai", "nature"],
        "rating": 4.8, "rating_count": 203, "is_featured": True,
    },
    {
        "name": "RKCS Art Gallery and Museum", "category": "heritage", "region": "imphal",
        "short_description": "Private art museum with 200+ years of Manipuri history on canvas.",
        "description": "A stunning private art museum exhibiting the monumental works of late master artist Rajkumar C.S. Singh, capturing over 200 years of Manipuri history, culture, and mythology through oil paintings.",
        "latitude": 24.7950, "longitude": 93.9370,
        "address": "Keishamthong, Imphal",
        "opening_hours": "09:00 AM - 04:30 PM (Daily)",
        "price_range": "budget", "tags": ["art", "museum", "culture"],
        "rating": 4.6, "rating_count": 78, "is_featured": False,
    },
    {
        "name": "Joysana Retreat", "category": "nature", "region": "bishnupur",
        "short_description": "Tranquil eco-retreat with over-water wooden cottages against scenic hills.",
        "description": "A tranquil eco-retreat nestled against the backdrop of scenic hills and green paddy fields, featuring unique over-water wooden cottages, decorative lanterns, and an ornamental fish view pond.",
        "latitude": 24.7080, "longitude": 93.8240,
        "address": "Manda Hills, Oinam, near Nambol",
        "opening_hours": "09:00 AM - 06:00 PM (Daily for visitors)",
        "price_range": "mid", "tags": ["resort", "eco", "romantic", "lake"],
        "rating": 4.7, "rating_count": 124, "is_featured": True,
    },
    {
        "name": "ISKCON Imphal", "category": "temple", "region": "imphal",
        "short_description": "Serene Krishna temple with unique dome built from local materials.",
        "description": "A beautiful temple dedicated to Sri Sri Radha Krishnachandra, known for its unique dome architecture built with local materials and its highly serene, spiritually vibrant atmosphere.",
        "latitude": 24.7860, "longitude": 93.9180,
        "address": "Airport Road, Imphal",
        "opening_hours": "04:30 AM - 01:00 PM, 04:30 PM - 08:30 PM (Daily)",
        "price_range": "budget", "tags": ["temple", "spiritual", "krishna"],
        "rating": 4.8, "rating_count": 167, "is_featured": False,
    },
    {
        "name": "Sadu Chiru Waterfall", "category": "nature", "region": "imphal",
        "short_description": "Spectacular three-tiered waterfall, one of Manipur's most popular picnic spots.",
        "description": "A spectacular three-tiered perennial waterfall cascading down lush green hillsides, accessed via a well-maintained scenic uphill forest path. It is one of the most popular picnic spots in Manipur.",
        "latitude": 24.7414, "longitude": 93.7449,
        "address": "Bungte Chiru Village, Ichum Keirap, Kangpokpi",
        "opening_hours": "07:30 AM - 05:30 PM (Closed on Sundays)",
        "price_range": "budget", "tags": ["waterfall", "nature", "trekking", "picnic"],
        "rating": 4.7, "rating_count": 145, "is_featured": True,
    },
    {
        "name": "Manipur Zoological Garden", "category": "nature", "region": "imphal",
        "short_description": "The 'Jewel Box of Manipur' — home to rare Himalayan wildlife and Sangai breeding.",
        "description": "A wildlife park known as the 'Jewel Box of Manipur', home to a variety of rare Himalayan and Northeast Indian birds and animals, including a special captive breeding section for the Sangai deer.",
        "latitude": 24.8190, "longitude": 93.8960,
        "address": "Iroishemba, Imphal",
        "opening_hours": "10:00 AM - 04:00 PM (Closed on Mondays)",
        "price_range": "budget", "tags": ["zoo", "wildlife", "family"],
        "rating": 4.4, "rating_count": 98, "is_featured": False,
    },
    {
        "name": "Singda Dam", "category": "nature", "region": "imphal",
        "short_description": "The highest mud dam in the world, overlooking a serene turquoise reservoir.",
        "description": "The highest mud-dam in the world, overlooking a serene turquoise reservoir lake and surrounded by verdant hills. It is highly favored by locals for peaceful day picnics and morning treks.",
        "latitude": 24.8550, "longitude": 93.8150,
        "address": "Singda, approx. 16 km from Imphal",
        "opening_hours": "08:00 AM - 06:00 PM (Daily)",
        "price_range": "budget", "tags": ["dam", "nature", "picnic", "trekking"],
        "rating": 4.5, "rating_count": 112, "is_featured": False,
    },
    {
        "name": "Khongjom War Memorial Complex", "category": "monument", "region": "thoubal",
        "short_description": "Home of the world's tallest sword statue — honoring the 1891 Anglo-Manipur War martyrs.",
        "description": "A historic site honoring the valiant Manipuri soldiers who fought the British in the Anglo-Manipur War of 1891, featuring the world's tallest sword statue and a beautiful hilltop war memorial tower.",
        "latitude": 24.5710, "longitude": 94.0220,
        "address": "Khongjom, Indo-Myanmar Road, Thoubal",
        "opening_hours": "09:00 AM - 05:00 PM (Daily)",
        "price_range": "budget", "tags": ["war-memorial", "history", "monument"],
        "rating": 4.6, "rating_count": 86, "is_featured": False,
    },
    {
        "name": "Shirui Kashung", "category": "nature", "region": "ukhrul",
        "short_description": "Majestic peak — the only place on Earth where the Shirui Lily grows.",
        "description": "A majestic peak famous as the exclusive natural habitat of the rare, seasonal Shirui Lily (Lilium mackliniae) which grows nowhere else in the world, offering sweeping panoramic views of the surrounding hills.",
        "latitude": 25.1200, "longitude": 94.4600,
        "address": "Shirui Village, Ukhrul",
        "opening_hours": "06:00 AM - 04:00 PM (Daily)",
        "price_range": "budget", "tags": ["peak", "trekking", "flower", "nature"],
        "rating": 4.9, "rating_count": 176, "is_featured": True,
    },
    {
        "name": "Matai Garden", "category": "nature", "region": "imphal",
        "short_description": "Peaceful botanical garden with manicured Duranta shrub structures.",
        "description": "Also known as the Ibudhou Asheiningthou Garden, this peaceful botanical landscape is famous for its neatly manicured structures of Duranta shrubs and clean cemented walkways perfect for strolls.",
        "latitude": 24.8614, "longitude": 93.9166,
        "address": "Matai Mamang Leikai, Imphal East",
        "opening_hours": "09:00 AM - 05:00 PM (Closed on Weekends)",
        "price_range": "budget", "tags": ["garden", "botanical", "walk", "family"],
        "rating": 4.4, "rating_count": 64, "is_featured": False,
    },
    {
        "name": "Loukoi Pat Lake", "category": "nature", "region": "bishnupur",
        "short_description": "Picturesque small lake with boating, eco-park, and fish-feeding decks.",
        "description": "A picturesque, small lake tucked inside a crescent of green hills, featuring boating facilities, a beautifully maintained eco-park, and fish feeding decks popular with weekend family travelers.",
        "latitude": 24.7090, "longitude": 93.8360,
        "address": "Nambol, Bishnupur",
        "opening_hours": "09:00 AM - 06:00 PM (Daily)",
        "price_range": "budget", "tags": ["lake", "boating", "family", "eco-park"],
        "rating": 4.3, "rating_count": 72, "is_featured": False,
    },
    {
        "name": "Maibam Lokpa Ching", "category": "heritage", "region": "bishnupur",
        "short_description": "WWII battlefield known as 'Red Hill' — a solemn war memorial.",
        "description": "Also known as Red Hill, this historic hillock was the site of a fierce battle between the British and the Japanese Allied Forces during World War II, marked today by a solemn memorial monument.",
        "latitude": 24.7060, "longitude": 93.8440,
        "address": "Red Hill, Nambol, Bishnupur",
        "opening_hours": "09:00 AM - 05:00 PM (Daily)",
        "price_range": "budget", "tags": ["war-site", "history", "wwii", "memorial"],
        "rating": 4.5, "rating_count": 58, "is_featured": False,
    },
    {
        "name": "Imphal Peace Museum", "category": "heritage", "region": "bishnupur",
        "short_description": "Modern museum commemorating the 75th anniversary of the Battle of Imphal.",
        "description": "A modern museum built to commemorate the 75th anniversary of the Battle of Imphal (WWII), displaying authentic war battlefield relics, weaponry, personal diaries, and stories of local reconciliation.",
        "latitude": 24.7065, "longitude": 93.8435,
        "address": "Foot of Red Hill, Nambol, Bishnupur",
        "opening_hours": "09:30 AM - 05:00 PM (Closed on Mondays)",
        "price_range": "budget", "tags": ["museum", "history", "wwii"],
        "rating": 4.6, "rating_count": 94, "is_featured": False,
    },
]


# ============================================================
# RESTAURANTS (added as Places with category="restaurant")
# Format: (name, avg_cost_inr, area, lat, lng, hours, short_desc)
# ============================================================
RESTAURANTS = [
    ("Forage Restaurant", 800, "Gadon Complex, Thangmeiband", 24.8192, 93.9352, "11:30 AM - 10:00 PM", "Fine dining with Mediterranean-Manipuri fusion, farm-to-table approach, and eco-chic interiors."),
    ("Leirung Resto", 600, "Uripok Tourangbam Leikai", 24.8125, 93.9214, "12:00 PM - 09:30 PM", "Modern multi-cuisine family restaurant with impeccable service and family-friendly ambiance."),
    ("SomeWhere Cafe & Restaurant", 400, "Opposite Standard College, Kongba", 24.7951, 93.9634, "11:00 AM - 08:30 PM", "Cozy boutique cafe known for minimalist architecture, artisanal coffees, and clean continental platters."),
    ("Harvest Cafe x Kitchen", 500, "Lamphelpat, Near Shija Hospitals", 24.8258, 93.9189, "10:30 AM - 09:00 PM", "Organic bistro sourcing local farm produce — premium salads, fresh juices, and health-focused food."),
    ("Hao Naga Kitchen", 700, "Chingmeirong, Near Asker Ali Petrol Pump", 24.8272, 93.9431, "11:30 AM - 09:30 PM", "Authentic Naga cuisine — smoked meat platters and fiery tribal delicacies in an upscale setting."),
    ("Le Zara Imphal", 900, "Thangmeiband, Imphal", 24.8185, 93.9348, "12:00 PM - 10:00 PM", "Premier Asian-fusion hotspot famous for dim sums, sushi, and elite contemporary ambiance."),
    ("Timber Cafe Imphal", 450, "Porompat, Near JNIMS", 24.8055, 93.9575, "11:00 AM - 09:00 PM", "Rooftop lounge with wooden aesthetics, city skyline views, and excellent mocktails and short-eats."),
    ("Classic Cafe", 1200, "The Classic Hotel, North AOC", 24.8130, 93.9470, "06:30 AM - 10:30 PM", "Prestigious 3-star ISO-certified dining hall with luxury buffet spreads and global multi-cuisine."),
    ("Uncle Ugen's Momo", 350, "Thangmeiband Lilasing Khongnangkhong", 24.8220, 93.9375, "11:30 AM - 08:30 PM", "Cozy dining nook serving authentic Tibetan and Sikkimese street food and Himalayan momos."),
    ("De Avenue Cafe", 500, "New Checkon Road", 24.8012, 93.9535, "10:00 AM - 09:00 PM", "Elegant espresso bistro with premium blends, top-tier baked desserts, and impeccable ambiance."),
    ("The Lux Cafe", 400, "Paona Bazar", 24.8035, 93.9390, "09:00 AM - 08:00 PM", "Air-conditioned luxury lounge with French pastries, global teas, and unmatched cleanliness."),
    ("Flavours - Classic Grande", 1500, "Hotel Classic Grande, Chingmeirong", 24.8315, 93.9485, "06:00 AM - 11:00 PM", "Manipur's peak luxury dining — elite pan-Indian and European delicacies in a lavish environment."),
    ("The Noodle House", 500, "Kwakeithel, Tiddim Road", 24.7820, 93.9245, "11:00 AM - 09:00 PM", "Contemporary pan-Asian diner with high-pressure steam kitchens serving flavorful noodles and stir-fries."),
    ("Sosa's Kitchen", 450, "Kakwa, Indo-Burma Road", 24.7640, 93.9355, "11:00 AM - 08:30 PM", "Boutique healthy diner focusing on premium health foods and organic plates with zero additives."),
    ("Sosa Cafe x Resto", 500, "Sagolband Moirang Leirak", 24.8010, 93.9180, "11:00 AM - 09:00 PM", "High-end modern bistro with spotless minimalist interiors and global snacks and signature mocktails."),
    ("Zaika Restaurant", 750, "Minuthong, Imphal", 24.8142, 93.9450, "12:00 PM - 10:00 PM", "Premium Awadhi and Mughlai — gourmet kebabs and biryanis in a pristine royal-themed hall."),
    ("Imphal Coffee House", 300, "Palace Compound Road", 24.8020, 93.9490, "08:00 AM - 09:00 PM", "Heritage artisanal coffee spot blending old architecture with modern brewing and local savories."),
    ("ManiBaking Co.", 350, "Singjamei Bazaar", 24.7735, 93.9330, "09:30 AM - 08:30 PM", "Premium artisanal patisserie — elite custom cakes, macaroons, and European breads."),
    ("Bake My Day", 400, "Lamlong Bazaar", 24.8210, 93.9610, "10:00 AM - 08:30 PM", "Modern dessert parlour specializing in waffles, pancakes, and gourmet milkshakes."),
    ("Roof Top Cafe - Sangai Continental", 800, "Thangal Bazar", 24.8075, 93.9370, "11:00 AM - 09:30 PM", "Elite rooftop dining with panoramic city views and premium Chinese and Indian cuisine."),
    ("Meitei Chakhum", 300, "Kwakeithel Bazaar", 24.7830, 93.9250, "11:00 AM - 04:00 PM, 06:00 PM - 09:00 PM", "The most hygienic destination for traditional Manipuri 'Chak-luk' (thali) served on bell-metal plates."),
    ("Hot Bite Imphal", 450, "Uripok Achom Leikai", 24.8110, 93.9230, "10:30 AM - 09:00 PM", "Premium fast-casual with transparent stainless-steel kitchen — burgers, pizzas, and fried chicken."),
    ("Brew & Bite", 400, "Langol Road", 24.8290, 93.9160, "11:00 AM - 09:00 PM", "Container-themed cafe with open-air garden, specialty drip coffees, and artisanal sandwiches."),
    ("The Urban Kitchen", 650, "Mantripukhri, National Highway 2", 24.8450, 93.9520, "11:30 AM - 09:30 PM", "Premium highway diner with grand contemporary layouts and highly rated Indian-Chinese dishes."),
    ("Chili's Imphal Bistro", 700, "Lamphelpat Supermarket", 24.8215, 93.9205, "11:00 AM - 09:30 PM", "Modern western bistro famous for sizzling fajitas, perfectly grilled steaks, and Tex-Mex fare."),
    ("The Olive Garden Resto", 750, "Airport Road, Ghari", 24.7690, 93.9020, "11:00 AM - 09:30 PM", "Open-lawn garden restaurant near the airport with multi-cuisine platters and peaceful ambiance."),
    ("The Yellow Chilli Imphal", 900, "North AOC Flyover Corner", 24.8150, 93.9465, "12:00 PM - 10:30 PM", "Celebrity-chef franchise serving exquisite master-crafted Indian curries and signature drinks."),
    ("Waffle & Co.", 300, "Keishampat Junction", 24.7965, 93.9350, "11:00 AM - 09:00 PM", "Bright pastel-themed dessert bar specializing in fresh bubble waffles and premium gelato."),
    ("Ningthou Traditional Dining", 600, "Palace Compound, Near Kangla Gate", 24.8015, 93.9510, "11:30 AM - 09:30 PM", "Elite cultural dining space merging luxury with historical Meitei hospitality and royal feasts."),
    ("The Corner Cafe", 450, "Lalambung Makhong", 24.8140, 93.9295, "09:00 AM - 09:00 PM", "Premium boutique cafe with top-tier water purification lines and exceptional gourmet pastries."),
]


# ============================================================
# HOMESTAYS (sample curated data — attach to seller)
# ============================================================
HOMESTAYS = [
    {
        "slug": "lakeside-homestay-loktak",
        "title": "Lakeside Homestay near Loktak",
        "description": "Cozy family-run homestay with stunning views of Loktak Lake. Wake up to phumdis floating past your window and enjoy home-cooked Manipuri meals by the water.",
        "region": "loktak", "address": "Thanga Village, Bishnupur",
        "latitude": 24.5500, "longitude": 93.8000,
        "price_per_night": 1500, "max_guests": 4, "bedrooms": 2, "beds": 3, "bathrooms": 1,
        "amenities": ["wifi", "meals_included", "parking", "hot_water"],
        "rating": 4.8, "rating_count": 23,
    },
    {
        "slug": "imphal-heritage-homestay",
        "title": "Imphal Heritage Homestay",
        "description": "Restored traditional Manipuri house in the heart of Imphal. Walk to Kangla Fort and Ema Keithel in minutes.",
        "region": "imphal", "address": "Palace Compound, Imphal",
        "latitude": 24.8080, "longitude": 93.9450,
        "price_per_night": 2000, "max_guests": 6, "bedrooms": 3, "beds": 4, "bathrooms": 2,
        "amenities": ["wifi", "kitchen", "parking", "ac"],
        "rating": 4.7, "rating_count": 41,
    },
    {
        "slug": "ukhrul-hilltop-homestay",
        "title": "Ukhrul Hilltop Homestay",
        "description": "Wooden cottage on a hilltop with panoramic views of the Shirui Hills. Perfect for trekkers and nature lovers.",
        "region": "ukhrul", "address": "Shirui Village, Ukhrul",
        "latitude": 25.1200, "longitude": 94.4600,
        "price_per_night": 1200, "max_guests": 3, "bedrooms": 1, "beds": 2, "bathrooms": 1,
        "amenities": ["meals_included", "hot_water", "bonfire"],
        "rating": 4.9, "rating_count": 18,
    },
    {
        "slug": "bishnupur-eco-stay",
        "title": "Bishnupur Eco Stay",
        "description": "Eco-friendly bamboo cottage surrounded by paddy fields, close to Red Hill and Loktak Lake.",
        "region": "bishnupur", "address": "Nambol, Bishnupur",
        "latitude": 24.7100, "longitude": 93.8400,
        "price_per_night": 1000, "max_guests": 4, "bedrooms": 2, "beds": 3, "bathrooms": 1,
        "amenities": ["meals_included", "bicycle", "garden"],
        "rating": 4.6, "rating_count": 15,
    },
    {
        "slug": "thoubal-farm-stay",
        "title": "Thoubal Farm Stay",
        "description": "Working organic farm where guests help with harvest and cook traditional Manipuri dishes.",
        "region": "thoubal", "address": "Khongjom, Thoubal",
        "latitude": 24.6000, "longitude": 94.0200,
        "price_per_night": 900, "max_guests": 5, "bedrooms": 2, "beds": 3, "bathrooms": 1,
        "amenities": ["meals_included", "farm_tour", "parking"],
        "rating": 4.5, "rating_count": 11,
    },
]


# ============================================================
# MARKETPLACE LISTINGS (products + services)
# ============================================================
LISTINGS = [
    {
        "type": "product", "title": "Handwoven Manipuri Phanek",
        "short_description": "Traditional wrap-around skirt woven by Imphal artisans",
        "description": "Authentic handwoven Phanek (Manipuri wrap-around skirt) using traditional motifs. Pure cotton, natural dyes, 2m x 1m. Each piece takes 3 days to weave.",
        "price": 1800, "price_unit": "per item",
        "region": "imphal", "category": "textile",
    },
    {
        "type": "product", "title": "Manipuri Black Rice (Chak-hao) — 1kg",
        "short_description": "Premium organic black rice from Manipur's wetlands",
        "description": "Chak-hao is a unique black rice grown in Manipur. Rich in antioxidants, with a nutty flavor. Perfect for kheer and salads. 1kg vacuum-sealed pack.",
        "price": 350, "price_unit": "per kg",
        "region": "imphal", "category": "food",
    },
    {
        "type": "product", "title": "Handcrafted Bamboo Basket Set",
        "short_description": "Set of 3 traditional Manipuri bamboo baskets",
        "description": "Handwoven bamboo baskets made by local artisans. Set of 3 in nesting sizes. Eco-friendly, durable, food-safe.",
        "price": 850, "price_unit": "per set",
        "region": "imphal", "category": "handicraft",
    },
    {
        "type": "product", "title": "Manipuri Handloom Silk Shawl",
        "short_description": "Luxurious silk shawl with traditional motifs",
        "description": "Pure mulberry silk shawl handwoven in Imphal. Features traditional Manipuri motifs and vibrant natural dyes. Perfect gift.",
        "price": 3500, "price_unit": "per item",
        "region": "imphal", "category": "textile",
    },
    {
        "type": "product", "title": "Handmade Tribal Beaded Necklace",
        "short_description": "Traditional Naga-style beaded jewelry",
        "description": "Handcrafted beaded necklace inspired by Tangkhul Naga designs. Made with glass beads and brass. Each piece is unique.",
        "price": 650, "price_unit": "per item",
        "region": "ukhrul", "category": "jewelry",
    },
    {
        "type": "service", "title": "Guided Heritage Tour of Kangla Fort",
        "short_description": "3-hour guided walking tour with local historian",
        "description": "Explore Kangla Fort with a local historian who brings its 2000-year history to life. Includes entry tickets and refreshments.",
        "price": 1200, "price_unit": "per person",
        "region": "imphal", "category": "guide",
    },
    {
        "type": "service", "title": "Manipuri Classical Dance Workshop",
        "short_description": "2-hour hands-on workshop with a Ras Leela performer",
        "description": "Learn the basics of Manipuri classical dance from a professional Ras Leela performer. Includes costume trial. Great for culture enthusiasts.",
        "price": 800, "price_unit": "per person",
        "region": "imphal", "category": "workshop",
    },
    {
        "type": "service", "title": "Loktak Lake Sunrise Boat Tour",
        "short_description": "Sunrise boat ride through phumdis with photographer",
        "description": "Early-morning boat tour of Loktak Lake with a local guide who knows the best photo spots. Includes tea and snacks.",
        "price": 1500, "price_unit": "per person",
        "region": "loktak", "category": "guide",
    },
    {
        "type": "service", "title": "Pottery Workshop with Local Artisan",
        "short_description": "Learn traditional Manipuri pottery in 3 hours",
        "description": "Hands-on pottery workshop with a 3rd-generation Manipuri potter. Take home your creation. All materials included.",
        "price": 1000, "price_unit": "per person",
        "region": "imphal", "category": "workshop",
    },
    {
        "type": "service", "title": "Traditional Manipuri Cooking Class",
        "short_description": "Cook Eromba, Chamthong & Singju with a local chef",
        "description": "Learn to cook 3 iconic Manipuri dishes: Eromba (fermented fish curry), Chamthong (vegetable stew), and Singju (spicy salad). Includes market visit.",
        "price": 1800, "price_unit": "per person",
        "region": "imphal", "category": "workshop",
    },
]


class Command(BaseCommand):
    help = "Seed the database with all Manipur travel data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n🌱 Seeding Xcalate database...\n"))

        self.seed_regions()
        self.seed_places()
        self.seed_users()
        self.seed_homestays()
        self.seed_marketplace()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("✅ ALL DONE — Xcalate is ready to demo!"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write("")
        self.stdout.write(f"   Regions:      {Region.objects.count()}")
        self.stdout.write(f"   Places:       {Place.objects.count()}")
        self.stdout.write(f"   Restaurants:  {Place.objects.filter(category='restaurant').count()}")
        self.stdout.write(f"   Homestays:    {Homestay.objects.count()}")
        self.stdout.write(f"   Listings:     {Listing.objects.count()}")
        self.stdout.write(f"   Users:        {User.objects.count()}")
        self.stdout.write("")

    # --------------------------------------------------------
    def seed_regions(self):
        self.stdout.write(self.style.HTTP_INFO("📍 Seeding regions..."))
        created = updated = 0
        for data in REGIONS:
            obj, was_created = Region.objects.update_or_create(
                slug=data["slug"], defaults=data
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(f"   ✅ {created} created, {updated} updated")

    # --------------------------------------------------------
    def seed_places(self):
        self.stdout.write(self.style.HTTP_INFO("🏛️  Seeding places..."))

        # Tourist spots
        created = updated = 0
        for data in PLACES:
            slug = slugify(data["name"])
            defaults = {**data, "slug": slug, "images": [f"https://picsum.photos/seed/{slug}/1200/800"]}
            obj, was_created = Place.objects.update_or_create(slug=slug, defaults=defaults)
            if was_created:
                created += 1
            else:
                updated += 1

        # Restaurants
        r_created = 0
        for (name, cost, area, lat, lng, hours, desc) in RESTAURANTS:
            slug = slugify(name)
            if cost < 400:
                price_range = "budget"
            elif cost < 800:
                price_range = "mid"
            else:
                price_range = "premium"

            defaults = {
                "name": name, "category": "restaurant", "region": "imphal",
                "short_description": desc[:280], "description": desc,
                "images": [f"https://picsum.photos/seed/{slug}/1200/800"],
                "latitude": lat, "longitude": lng, "address": area,
                "opening_hours": hours, "price_range": price_range,
                "tags": ["food", "restaurant", "manipur"],
                "rating": round(4.2 + (hash(slug) % 8) / 10, 1),
                "rating_count": 20 + (hash(slug) % 200),
                "is_featured": cost >= 700,
            }
            _, was_created = Place.objects.update_or_create(slug=slug, defaults=defaults)
            if was_created:
                r_created += 1

        self.stdout.write(f"   ✅ {created} tourist spots created ({updated} updated)")
        self.stdout.write(f"   ✅ {r_created} restaurants created")

    # --------------------------------------------------------
    def seed_users(self):
        self.stdout.write(self.style.HTTP_INFO("👤 Seeding test users..."))

        # Seller
        if not User.objects.filter(username="ramesh").exists():
            User.objects.create_user(
                username="ramesh", email="ramesh@xcalate.com",
                password="Test@1234", role="local",
                phone="+919999999999", region="imphal",
                business_name="Ramesh Handicrafts",
            )
            self.stdout.write("   ✅ Created seller: ramesh / Test@1234")
        else:
            self.stdout.write("   🔄 Seller ramesh already exists")

        # Tourist
        if not User.objects.filter(username="adish").exists():
            User.objects.create_user(
                username="adish", email="adish@xcalate.com",
                password="Test@1234", role="tourist",
                phone="+918888888888",
            )
            self.stdout.write("   ✅ Created tourist: adish / Test@1234")
        else:
            self.stdout.write("   🔄 Tourist adish already exists")

    # --------------------------------------------------------
    def seed_homestays(self):
        self.stdout.write(self.style.HTTP_INFO("🏠 Seeding homestays..."))
        seller = User.objects.get(username="ramesh")

        created = 0
        for data in HOMESTAYS:
            defaults = {
                **data,
                "host_name": "Ramesh",
                "host_phone": "+919999999999",
                "host_email": "ramesh@xcalate.com",
                "user": seller,
                "images": [f"https://picsum.photos/seed/{data['slug']}/1200/800"],
                "is_active": True,
            }
            _, was_created = Homestay.objects.update_or_create(
                slug=data["slug"], defaults=defaults
            )
            if was_created:
                created += 1
        self.stdout.write(f"   ✅ {created} homestays created")

    # --------------------------------------------------------
    def seed_marketplace(self):
        self.stdout.write(self.style.HTTP_INFO("🛒 Seeding marketplace listings..."))
        seller = User.objects.get(username="ramesh")

        created = 0
        for data in LISTINGS:
            slug = slugify(data["title"])
            defaults = {
                **data,
                "slug": slug,
                "user": seller,
                "contact_phone": "+919999999999",
                "contact_email": "ramesh@xcalate.com",
                "whatsapp": "+919999999999",
                "images": [f"https://picsum.photos/seed/{slug}/1200/800"],
                "is_active": True,
                "is_featured": False,
                "view_count": 0,
            }
            _, was_created = Listing.objects.update_or_create(slug=slug, defaults=defaults)
            if was_created:
                created += 1
        self.stdout.write(f"   ✅ {created} listings created")