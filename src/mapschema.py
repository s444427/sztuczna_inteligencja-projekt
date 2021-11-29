def createField():
    field = [["soil", "soil", "soil", "soil", "soil", "soil", "rocks", "soil", "soil", "soil"],
             ["soil", "soil", "soil", "soil", "soil", "soil", "rocks", "soil", "soil", "soil"],
             ["soil", "soil", "soil", "soil", "soil", "road", "road", "road", "road", "road"],
             ["rocks", "rocks", "rocks", "rocks", "soil", "road", "soil", "soil", "rocks", "soil"],
             ["soil", "soil", "soil", "soil", "soil", "road", "rocks", "rocks", "soil", "soil"],
             ["soil", "soil", "soil", "pond", "rocks", "road", "rocks", "soil", "soil", "rocks"],
             ["rocks", "pond", "pond", "pond", "pond", "road", "rocks", "soil", "soil", "rocks"],
             ["road", "road", "road", "road", "road", "road", "rocks", "soil", "soil", "soil"],
             ["soil", "soil", "soil", "soil", "soil", "soil", "rocks", "soil", "rocks", "rocks"],
             ["soil", "soil", "soil", "soil", "soil", "rocks", "soil", "rocks", "rocks", "soil"]
             ]
    return field


def createPlants():
    field = [["wheat", "wheat", "wheat", "wheat", "wheat", "wheat", 0, "strawberry", "strawberry", "strawberry"],
             ["wheat", "wheat", "wheat", "wheat", "wheat", "wheat", 0, "strawberry", "strawberry", "strawberry"],
             ["wheat", "wheat", "wheat", "wheat", 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             ["wheat", "wheat", "wheat", "wheat", 0, 0, 0, 0, 0, 0],
             ["wheat", "wheat", "wheat", 0, 0, 0, 0, "potato", "potato", 0],
             [0, 0, 0, 0, 0, 0, 0, "potato", "potato", 0],
             [0, 0, 0, 0, 0, 0, 0, "potato", "potato", "potato"],
             ["strawberry", "strawberry", "strawberry", "strawberry", "strawberry", 0, 0, "potato", 0, 0],
             ["strawberry", "strawberry", "strawberry", "strawberry", "strawberry", 0, 0, 0, 0, 0]
             ]
    return field
