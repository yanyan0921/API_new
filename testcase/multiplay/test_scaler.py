from testcase.multiplay.objects import object_controller


def test_scaler_fleet():
    try:
        instance_type = object_controller.create_instance_type()
        image = object_controller.create_image()
        fleet = object_controller.create_fleet(instance_type.id, image.id)
        region = object_controller.create_region()
    finally:
        object_controller.delete_region(region.id)
        object_controller.delete_fleet(fleet.id)
        object_controller.delete_image(image.id)
        object_controller.delete_instance_type(instance_type.id)
