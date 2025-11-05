import json

def validate_input(a, b):
    """Ensures both inputs are positive integers."""
    if not isinstance(a, int) or not isinstance(b, int) or a <= 0 or b <= 0:
        raise ValueError("Inputs must be positive integers.")

def add(a, b):
    """Supports addition of two positive integers."""
    validate_input(a, b)
    return a + b

def subtract(a, b):
    """Supports subtraction of two positive integers."""
    validate_input(a, b)
    return a - b

def product(a, b):
    """Supports product of two positive integers."""
    validate_input(a, b)
    return a * b

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    It routes the operation based on the 'operation' in the event body.
    """
    try:
        # Assuming the input is passed in the event body (from API Gateway)
        body = json.loads(event['body'])
        operation = body['operation'].lower()
        num1 = body['num1']
        num2 = body['num2']

        result = None
        if operation == 'add':
            result = add(num1, num2)
        elif operation == 'subtract':
            result = subtract(num1, num2)
        elif operation == 'product':
            result = product(num1, num2)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid operation specified.'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({'result': result})
        }

    except ValueError as e:
        # Catches validation errors (non-positive integers)
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        # Catches other potential errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal error: {str(e)}'})
        }

# Structure the directory:
# .
# ├── calculator.py
# └── test_calculator.py