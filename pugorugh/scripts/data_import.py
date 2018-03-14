import json
from os import environ, path
import sys

import django


# dirname() of dirname() of abspath() should get us
# the folder of the folder of THIS script file.
# so it should get us to the "pugorugh" folder
# because THIS script is contained inside "scripts",
# which is inside "pugorugh".
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

# dirname() moves us up 1-level from BASEDIR
# so dirname() of BASE_DIR gets us up to "backend"s PATH
PROJECT_DIR = path.dirname(BASE_DIR)


# We add this path to the system path, so Django looks within this folder
# for Django path stuff.
sys.path.insert(0, PROJECT_DIR)


def main():
    """
    Imports data from 'dog_details.json',

    Raises an error if DogSerializer does not exist
    inside pugorugh/serializers.py
    """
    try:
        from pugorugh.serializers import DogSerializer
    except ImportError:
        raise ImportError("DogSerializer not implemented in serializers.py")

    # Full path to dog_details.json leveraging
    # Pythons ability to find file path of this script from earlier.
    json_file = path.join(PROJECT_DIR,
                          'pugorugh',
                          'static',
                          'dog_details.json')

    # pass full file path to open()
    with open(json_file, 'r') as file:
        data = json.load(file)
        serializer = DogSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


# A block always good to have for custom scripts or standalone scripts.
# Since this script lives outside of Django.
if __name__ == '__main__':
    # Load/setup environment Python Path for Django
    environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()

    # Call main() to run rest of script to import.
    main()