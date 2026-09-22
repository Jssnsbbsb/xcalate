"""
Seed the marketplace with 30 real Manipur artisans + 5 services.
Source: Manipur Cultural Products & Artisans Directory.

Run: python manage.py seed_marketplace
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from marketplace.models import Listing

User = get_user_model()


# Format: (title, category, region, price_inr, unit, contact_phone, desc)
PRODUCTS = [
    # ---------------- HANDLOOM / TEXTILES ----------------
    (
        "Namthang Khulhat Silk Inaphee",
        "textile", "imphal", 6500, "per item", "+919774521240",
        "Premium mulberry silk wrap featuring complex geometric Namthang Khulhat border motifs, woven on an indigenous loin/throw-shuttle loom. By Smt. Angom Anita Devi (National Awardee), Wangkhei Mayai Leikai, Imphal East."
    ),
    (
        "Rani Phee (Luxury Bridal Silk Veil)",
        "textile", "imphal", 8500, "per item", "+913852452112",
        "Translucent luxury fabric invented by the pioneer designer herself — fine mulberry silk warp blended with intricate weft designs using shiny tinsel and zari work. By Smt. Chabungbam Rani Devi (M/S Imphal Handloom), Wangkhei."
    ),
    (
        "Shaphee Lanphee (Warrior Shawl)",
        "textile", "imphal", 3200, "per item", "+917005545387",
        "Traditional black embroidered fabric with multi-colored border art (elephants, sun, stars) — historically gifted by regional kings to victorious warriors. GI Tagged. By M/S Luwangla Mijing Handloom Ltd., Andro Khunou Leikai."
    ),
    (
        "Wangkhei Phee (Fine Cotton Shawl)",
        "textile", "imphal", 1800, "per item", "+919862027931",
        "Ultra-light, highly transparent pristine white cotton fabric meticulously woven using exceptionally fine cotton yarn spikes on a fly-shuttle loom. GI Tagged. By Smt. Timayum Ashaprem Devi, Khongman Zone 2."
    ),
    (
        "Moirang Phee (Temple Border Saree)",
        "textile", "imphal", 2800, "per item", "+919436080402",
        "Historic weave characterized by the iconic sharp pointed 'Moirang Pheeijg' (temple spire structure) along its lengthwise borders. By Smt. Laishram Memicha Devi, Langthabal Kunja, Imphal West."
    ),
    (
        "Leirum Phee (Cultural Meitei Scarf)",
        "textile", "imphal", 1200, "per item", "+919436080190",
        "The signature red and white checked cultural scarf of the Meitei community, carrying historical state motifs and symbolic community protection geometry. By M/S Crafts Development Promotors Org., Ningomthong."
    ),
    (
        "Phanek Mapal Naiba (Embroidered Skirt)",
        "textile", "thoubal", 2200, "per item", "+919334105882",
        "The quintessential lower wrap for women, embellished with classic hand-needlework lines along the borders using fine silk thread gradients. By Smt. Yengkhom Ongbi Indira Devi, Kakching Khunou."
    ),
    (
        "Khamen Chatpa (Block Printed Silk Dhoti)",
        "textile", "imphal", 3800, "per item", "+919862107863",
        "Deep purple block patterns hand-printed on white silk dhotis — historically worn by royalty, nobles, and distinguished elders during festivals. By Shri L. Loken Singh (Krydo), Iroisemba, Imphal West."
    ),
    (
        "Phanek Mayek Naiba (Traditional Skirt)",
        "textile", "bishnupur", 1600, "per item", "+919774300812",
        "Hand-loomed cotton wrap-around with precision horizontal stripe grids — specifically stylized for cultural dances and community ritual assemblies. By Smt. Heisnam Sabitri Devi, Thanga Heisnam Leikai."
    ),
    (
        "Purum Pon (Tribal Geometric Shawl)",
        "textile", "churachandpur", 2600, "per item", "+919612399402",
        "Heavy cotton tribal wrap carrying specific family-line red, black, and white bands representing ancient lineage identifiers of the Chothe clan. By M/S Chothe Tribal Weaving Center, Purum Khullen, Chandel."
    ),
    (
        "Inpui Kachon (Tribal Ceremonial Shawl)",
        "textile", "tamenglong", 2400, "per item", "+918731902447",
        "Thick backstrap-loomed shawl displaying signature stylized black rows interspersed with tiny scarlet horizontal bands, representing unity. By M/S Inpui Naga Weaving Cluster, Haochong Village, Noney."
    ),
    (
        "Poumai Kiili (Heavy Woolen Shawl)",
        "textile", "senapati", 3500, "per item", "+919863211095",
        "Extremely dense, wind-resistant loin-loomed black wool wrap detailed with red and emerald broad columns — engineered for harsh high-altitude winters. By M/S Poumai Naga Textile Weavers, Lairouching, Senapati."
    ),
    (
        "Chonkhom (Tangkhul Tribal Shawl)",
        "textile", "ukhrul", 2900, "per item", "+918131844026",
        "Vibrant red throw-shawl styled with central broad white panels and thin black side-lines — standard festive apparel for young tribal leaders. By M/S Tangkhul Handloom Society, Hunphun, Ukhrul."
    ),

    # ---------------- POTTERY ----------------
    (
        "Longpi Ham (Black Stone Cooking Pot)",
        "handicraft", "ukhrul", 2200, "per item", "+917423967383",
        "World-famous matte black earthenware crafted by hand without a potter's wheel, using a unique paste of serpentine stone and local black clay. By M/S Longpi Pottery Co-operative Society, Longpi Khullen & Kajiui, Ukhrul."
    ),
    (
        "Andro Charai Ham (Coiled Red Pottery)",
        "handicraft", "imphal", 900, "per item", "+917005144293",
        "Traditional terracotta utility vessels made through code-guided coiling and hand-beating methods by married women of the Andro community, baked in open pits. By M/S Andro Pottery Heritage Cluster, Andro Loi Village."
    ),

    # ---------------- CANE & BAMBOO ----------------
    (
        "Phingaruk (Traditional Dome Basket)",
        "handicraft", "imphal", 1400, "per item", "+919862107863",
        "Double-walled domed storage basket made from finely split hill bamboo — heavily used for storing premium wedding garments and royal offerings. By M/S Konthoujam Tribal Handicraft Society, Imphal West."
    ),
    (
        "Leephang (Low Dining Bamboo Table)",
        "handicraft", "churachandpur", 3800, "per item", "+919402831447",
        "Circular, short-legged dining tables woven entirely from cured wild cane and bamboo slits, coated with natural resin for heat resistance. By M/S Maring Bamboo Basketry Cluster, Machhi Village, Chandel."
    ),
    (
        "Long (Traditional Bamboo Fishing Trap)",
        "handicraft", "churachandpur", 750, "per item", "+917085311405",
        "Ergonomic, basket-like conical fishing gear made from fine bamboo splits — widely utilized by village communities in pristine local marsh streams. By M/S Tarao Cane & Thatch Crafts, Leishang Khunou, Chandel."
    ),
    (
        "Sanamahi Kot (Bamboo Sculpted Shrine)",
        "handicraft", "tamenglong", 1800, "per item", "+919436844102",
        "Miniature household Sanamahi structural altars intricately hand-carved from seasoned hollow bamboo poles for ethnic home setups. By M/S Noney Bamboo Crafts Society, Longmai (Noney) Bazaar."
    ),

    # ---------------- NATURAL FIBER ----------------
    (
        "Kauna Phak (Water Reed Mat & Cushion)",
        "handicraft", "thoubal", 1200, "per set", "+913852450340",
        "Organic eco-friendly mats and cushions intricately hand-woven from dry Kauna (marsh water reed) — known for natural thermal insulation properties. By M/S Alliance for Development Alternative, Kakching Bazaar."
    ),
    (
        "Kauna Sustainable Designer Handbags",
        "handicraft", "imphal", 1600, "per item", "+917005122910",
        "Contemporary, strong-braided ladies' handbag made from premium water hyacinth and water reed stalk fibers with floral cloth inner lining. By Smt. Chongtham Loyalakpi Chanu, Sega Road, Imphal."
    ),
    (
        "Kauna Eco-Friendly Picnic Baskets",
        "handicraft", "thoubal", 950, "per item", "+919856511983",
        "Sturdy woven storage basket with loop handles, made entirely of marsh reed stalks — completely organic and treated against moisture. By M/S Waithou Reed Handcrafts Society, Waithou Mapal."
    ),

    # ---------------- JEWELRY ----------------
    (
        "Likli (Manipuri Beaded Jewelry Set)",
        "jewelry", "imphal", 1100, "per set", "+919856140332",
        "Traditional necklaces and bracelets crafted using micro glass beads and polished metal spacers, following old royal structural patterns. By Smt. A. Bimola Devi, Kwaitehel Heinoukhongnembi, Imphal West."
    ),
    (
        "Thangal Tribal Beaded Headgear",
        "jewelry", "senapati", 2500, "per item", "+917629988103",
        "Ceremonial dynamic head-wear lined with genuine boar tusks, red felt, and hand-woven geometric glass beads — used in historical community dances. By M/S Thangal Eco-Tourism Crafts Union, Mayangkhang."
    ),

    # ---------------- WOOD CARVING ----------------
    (
        "Zeliangrong Engraved Wooden Platters",
        "handicraft", "tamenglong", 2800, "per set", "+919402755301",
        "Solid single-block wood dining serving platters featuring relief carvings of hornbill birds and animal head contours symbolizing prosperity. By M/S Zeliangrong Wood Carving Guild, Tamenglong Ward No. 3."
    ),

    # ---------------- CULTURAL AGRI-PRODUCTS ----------------
    (
        "Chak-Hao (Premium GI Organic Black Rice) — 1kg",
        "food", "imphal", 450, "per kg", "+913852410687",
        "Aromatic, deep-purple rich glutinous rice grown organically in the valleys — traditional core ingredient for community feast porridge/kheer. GI Certified. By M/S Thangjam Agro Industries (Pabung), Chingmeirong."
    ),
    (
        "Sirarakhong Hathei Chilli (Powder/Dried) — 250g",
        "food", "ukhrul", 350, "per pack", "+918794721094",
        "Brilliant blood-red, long, organic chilli variety native strictly to the microclimate of Sirarakhong hills — loved for high color and distinct mild heat. By M/S Ukhrul Chilli Growers Cluster, Sirarakhong Village."
    ),
    (
        "Kachai Lemon (GI Organic Citrus) — 1kg",
        "food", "ukhrul", 280, "per kg", "+919612904881",
        "Exquisite variety of lemon containing exceptionally high ascorbic acid (Vitamin C) content — grown exclusively in the hill terrains of Kachai village. GI Certified."
    ),
    (
        "Tamenglong Mandarin Orange — 2kg",
        "food", "tamenglong", 400, "per 2kg", "+918415933201",
        "Famous GI-protected, thick-skinned mandarin oranges heavily integrated into regional community winter harvest folklore and harvest festivals. By M/S Tamenglong Orange Growers Group."
    ),
    (
        "Mao Local Plum & Wild Forest Honey Combo",
        "food", "senapati", 650, "per combo", "+918974055109",
        "Pure, unpasteurized forest honey paired with sun-dried sweet plums harvested locally by the Mao Naga tribal community in hill farms. By M/S Mao Organic Flower & Fruit Hub, Mao Border Town."
    ),
]


# Services — kept from before (guides, workshops)
SERVICES = [
    (
        "Guided Heritage Tour of Kangla Fort",
        "guide", "imphal", 1200, "per person", "+919999999999",
        "3-hour guided walking tour of Kangla Fort with a local historian. Includes entry tickets and refreshments."
    ),
    (
        "Manipuri Classical Dance Workshop",
        "workshop", "imphal", 800, "per person", "+919999999999",
        "2-hour hands-on workshop with a professional Ras Leela performer. Includes costume trial."
    ),
    (
        "Loktak Lake Sunrise Boat Tour",
        "guide", "loktak", 1500, "per person", "+919999999999",
        "Early-morning boat tour of Loktak Lake with a local guide who knows the best photo spots. Includes tea and snacks."
    ),
    (
        "Pottery Workshop with Local Artisan",
        "workshop", "imphal", 1000, "per person", "+919999999999",
        "Hands-on pottery workshop with a 3rd-generation Manipuri potter. Take home your creation. All materials included."
    ),
    (
        "Traditional Manipuri Cooking Class",
        "workshop", "imphal", 1800, "per person", "+919999999999",
        "Learn to cook 3 iconic Manipuri dishes: Eromba, Chamthong, and Singju. Includes market visit."
    ),
]

EXTRA_SERVICES = [
    # ============ PERFORMING ARTS ============
    (
        "Pena Traditional Musical Storytelling & Ballad Session",
        "performance", "imphal", 2500, "per session", "+919774351953",
        "Exclusive tourist recitals of 'Pena' — an ancient single-stringed bowed musical instrument used to invoke deities in Lai Haraoba festivals and narrate the love epic of Khamba and Thoibi. By Kanglei Indigenous Martial Arts and Cultural Society (KIMACS), Keishamthong Elangbam Leikai."
    ),
    (
        "Lai Haraoba Ritualistic Dance Performance Guiding",
        "performance", "imphal", 3000, "per group", "+919362111253",
        "Managed access and cultural explanation sessions for international visitors wishing to observe the highly stylized sacred dances performed by Maibis (priestesses) to celebrate cosmic creation stories. By Lai Haraoba Ritualistic Dance Performers Ensemble, Thangmeiband Yumnam Leikai."
    ),

    # ============ MARTIAL ARTS & SPORTS ============
    (
        "Thang-Ta Ancient Sword & Spear Live Demonstration",
        "performance", "imphal", 1500, "per person", "+914385279540",
        "Curated 1-hour demonstrations of Huyen Langlon — breathing control, historical shields, active sword fights, and spear routines originally used by warriors to defend the kingdom. By Thang-Ta Federation of India, Yumnam Huidrom."
    ),
    (
        "3-Day Thang-Ta Martial Art Bootcamp",
        "workshop", "imphal", 4500, "per person", "+917005702675",
        "Intensive 3-day beginner package covering ritualistic postures, defensive footwork, and the basic history behind Manipur's ancient blade culture. By Laaman Thang-Ta Academy, Tera Loukrakpam Leikai."
    ),
    (
        "Manipuri Traditional Bamboo Bow Archery Trial",
        "workshop", "imphal", 900, "per session", "+919402699699",
        "Hands-on shooting workshop with master marksmen using hand-carved local bamboo longbows. Focuses on historical archery stances and traditional techniques. At Khuman Lampak Sports Complex."
    ),
    (
        "Mukna Traditional Wrestling Exhibition Match",
        "performance", "imphal", 2500, "per group", "+919354559217",
        "Live tournaments of Mukna — a historic form of wrestling dating back to the 14th century, complete with ancient waist-girdle holding techniques and traditional refereeing costumes. By Mukna Association, Kakching Khunou."
    ),

    # ============ HERITAGE GUIDING ============
    (
        "Imphal Walks: WWII & Royal Heritage Trail",
        "guide", "imphal", 1200, "per person", "+919856009357",
        "High-end walking tours through Kangla Fort, royal coronation sites, sacred groves, and the intense World War II battlegrounds of the Battle of Imphal. Includes certified English-speaking historians. By Imphal Walks."
    ),
    (
        "Andro Cultural Heritage Village Guided Walk",
        "guide", "imphal", 700, "per person", "+918131980420",
        "Guided walk through the famous open-air museum of Andro — highlighting the century-old sacred fire that has been continuously lit, unique pottery huts, and tribal doll installations. By Andro Cultural Heritage Village Interpreters."
    ),
    (
        "Khongjom War Memorial History Tour",
        "guide", "thoubal", 800, "per person", "+913852410687",
        "On-site specialized historical tour covering the heroic stand of Paona Brajabasi against British forces in 1891. Includes guided climb up the scenic Kheba Hill monument. By Khongjom War Memorial Heritage Guides."
    ),
    (
        "Sekta Archaeological Living Museum Tour",
        "guide", "imphal", 1500, "per person", "+919362111253",
        "Certified English/Hindi-speaking micro-guide tour of the Sekta Archaeological Living Museum, ancient monolith locations, and cave paths. By Incredible Manipur Tourist Information Center."
    ),

    # ============ CRAFT WORKSHOPS ============
    (
        "Ancient Split-Bamboo Fish Trap Weaving Workshop",
        "workshop", "churachandpur", 1500, "per person", "+919862028656",
        "Tribal craft training session where elders teach the geometric secrets behind mathematical bamboo splitting and interlocking weave patterns for 'Long' fishing baskets. By Maring Bamboo & Cane Basketry Weaving Cell, Maring Phunal Village, Chandel."
    ),
    (
        "Wangkhei Loom-to-Garment Handloom Discovery Walk",
        "guide", "imphal", 1000, "per person", "+913852450340",
        "Takes visitors inside residential lanes where Meitei women weave high-transparency luxury fabrics right underneath their traditional stilt houses on customized wooden frames. By Wangkhei Weaving Clusters Guide Service."
    ),

    # ============ CULINARY EXPERIENCES ============
    (
        "Chak-Hao Kheer (Black Rice Dessert) Making Session",
        "workshop", "imphal", 1200, "per person", "+919362111253",
        "Hands-on culinary service teaching food travelers how to extract the deep purple hue and nutty aroma of Manipur's GI-tagged black rice using local techniques. By Chak-Hao Organic Food Artisans Guild, Lamphelpat."
    ),
    (
        "Loktak Lake Smoked Fish & Foraging Culinary Tour",
        "other", "loktak", 2200, "per person", "+918415076121",
        "Dynamic culinary tour where tourists catch native fish with local fishermen and smoke them using traditional hay and wood embers inside a floating bamboo hut. By Loktak Lake Traditional Smoked Fish Culinary Tours, Moirang."
    ),
    (
        "Sirarakhong Hathei Chilli Paste Workshop",
        "workshop", "ukhrul", 1000, "per person", "+919435148180",
        "Learn to safely use the highly vibrant, non-pungent Sirarakhong Hathei chilli to create traditional tribal pastes over open woodfires. By Sirarakhong Hathei Spice Kitchen, Ukhrul."
    ),
    (
        "Ima Keithel Fermented Food Tasting Trail",
        "other", "imphal", 900, "per person", "+919856009357",
        "Guided flavor walk through Asia's largest all-women market — educating culinary travelers on bamboo-shoot fermentation (Soibum) and sun-dried fish aging (Ngari). By Ima Keithel Organic Fermented Food Explorations."
    ),

    # ============ EXTRA TRANSPORT / LOGISTICS ============
    (
        "Kangla Fort Sunrise Photo Walk",
        "guide", "imphal", 700, "per person", "+919999999999",
        "Early-morning photo walk through Kangla Fort with a local photographer-guide who knows the best sunrise angles. Includes chai and traditional Manipuri breakfast."
    ),
    (
        "Manipur Village Homestay Day Trip",
        "transport", "imphal", 2000, "per group", "+919999999999",
        "Full-day visit to a traditional Manipuri village with home-cooked lunch, weaving demonstration, and cultural exchange. Up to 4 passengers."
    ),
]


class Command(BaseCommand):
    help = "Seed the marketplace with real Manipur artisans and services"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            "\n🛒 Seeding marketplace with real artisans...\n"
        ))

        seller = self._get_seller()
        self.stdout.write(f"   👤 Seller: {seller.username}\n")

        product_created = self._seed_items(PRODUCTS, "product", seller)
        service_created = self._seed_items(SERVICES, "service", seller)
        extra_created = self._seed_items(EXTRA_SERVICES, "service", seller)
        service_created += extra_created

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("✅ Marketplace seeded!"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(f"   Products:  {product_created} created")
        self.stdout.write(f"   Services:  {service_created} created")
        self.stdout.write(f"   Total listings in DB: {Listing.objects.count()}")
        self.stdout.write("")

    # --------------------------------------------------------
    def _get_seller(self):
        """Get or create the demo seller account."""
        seller, _ = User.objects.get_or_create(
            username="ramesh",
            defaults={
                "email": "ramesh@xcalate.com",
                "role": "local",
                "phone": "+919999999999",
                "region": "imphal",
                "business_name": "Xcalate Artisan Collective",
            },
        )
        if not seller.has_usable_password():
            seller.set_password("Test@1234")
            seller.save()
        return seller

    # --------------------------------------------------------
    def _seed_items(self, items, item_type, seller):
        created = 0
        for (title, category, region, price, unit, phone, description) in items:
            slug = slugify(title)[:180]
            defaults = {
                "user": seller,
                "type": item_type,
                "title": title,
                "short_description": description[:280],
                "description": description,
                "price": price,
                "price_unit": unit,
                "region": region,
                "category": category,
                "contact_phone": phone,
                "contact_email": "ramesh@xcalate.com",
                "whatsapp": phone,
                "images": [f"https://picsum.photos/seed/{slug}/1200/800"],
                "is_active": True,
                "is_featured": price >= 2500,
            }
            _, was_created = Listing.objects.update_or_create(
                slug=slug, defaults=defaults
            )
            if was_created:
                created += 1
                self.stdout.write(f"   ✅ {title}")
        return created