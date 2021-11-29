# used in Plant

def decision_tree(plant):
    if plant.field.hydration == 4:
        if plant.is_healthy == 1:
            if plant.field.tractor_there == 0:
                if plant.ticks == 0:
                    return 0
                elif plant.ticks == 1:
                    return 1
            elif plant.field.tractor_there == 1:
                return 0
        elif plant.is_healthy == 0:
            return 0
    elif plant.field.hydration == 2:
        if plant.species == "sorrel":
            if plant.ticks == 1:
                if plant.is_healthy == 1:
                    return 1
                elif plant.is_healthy == 0:
                    return 0
            elif plant.ticks == 0:
                return 0
        elif plant.species == "potato":
            return 0
        elif plant.species == "wheat":
            return 0
        elif plant.species == "strawberry":
            return 0
    elif plant.field.hydration == 1:
        if plant.species == "potato":
            return 0
        elif plant.species == "strawberry":
            if plant.ticks == 1:
                return -1
            elif plant.ticks == 0:
                return 0
        elif plant.species == "wheat":
            return 0
        elif plant.species == "sorrel":
            if plant.is_healthy == 0:
                return 0
            elif plant.is_healthy == 1:
                if plant.field.tractor_there == 0:
                    if plant.ticks == 0:
                        return 0
                    elif plant.ticks == 1:
                        return 1
                elif plant.field.tractor_there == 1:
                    return 0
    elif plant.field.hydration == 3:
        if plant.ticks == 1:
            if plant.field.tractor_there == 0:
                if plant.is_healthy == 1:
                    if plant.species == "potato":
                        if plant.field.fertility == 1:
                            return 1
                        elif plant.field.fertility == 0:
                            return 0
                    elif plant.species == "strawberry":
                        return 1
                    elif plant.species == "sorrel":
                        return 1
                    elif plant.species == "wheat":
                        return 1
                elif plant.is_healthy == 0:
                    return 0
            elif plant.field.tractor_there == 1:
                return 0
        elif plant.ticks == 0:
            return 0
    elif plant.field.hydration == 5:
        if plant.field.tractor_there == 1:
            return 0
        elif plant.field.tractor_there == 0:
            if plant.is_healthy == 0:
                return 0
            elif plant.is_healthy == 1:
                if plant.ticks == 1:
                    return 1
                elif plant.ticks == 0:
                    return 0
    elif plant.field.hydration == 0:
        if plant.ticks == 0:
            return 0
        elif plant.ticks == 1:
            return -1
