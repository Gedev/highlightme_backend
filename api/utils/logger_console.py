def print_start_message(message):
    border_length = len(message) + 8

    top_bottom_border = '*' * (border_length + 4)

    middle_border = '*' + ' ' * (border_length + 2) + '*'

    formatted_message = f"""
    {top_bottom_border}
    {middle_border}
    *  ** {message} **  *
    {middle_border}
    {top_bottom_border}
    """

    print(formatted_message)

