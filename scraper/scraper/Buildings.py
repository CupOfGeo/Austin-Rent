from crawlee import Request

"""
I have been going back and forth on making this a database table but because well have so few rows
I also think that the label which dictates which route handler we use shouldn't be coded to the database.
I'm leaving in the db migration empty table but will remove the daos and models.
"""
buildings = [
    Request.from_url(
        url="https://sightmap.com/app/api/v1/8epml7q1v6d/sightmaps/80524",
        label="JSON",
        user_data={"building_id": 1},
    ),
    Request.from_url(
        url="https://sightmap.com/app/api/v1/60p7q39nw7n/sightmaps/397",
        label="JSON",
        user_data={"building_id": 2},
    ),
    Request.from_url(
        url="https://www.windsorcommunities.com/properties/windsor-on-the-lake/floorplans/",
        label="HTML",
        user_data={"building_id": 3},
    ),
    #     Request.from_url(
    #     url="https://en.wikipedia.org/wiki/Cgroups",
    #     label="HTML",
    #     user_data={"building_id": 3},
    # ),
]
