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


def get_element_types(ifc_path):
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        element_types = set()
        for entity in ifc_file:
            element_types.add(entity.is_a())
        return list(element_types)
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_psets_for_entity(ifc_path, entity_type):
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        psets = set()
        for entity in ifc_file.by_type(entity_type):
            for definition in entity.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    psets.add(definition.RelatingPropertyDefinition.Name)
        return list(psets)
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_properties_in_pset(ifc_path, pset_name):
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        for entity in ifc_file.by_type('IfcPropertySet'):
            if entity.Name == pset_name:
                return [prop.Name for prop in entity.HasProperties]
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_property_value(ifc_path, entity_type, pset_name, property_name):
    try:
        ifc_file = ifcopenshell.open(ifc_path)
        for entity in ifc_file.by_type(entity_type):
            for definition in entity.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    pset = definition.RelatingPropertyDefinition
                    if pset.Name == pset_name:
                        for prop in pset.HasProperties:
                            if prop.Name == property_name:
                                return prop.NominalValue
        raise ValueError("Property not found")
    except Exception as e:
        print(f"Error: {e}")
        raise ValueError("Error retrieving property value")

def compare_ifcs(ifc_path1, ifc_path2):
    element_types = get_element_types(ifc_path1)
    print(f"Element types: {element_types}")

    all_psets = {}
    for entity_type in element_types:
        psets = get_psets_for_entity(ifc_path1, entity_type)
        all_psets[entity_type] = psets
        print(f"Psets for {entity_type}: {psets}")

    all_properties = {}
    for entity_type, psets in all_psets.items():
        for pset in psets:
            properties = get_properties_in_pset(ifc_path1, pset)
            all_properties[(entity_type, pset)] = properties
            print(f"Properties in {pset} for {entity_type}: {properties}")

    all_values_ifc1 = []
    for (entity_type, pset), properties in all_properties.items():
        for prop in properties:
            value = get_property_value(ifc_path1, entity_type, pset, prop)
            all_values_ifc1.append(value)
    print(f"All values from IFC1: {all_values_ifc1}")

    request_count = 0
    matched_count = 0
    for (entity_type, pset), properties in all_properties.items():
        for prop in properties:
            try:
                value_ifc1 = get_property_value(ifc_path1, entity_type, pset, prop)
                value_ifc2 = get_property_value(ifc_path2, entity_type, pset, prop)
                request_count += 1
                if isinstance(value_ifc2, type(value_ifc1)):
                    matched_count += 1
            except ValueError:
                continue
    
    similarity_score = (matched_count / request_count) * 100 if request_count > 0 else 0
    print(f"Requests made: {request_count}")
    print(f"Requests matched: {matched_count}")
    print(f"Similarity score: {similarity_score:.2f}%")


if __name__ == "__main__":
    compare_ifcs("path/to/your1.ifc", "path/to/your2.ifc")
