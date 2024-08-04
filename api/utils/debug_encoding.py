# report/utils.py

def inspect_data(data):
    """
    Inspect data items for encoding issues and log any UnicodeEncodeError.
    """
    for item in data:
        try:
            # Attempt to print the data item
            print(f"Data item: {item}")
        except UnicodeEncodeError as e:
            # Log encoding error details
            print(f"Encoding error for item: {item} - {e}")
            # Display sanitized item with non-ASCII characters ignored
            sanitized_item = item.encode('utf-8', 'ignore').decode('utf-8')
            print(f"Sanitized problematic item: {sanitized_item}")

