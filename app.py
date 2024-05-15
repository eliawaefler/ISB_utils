import streamlit as st

import ifcopenshell
import random
import ifcopenshell
import ifcopenshell.util.element
import streamlit as st
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

def main():
    st.title('IFC File Cleaner')
    uploaded_file = st.file_uploader("Upload an IFC file", type=['ifc'])
    
    if uploaded_file is not None:
        # Save the uploaded file locally
        with open("uploaded.ifc", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Clean the IFC file
        cleaned_ifc = clean_ifc("uploaded.ifc")
        
        # Save the cleaned IFC file locally
        cleaned_ifc.write("cleaned.ifc")
        
        # Provide a download link for the cleaned IFC file
        with open("cleaned.ifc", "rb") as f:
            st.download_button("Download Cleaned IFC", f, file_name="cleaned.ifc")

if __name__ == "__main__":
    main()

def request_ifc(ifc_path, query=''):
    # Open the IFC file
    ifc_model = ifcopenshell.open(ifc_path)
    
    # Define the query logic
    if query == 'get_wall_attributes':
        result = []
        walls = ifc_model.by_type('IfcWall')
        for wall in walls:
            wall_data = {
                "GlobalId": wall.GlobalId,
                "Name": wall.Name,
                "Description": wall.Description,
                "ObjectType": wall.ObjectType,
            }
            result.append(wall_data)
        return result
    
    elif query == 'get_door_property_sets':
        result = []
        doors = ifc_model.by_type('IfcDoor')
        for door in doors:
            door_data = {
                "GlobalId": door.GlobalId,
                "Name": door.Name,
                "PropertySets": {}
            }
            psets = ifcopenshell.util.element.get_psets(door)
            for pset_name, properties in psets.items():
                door_data["PropertySets"][pset_name] = properties
            result.append(door_data)
        return result
    
    elif query == 'get_floor_geometries':
        result = []
        floors = ifc_model.by_type('IfcSlab')
        for floor in floors:
            floor_data = {
                "GlobalId": floor.GlobalId,
                "Name": floor.Name,
                "Geometries": []
            }
            if floor.Representation is not None:
                for rep in floor.Representation.Representations:
                    rep_data = {
                        "RepresentationType": rep.RepresentationType,
                        "Items": [str(item) for item in rep.Items]
                    }
                    floor_data["Geometries"].append(rep_data)
            result.append(floor_data)
        return result
    
    else:
        return f"Unknown query: {query}"

# Example usage
ifc_path = "cleaned.ifc"
print(request_ifc(ifc_path, 'get_wall_attributes'))
print(request_ifc(ifc_path, 'get_door_property_sets'))
print(request_ifc(ifc_path, 'get_floor_geometries'))

st.write("hello world")



def generate_queries(ifc_path, n=50):
    # Open the IFC file
    ifc_model = ifcopenshell.open(ifc_path)
    
    # Define a list to store queries and their predefined answers
    queries_with_answers = []

    # Define possible queries
    possible_queries = [
        "get_wall_attributes",
        "get_door_property_sets",
        "get_floor_geometries"
    ]

    # Generate n queries
    for _ in range(n):
        query = random.choice(possible_queries)
        
        if query == 'get_wall_attributes':
            walls = ifc_model.by_type('IfcWall')
            if walls:
                answer = random.choice([
                    "Answer = 'GlobalId: " + walls[0].GlobalId + "'",
                    "Answer = 'Name: " + str(walls[0].Name) + "'",
                    "Answer = 'Description: " + str(walls[0].Description) + "'",
                    "Answer = 'ObjectType: " + str(walls[0].ObjectType) + "'",
                ])
            else:
                answer = "Answer = None"
        
        elif query == 'get_door_property_sets':
            doors = ifc_model.by_type('IfcDoor')
            if doors:
                psets = ifcopenshell.util.element.get_psets(doors[0])
                if psets:
                    pset_name, properties = random.choice(list(psets.items()))
                    prop_name, prop_value = random.choice(list(properties.items()))
                    answer = f"Answer = '{pset_name} - {prop_name}: {prop_value}'"
                else:
                    answer = "Answer = None"
            else:
                answer = "Answer = None"
        
        elif query == 'get_floor_geometries':
            floors = ifc_model.by_type('IfcSlab')
            if floors and floors[0].Representation:
                rep = random.choice(floors[0].Representation.Representations)
                answer = f"Answer = 'RepresentationType: {rep.RepresentationType}'"
            else:
                answer = "Answer = None"
        
        # Append the query and answer to the list
        queries_with_answers.append((query, answer))

    return queries_with_answers

# Example usage
ifc_path = "cleaned.ifc"
queries = generate_queries(ifc_path, n=5)
for query, answer in queries:
    print(f"Query: {query}, {answer}")
