{
    "name": "Real Estate",
    "summary": "Test module",
    "version": "18.0",
    "license": "OEEL-1",
    "depends": ["crm"],
    "data": [
        # Security files
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # Views
        "views/real_estate_views.xml",
        "views/estate_menus.xml"
    ],
    "demo": [
        "demo/demo.xml"
    ],
    "application": True
}