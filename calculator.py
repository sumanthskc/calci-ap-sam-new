import json

def validate_input(a, b):
    """Ensures both inputs are positive integers."""
    # ... (rest of the validation function remains the same)
    if not isinstance(a, int) or not isinstance(b, int) or a <= 0 or b <= 0:
        raise ValueError("Inputs must be positive integers.")

def add(a, b):
    validate_input(a, b)
    return a + b

def subtract(a, b):
    validate_input(a, b)
    return a - b

def product(a, b):
    validate_input(a, b)
    return a * b

def lambda_handler(event, context):
    """
    AWS Lambda handler function, updated to read from QUERY STRING PARAMETERS.
    """
    try:
        # Check if query string parameters exist
        params = event.get('queryStringParameters')
        if not params:
            raise ValueError("Missing query string parameters (operation, num1, num2).")

        # Extract data from query string parameters
        operation = params.get('operation', '').lower()
        num1 = int(params.get('num1', '0'))
        num2 = int(params.get('num2', '0'))

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
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal error: {str(e)}'})
        }