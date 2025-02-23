from get_ride_planning.infrastructure.config import start_app

get_ride_planning_handler = start_app()


def handler(event, context):
    return get_ride_planning_handler.handle(event, context)
