from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

def func(x):
    return x + 2


def test_answer():
    assert func(3) == 5

def test_validation_jsonschema_false():
    assert check_validate(instance={"name" : "Eggs", "price" : '34.99'}, schema=schema) == False

def test_validation_jsonschema():
    assert check_validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema) == True



def check_validate(instance, schema):
    try:
        validate(instance= instance, schema = schema)
        return True
    
    except:
        return False

