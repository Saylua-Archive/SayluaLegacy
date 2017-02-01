import json
import os

## Reasons

class InvalidScriptName(Exception):
    pass


class InvalidSchemaJSON(Exception):
    pass


#class InvalidTraitName(Exception):
#   pass


def read_schema(schema_location):
    """Read schema into a list of appropriately namespaced dicts.
    """

    namespaced_files = []

    for root, dirs, files in os.walk(schema_location):
        if root != schema_location:
            # Determine our namespace from the directory name
            file_type = os.path.split(root)[-1]

            for file in files:
                file_path = os.path.join(root, file)
                file_object = None
                stripped_name = file.split('.')[0]

                # Read our file into an object, append object to output list.
                with open(file_path, 'r') as f:
                    content = f.read()
                    file_object = {
                        'name': stripped_name,
                        'content': content,
                        'namespace': file_type
                    }

                namespaced_files.append(file_object)

    return namespaced_files


def interpret_schema(namespaced_files):
    """Resolves dynamic variables denoted with '$' into their respective
    values if a matching entry is found within the namespace.

    Currently limited to script related keys located within 'events'.
    """

    for file in namespaced_files:
        if file.get('namespace') in ['entities', 'scripts', 'tiles', 'traits']:
            content = json.reads(file.get('content'))

            if content.get('events'):
                # Keep track of which keys we should remove
                prune_keys = []

                for event in content.get('events'):
                    if event.startswith('$'):
                        # We must search for a matching script.
                        target_name = namespaced_files['events'][event]
                        stripped_event = event[1:]
                        results = list(filter(lambda x: x.name == target_name, namespaced_files))

                        if len(results) == 1:
                            result = results[0]
                            content['events'][stripped_event] = result.get('content')

                            prune_keys.append(event)

                # Remove interpreted keys
                for key in prune_keys:
                    file['events'].pop(key)

    return namespaced_files


def generate_models_from_schema(schema):
    pass

def provision_dungeon_schema():
    cwd = __file__
    schema_location = os.path.join(cwd, "schema")

    namespaced_files = read_schema(schema_location)
    processed_schemas = interpret_schema(namespaced_files)
    models = generate_models_from_schema(processed_schemas)

    return models
