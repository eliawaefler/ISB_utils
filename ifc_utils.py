import ifcopenshell

def clean_ifc(ifc_file_path):
    # Open the IFC file
    ifc_model = ifcopenshell.open(ifc_file_path)
    
    # Create a new empty IFC file
    new_ifc_model = ifcopenshell.file()
    
    # Add the necessary header information
    for entity in ifc_model.by_type('IfcProject'):
        new_ifc_model.createIfcProject(entity.GlobalId, entity.OwnerHistory, entity.Name, entity.Description, entity.ObjectType, entity.LongName, entity.Phase)
        
    # Define the types to keep one instance of
    types_to_keep = [
        'IfcWall', 'IfcDoor', 'IfcWindow', 'IfcSlab', 'IfcColumn', 'IfcBeam',
        'IfcRoof', 'IfcStair', 'IfcRamp', 'IfcSpace', 'IfcZone', 'IfcCovering'
    ]
    
    # Dictionary to track added types
    added_types = {type_name: False for type_name in types_to_keep}
    
    for type_name in types_to_keep:
        instances = ifc_model.by_type(type_name)
        if instances:
            instance = instances[0]
            new_instance = new_ifc_model.add(instance)
            added_types[type_name] = True
            
            # Copy all attributes and property sets
            for attribute in instance.__dict__:
                setattr(new_instance, attribute, getattr(instance, attribute))
            for pset in ifcopenshell.util.element.get_psets(instance):
                ifcopenshell.util.element.add_pset(new_ifc_model, new_instance, pset)
    
    return new_ifc_model
