import json
import os


class InvalidAnimationName(Exception):
    pass


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
                        'name': "{}_{}".format(file_type, stripped_name),
                        'content': content,
                        'type': file_type
                    }

                namespaced_files.append(file_object)

    return namespaced_files


def interpret_schema(namespaced_files):
    """Validates and translates file contents to JSON.
    """

    for i, file in enumerate(namespaced_files):
        if file.get('type') in ['entity', 'tile', 'trait', 'animation']:
            try:
                content = json.loads(file.get('content'))
            except json.decoder.JSONDecodeError as e:
                raise InvalidSchemaJSON(str(e))

            # Replace old raw string with JSON-ified content
            namespaced_files[i]['content'] = content

        else:
            # We will make an exception for scripts, but anything else should raise an error.
            if file.get('type') != 'script':
                raise InvalidSchemaType

    return namespaced_files


# TODO: Account for inlined scripts, or explicitly error when used.
def generate_models_from_schema(schema):
    """Returns models from a specific set of dungeon model types.
    """

    def find_animation(target_name, schema):
        target = [x for x in schema if (x.get('type') == 'animation' and x.get('name') == target_name)]

        if len(target) == 1:
            return target[0]

        else:
            raise InvalidAnimationName(
                'Returned {} results when searching for animation \'{}\'.'.format(
                    len(target),
                    target_name
                )
            )

    def find_script(target_name, models):
        target = [x for x in models if (x.__tablename__ == 'dungeon_scripts' and x.name == target_name)]

        if len(target) == 1:
            return target[0]

        else:
            raise InvalidScriptName(
                'Returned {} results when searching for script \'{}\'.'.format(
                    len(target),
                    target_name
                )
            )

    def find_trait(target_name, models):
        target = [x for x in models if (x.__tablename__ == 'dungeon_traits' and x.name == target_name)]

        if len(target) == 1:
            return target[0]

        else:
            raise InvalidTraitName(
                'Returned {} results when searching for trait \'{}\'.'.format(
                    len(target),
                    target_name
                )
            )

    try:
        from saylua.modules.explore.models.db import (
            DungeonScript, DungeonScriptWrapper,
            DungeonTrait, DungeonEntity,
            DungeonTile
        )

    except ImportError:
        try:
            from ..models.db import DungeonScript, DungeonScriptWrapper, DungeonTrait, DungeonEntity, DungeonTile
        except ImportError:
            raise

    models = []

    # Scripts first
    for scheme in [x for x in schema if x.get('type') == 'script']:
        script = DungeonScript(name=scheme.get('name'), content=scheme.get('content'))
        models.append(script)

    # Traits second
    for scheme in [x for x in schema if x.get('type') == 'trait']:
        content = scheme.get('content')

        # Define our base Trait
        trait = DungeonTrait(
            name=scheme.get('name'),
            display_name=content.get('name'),
            description=content.get('description'),
            meta=content.get('meta')
        )

        for event in content.get('events', []):
            if event.startswith('$'):
                # We need to find the specified script
                target_name = content['events'][event]
                target = find_script(target_name, models)

                # Get proper name, create wrapper
                stripped_name = event[1:]
                wrapper = DungeonScriptWrapper(event_name=stripped_name, event_script=[target])

                # Store wrapper
                trait.events.append(wrapper)
                models.append(wrapper)

        models.append(trait)

    # Entities third
    for scheme in [x for x in schema if x.get('type') == 'entity']:
        content = scheme.get('content')

        # Define our base Entity
        entity = DungeonEntity(
            name=scheme.get('name'),
            display_name=content.get('name'),
            description=content.get('description'),
            type=content.get('type'),
            meta=content.get('meta')
        )

        for event in content.get('events', []):
            if event.startswith('$'):
                # We need to find the specified script
                target_name = content['events'][event]
                target = find_script(target_name, models)

                # Get proper name, create wrapper
                stripped_name = event[1:]
                wrapper = DungeonScriptWrapper(event_name=stripped_name, event_script=[target])

                # Store wrapper
                entity.events.append(wrapper)
                models.append(wrapper)

        for event in content.get('traits', []):
            if event.startswith('$'):
                target_name = content['events'][event]
                target = find_trait(target_name, models)

                # Store trait
                entity.traits.append(target)

        if content.get('$animations'):
            target_name = content.get('$animations')
            target = find_animation(target_name, schema)

            entity.animations = target.get('content')

        models.append(entity)

    # Tiles come last.
    for scheme in [x for x in schema if x.get('type') == 'tile']:
        content = scheme.get('content')

        # Define our base Tile
        tile = DungeonTile(
            name=scheme.get('name'),
            display_name=content.get('name'),
            description=content.get('description'),
            type=content.get('type'),
            meta=content.get('meta')
        )

        for event in content.get('events', []):
            if event.startswith('$'):
                # We need to find the specified script
                target_name = content['events'][event]
                target = find_script(target_name, models)

                # Get proper name, create wrapper
                stripped_name = event[1:]
                wrapper = DungeonScriptWrapper(event_name=stripped_name, event_script=[target])

                # Store wrapper
                tile.events.append(wrapper)
                models.append(wrapper)

        for event in content.get('traits', []):
            if event.startswith('$'):
                target_name = content['events'][event]
                target = find_trait(target_name, models)

                # Store trait
                tile.traits.append(target)

        models.append(tile)

    return models


def provision_dungeon_schema():
    cwd = os.path.split(__file__)[0]
    schema_location = os.path.join(cwd, "schema")

    namespaced_files = read_schema(schema_location)
    processed_schemas = interpret_schema(namespaced_files)
    models = generate_models_from_schema(processed_schemas)

    return models
