{
    "name": "Property Management",
    "summary": "Property Listing",
    "version": "18.0.1.0.0",
    "license": "OEEL-1",
    "depends": ["base"],
    "data": [
        # Data
        "data/property_type_data.xml",
        # Security files
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # Views
        "views/real_estate_views.xml",
        "views/estate_menus.xml"
        "views/res_users_views.xml"

    ],
    "demo": [
        "demo_data/demo.xml"
    ],
    "application": True
}