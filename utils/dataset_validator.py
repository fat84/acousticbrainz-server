from flask_uuid import UUID_RE

DATASET_NAME_LEN_MIN = 1
DATASET_NAME_LEN_MAX = 100

CLASS_NAME_LEN_MIN = 1
CLASS_NAME_LEN_MAX = 100


def validate(dataset):
    """Validator for datasets.

    Dataset must have the following structure:
    {
        - name (string)
        - description (string, optional)
        - classes (list of class dicts)
            {
                - name (string)
                - description (string, optional)
                - recordings (list of UUIDs)
            }
    }

    Complete dataset must contain at least two classes with two recordings in
    each class.

    Args:
        dataset: Dataset stored in a dictionary.

    Raises:
        ValidationException: A general exception for validation errors.
        IncompleteDatasetException: Raised in cases when one of "completeness"
            requirements is not satisfied.
    """
    if not isinstance(dataset, dict):
        raise ValidationException("Dataset must be a dictionary.")
    _check_dict_structure(dataset, ["name", "description", "classes", "public"])

    # Name
    if "name" not in dataset:
        raise ValidationException("Dataset must have a name.")
    if not isinstance(dataset["name"], basestring):
        raise ValidationException("Class name must be a string.")
    if not (DATASET_NAME_LEN_MIN < len(dataset["name"]) < DATASET_NAME_LEN_MAX):
        raise ValidationException("Class name must be between %s and %s characters" %
                                  (DATASET_NAME_LEN_MIN, DATASET_NAME_LEN_MAX))

    # Description (optional)
    if "description" in dataset and dataset["description"] is not None:
        if not isinstance(dataset["description"], basestring):
            raise ValidationException("Description must be a string.")
        # TODO: Do we need to check the length there?

    # Classes
    if "classes" not in dataset:
        raise ValidationException("Dataset must have a list of classes.")
    _validate_classes(dataset["classes"])

    # Publicity
    if "public" not in dataset:
        raise ValidationException("You need to specify if dataset is public or not.")
    if not isinstance(dataset["public"], bool):
        raise ValidationException('Value "public" must be a boolean.')


def _validate_classes(classes):
    if not isinstance(classes, list):
        raise ValidationException("Classes need to be in a list.")
    for cls in classes:
        _validate_class(cls)


def _validate_class(cls):
    if not isinstance(cls, dict):
        raise ValidationException("Class must be a dictionary.")
    _check_dict_structure(cls, ["name", "description", "recordings"])

    # Name
    if "name" not in cls:
        raise ValidationException("Each class must have a name.")
    if not isinstance(cls["name"], basestring):
        raise ValidationException("Class name must be a string.")
    if not (CLASS_NAME_LEN_MIN < len(cls["name"]) < CLASS_NAME_LEN_MAX):
        raise ValidationException("Class name must be between %s and %s characters" %
                                  (CLASS_NAME_LEN_MIN, CLASS_NAME_LEN_MIN))

    # Description (optional)
    if "description" in cls and cls["description"] is not None:
        if not isinstance(cls["description"], basestring):
            raise ValidationException("Description must be a string.")
        # TODO: Do we need to check the length there?

    # Recordings
    if "recordings" not in cls:
        raise ValidationException("Each class must have a list of recordings.")
    _validate_recordings(cls["recordings"])


def _validate_recordings(recordings):
    if not isinstance(recordings, list):
        raise ValidationException("Recordings need to be in a list.")
    for recording in recordings:
        if not UUID_RE.match(recording):
            raise ValidationException('"%s" is not a valid recording MBID.' % recording)


def _check_dict_structure(dictionary, allowed_keys):
    for key in dictionary.iterkeys():
        if key not in allowed_keys:
            raise ValidationException("Unexpected item: %s." % key)


class ValidationException(Exception):
    """Base class for dataset validation exceptions."""
    pass
