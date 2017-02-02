import json
import os

## Reasons

class InvalidScriptName(Exception):
    pass


class InvalidSchemaJSON(Exception):
    pass


class InvalidTraitName(Exception):
    pass


class InvalidSchemaType(Exception):
    pass


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

    Most functionality disabled due to the addition of SQLALchemy.
    Remains for posterity and possible future use.
    """

    for i, file in enumerate(namespaced_files):
        if file.get('namespace') in ['entities', 'tiles', 'traits']:
            try:
                content = json.loads(file.get('content'))
            except json.decoder.JSONDecodeError as e:
                raise InvalidSchemaJSON(str(e))

#            # Determine if we need to replace dynamic variables
#            if content.get('events'):
#                # Keep track of which keys we should remove
#                prune_keys = []
#
#                for event in content.get('events'):
#                    if event.startswith('$'):
#                        # We must search for a matching script.
#                        target_name = content['events'][event]
#                        stripped_event = event[1:]
#                        results = list(filter(
#                            lambda x: (x.name == target_name and x.namespace == 'scripts'),
#                            namespaced_files
#                        ))
#
#                        if len(results) == 1:
#                            result = results[0]
#                            content['events'][stripped_event] = result.get('content')
#
#                            prune_keys.append(event)
#
#                        else:
#                            raise InvalidScriptName(
#                                'Returned {} results when searching for script \'{}\'.'.format(
#                                    len(results),
#                                    target_name
#                                )
#                            )
#
#                # Remove interpreted keys
#                for key in prune_keys:
#                    file['events'].pop(key)

            # Replace old raw string with JSON-ified content
            namespaced_files[i]['content'] = content

         else:
            # We will make an exception for scripts, but anything else should raise an error.
            if file.get('namespace') != 'scripts':
                raise InvalidSchemaType

    return namespaced_files


def generate_models_from_schema(schema):
    """Returns models from a specific set of dungeon model types.
    """

    ## Reasons
    try:
        from saylua.models.explore.models.db import DungeonScript, DungeonEntity, DungeonTrait
    except ImportError:
        try:
            from ..models.db import DungeonScript, DungeonEntity, DungeonTrait

    models = []

    for scheme in schema:
        if scheme.namespace == "entities":
            pass

def provision_dungeon_schema():
    cwd = __file__
    schema_location = os.path.join(cwd, "schema")

    namespaced_files = read_schema(schema_location)
    processed_schemas = interpret_schema(namespaced_files)
    models = generate_models_from_schema(processed_schemas)

    return models
