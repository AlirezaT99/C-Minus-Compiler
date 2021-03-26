def get_next_token(cursor):
    return '', 0


def read_all_tokens(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    print(lines)
    for line_number, line in zip(range(1, len(lines) + 1), lines):
        cursor = 0
        while True:
            if (line_number == len(lines) and cursor == len(line) - 1) \
                    or (line_number != len(lines) and cursor == len(line) - 3):
                break
            token, cursor = get_next_token(cursor)
