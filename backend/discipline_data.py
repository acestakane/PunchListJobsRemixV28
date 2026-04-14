"""
PunchListJobs — Discipline → Trade → Skills hierarchy.
Single source of truth for seeding. Stored in DB under trades.skills[].
"""

DISCIPLINE_TREE = [
    {"name": "GENERAL LABOR", "trades": [
        {"name": "Moving Labor",        "skills": ["Loading", "Unloading", "Packing", "Furniture Moving", "Appliance Moving", "Heavy Lifting"]},
        {"name": "Site Cleanup",        "skills": ["Debris Removal", "Trash Hauling", "Construction Cleanup", "Post-Job Cleanup"]},
        {"name": "Event Labor",         "skills": ["Setup", "Teardown", "Booth Assembly", "Crowd Control"]},
        {"name": "Warehouse Support",   "skills": ["Sorting", "Palletizing", "Scanning", "Inventory Counting"]},
        {"name": "Delivery Assistance", "skills": ["Route Assistance", "Drop-offs", "Courier Support"]},
    ]},
    {"name": "HANDYMAN SERVICES", "trades": [
        {"name": "Minor Repairs",    "skills": ["Door Repair", "Drywall Patch", "Fixture Repair"]},
        {"name": "Installations",    "skills": ["Shelving", "Curtains", "Blinds", "TV Mounting"]},
        {"name": "Assembly",         "skills": ["Furniture Assembly", "Equipment Assembly"]},
        {"name": "Home Maintenance", "skills": ["Caulking", "Sealing", "Weatherproofing"]},
    ]},
    {"name": "CARPENTRY", "trades": [
        {"name": "Rough Carpentry",  "skills": ["Framing", "Blocking", "Joist Work"]},
        {"name": "Finish Carpentry", "skills": ["Trim", "Crown Molding", "Baseboards"]},
        {"name": "Cabinetry",        "skills": ["Cabinet Install", "Refacing", "Repair"]},
        {"name": "Custom Woodwork",  "skills": ["Built-ins", "Furniture Fabrication"]},
        {"name": "Decking",          "skills": ["Deck Build", "Deck Repair"]},
    ]},
    {"name": "PLUMBING", "trades": [
        {"name": "Basic Plumbing",        "skills": ["Leak Repair", "Faucet Install", "Toilet Install"]},
        {"name": "Advanced Plumbing",     "skills": ["Pipe Replacement", "Drain Line Install"]},
        {"name": "Drain Services",        "skills": ["Drain Cleaning", "Snaking", "Hydro Jetting"]},
        {"name": "Fixture Installation",  "skills": ["Sinks", "Showers", "Bathtubs"]},
        {"name": "Water Systems",         "skills": ["Water Heater Install", "Filtration Systems"]},
    ]},
    {"name": "ELECTRICAL", "trades": [
        {"name": "Basic Electrical", "skills": ["Outlet Install", "Switch Replacement", "Light Fixtures"]},
        {"name": "Wiring",           "skills": ["Rewiring", "Circuit Installation"]},
        {"name": "Panels",           "skills": ["Panel Upgrade", "Breaker Replacement"]},
        {"name": "Low Voltage",      "skills": ["Security Systems", "Data Cabling"]},
        {"name": "Smart Home",       "skills": ["Smart Switches", "Thermostats"]},
    ]},
    {"name": "HVAC", "trades": [
        {"name": "Installation", "skills": ["AC Units", "Furnaces", "Heat Pumps"]},
        {"name": "Maintenance",  "skills": ["Filter Replacement", "System Cleaning"]},
        {"name": "Repair",       "skills": ["Diagnostics", "Component Replacement"]},
        {"name": "Ventilation",  "skills": ["Duct Installation", "Duct Cleaning"]},
    ]},
    {"name": "PAINTING", "trades": [
        {"name": "Interior Painting",  "skills": ["Walls", "Ceilings", "Trim"]},
        {"name": "Exterior Painting",  "skills": ["Siding", "Fences", "Decks"]},
        {"name": "Specialty Coatings", "skills": ["Epoxy", "Waterproofing"]},
        {"name": "Surface Prep",       "skills": ["Sanding", "Priming", "Power Washing"]},
    ]},
    {"name": "DRYWALL & PLASTER", "trades": [
        {"name": "Installation", "skills": ["Hanging Drywall", "Taping"]},
        {"name": "Finishing",    "skills": ["Mudding", "Sanding"]},
        {"name": "Repair",       "skills": ["Hole Patching", "Crack Repair"]},
        {"name": "Texture",      "skills": ["Knockdown", "Orange Peel"]},
    ]},
    {"name": "FLOORING", "trades": [
        {"name": "Installation", "skills": ["Hardwood", "Laminate", "Vinyl", "Tile"]},
        {"name": "Repair",       "skills": ["Board Replacement", "Crack Repair"]},
        {"name": "Finishing",    "skills": ["Sanding", "Staining", "Sealing"]},
        {"name": "Carpet",       "skills": ["Install", "Stretching", "Repair"]},
    ]},
    {"name": "ROOFING", "trades": [
        {"name": "Installation", "skills": ["Shingles", "Metal Roofing"]},
        {"name": "Repair",       "skills": ["Leak Repair", "Flashing"]},
        {"name": "Maintenance",  "skills": ["Inspections", "Cleaning"]},
        {"name": "Gutters",      "skills": ["Install", "Cleaning", "Repair"]},
    ]},
    {"name": "LANDSCAPING & OUTDOOR", "trades": [
        {"name": "Lawn Care",      "skills": ["Mowing", "Edging", "Fertilizing"]},
        {"name": "Yard Cleanup",   "skills": ["Leaf Removal", "Debris Clearing"]},
        {"name": "Tree Services",  "skills": ["Trimming", "Removal", "Stump Grinding"]},
        {"name": "Hardscaping",    "skills": ["Pavers", "Retaining Walls"]},
        {"name": "Irrigation",     "skills": ["Sprinkler Install", "Repair"]},
    ]},
    {"name": "CONCRETE & MASONRY", "trades": [
        {"name": "Concrete Work", "skills": ["Pouring", "Finishing", "Stamping"]},
        {"name": "Masonry",       "skills": ["Bricklaying", "Stonework"]},
        {"name": "Repair",        "skills": ["Crack Repair", "Resurfacing"]},
        {"name": "Demolition",    "skills": ["Concrete Breaking"]},
    ]},
    {"name": "DEMOLITION", "trades": [
        {"name": "Interior Demo",   "skills": ["Walls", "Cabinets", "Fixtures"]},
        {"name": "Exterior Demo",   "skills": ["Sheds", "Decks"]},
        {"name": "Selective Demo",  "skills": ["Partial Removal"]},
        {"name": "Hauling",         "skills": ["Debris Removal"]},
    ]},
    {"name": "CLEANING SERVICES", "trades": [
        {"name": "Residential Cleaning",  "skills": ["Deep Cleaning", "Move-In/Out"]},
        {"name": "Commercial Cleaning",   "skills": ["Office Cleaning", "Janitorial"]},
        {"name": "Post-Construction",     "skills": ["Dust Removal", "Debris Cleanup"]},
        {"name": "Specialty Cleaning",    "skills": ["Carpet", "Windows", "Pressure Washing"]},
    ]},
    {"name": "MOVING & HAULING", "trades": [
        {"name": "Residential Moving", "skills": ["Local Moves", "Packing"]},
        {"name": "Commercial Moving",  "skills": ["Office Relocation"]},
        {"name": "Junk Removal",       "skills": ["Appliance Removal", "Furniture Disposal"]},
        {"name": "Specialty Moving",   "skills": ["Piano", "Safe Moving"]},
    ]},
    {"name": "AUTOMOTIVE SERVICES", "trades": [
        {"name": "Basic Maintenance", "skills": ["Oil Change", "Tire Rotation"]},
        {"name": "Repairs",           "skills": ["Brake Work", "Battery Replacement"]},
        {"name": "Mobile Mechanic",   "skills": ["On-Site Diagnostics"]},
        {"name": "Detailing",         "skills": ["Interior", "Exterior"]},
    ]},
    {"name": "DELIVERY & LOGISTICS", "trades": [
        {"name": "Last Mile Delivery", "skills": ["Package Delivery"]},
        {"name": "Freight Handling",   "skills": ["Loading", "Dock Work"]},
        {"name": "Courier Services",   "skills": ["Same-Day Delivery"]},
        {"name": "Route Driving",      "skills": ["Scheduled Routes"]},
    ]},
    {"name": "WAREHOUSE & DISTRIBUTION", "trades": [
        {"name": "Picking & Packing",    "skills": ["Order Fulfillment"]},
        {"name": "Forklift Operation",   "skills": ["Pallet Moving"]},
        {"name": "Inventory",            "skills": ["Audits", "Stocking"]},
        {"name": "Shipping/Receiving",   "skills": ["Dock Work"]},
    ]},
    {"name": "CONSTRUCTION TRADES (SPECIALIZED)", "trades": [
        {"name": "Ironwork",    "skills": ["Steel Erection"]},
        {"name": "Welding",     "skills": ["MIG", "TIG", "Stick"]},
        {"name": "Scaffolding", "skills": ["Assembly", "Dismantling"]},
        {"name": "Glazing",     "skills": ["Window Install"]},
        {"name": "Insulation",  "skills": ["Spray Foam", "Batt"]},
    ]},
    {"name": "SECURITY SERVICES", "trades": [
        {"name": "Event Security",   "skills": ["Crowd Monitoring"]},
        {"name": "Site Security",    "skills": ["Patrol", "Access Control"]},
        {"name": "Loss Prevention",  "skills": ["Retail Monitoring"]},
    ]},
    {"name": "TECHNOLOGY & INSTALLATION", "trades": [
        {"name": "IT Support",      "skills": ["Hardware Setup"]},
        {"name": "Network Install", "skills": ["Cabling", "Routers"]},
        {"name": "AV Installation", "skills": ["Speakers", "Projectors"]},
        {"name": "Smart Devices",   "skills": ["Cameras", "Automation"]},
    ]},
    {"name": "HOSPITALITY & EVENTS", "trades": [
        {"name": "Catering Staff",  "skills": ["Servers", "Bartenders"]},
        {"name": "Event Setup",     "skills": ["Tables", "Chairs"]},
        {"name": "Kitchen Help",    "skills": ["Prep Cook", "Dishwasher"]},
        {"name": "Guest Services",  "skills": ["Ushers", "Check-in"]},
    ]},
    {"name": "RETAIL SUPPORT", "trades": [
        {"name": "Merchandising",       "skills": ["Shelf Stocking"]},
        {"name": "Store Setup",         "skills": ["Fixture Assembly"]},
        {"name": "Inventory",           "skills": ["Cycle Counts"]},
        {"name": "Customer Assistance", "skills": ["Floor Support"]},
    ]},
    {"name": "HEALTHCARE SUPPORT (NON-LICENSED)", "trades": [
        {"name": "Patient Support",   "skills": ["Transport"]},
        {"name": "Facility Cleaning", "skills": ["Sanitation"]},
        {"name": "Medical Assistance","skills": ["Basic Aid Support"]},
    ]},
    {"name": "PERSONAL SERVICES", "trades": [
        {"name": "Errands",            "skills": ["Shopping", "Pickup"]},
        {"name": "Personal Assistant", "skills": ["Scheduling", "Admin"]},
        {"name": "Home Organization",  "skills": ["Decluttering"]},
        {"name": "Pet Care",           "skills": ["Walking", "Sitting"]},
    ]},
    {"name": "AGRICULTURE & FARM WORK", "trades": [
        {"name": "Harvesting",          "skills": ["Crop Picking"]},
        {"name": "Field Work",          "skills": ["Planting", "Weeding"]},
        {"name": "Equipment Operation", "skills": ["Tractor Use"]},
        {"name": "Livestock Care",      "skills": ["Feeding", "Cleaning"]},
    ]},
    {"name": "MARINE & OUTDOOR LABOR", "trades": [
        {"name": "Dock Work",      "skills": ["Loading", "Maintenance"]},
        {"name": "Boat Cleaning",  "skills": ["Detailing"]},
        {"name": "Marina Support", "skills": ["General Labor"]},
    ]},
    {"name": "ENERGY & UTILITIES", "trades": [
        {"name": "Solar Installation",    "skills": ["Panel Mounting"]},
        {"name": "Electrical Grid Work",  "skills": ["Line Support"]},
        {"name": "Meter Reading",         "skills": ["Data Collection"]},
    ]},
    {"name": "INSPECTION & QUALITY CONTROL", "trades": [
        {"name": "Site Inspection", "skills": ["Punchlist Verification"]},
        {"name": "QA/QC",           "skills": ["Compliance Checks"]},
        {"name": "Safety Inspection","skills": ["OSHA Compliance"]},
    ]},
    {"name": "PUNCHLIST / SNAGLIST SPECIALTY", "trades": [
        {"name": "Final Touch Work",    "skills": ["Paint Touch-Ups", "Trim Fixes"]},
        {"name": "Fixture Adjustments", "skills": ["Doors", "Cabinets"]},
        {"name": "Cosmetic Repairs",    "skills": ["Chips", "Scratches"]},
        {"name": "Compliance Fixes",    "skills": ["Code Corrections"]},
    ]},
    {"name": "GIG / ON-DEMAND TASKS", "trades": [
        {"name": "Task Running",       "skills": ["Errands", "Pickups"]},
        {"name": "Microtasks",         "skills": ["Assembly", "Quick Fixes"]},
        {"name": "Temporary Staffing", "skills": ["Short-Term Roles"]},
        {"name": "On-Demand Labor",    "skills": ["Same-Day Jobs"]},
    ]},
]
