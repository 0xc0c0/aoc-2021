def parse_data(fname=None):
    data = None
    with open(fname) as f:
        data = f.readlines()

    return [int(line.strip()) for line in data]

def main():
    data = parse_data('puzzle_input.txt')
    total_increasing_depth = 0
    for i,depth in enumerate(data):
        if i > 0:
            if depth > data[i-1]:
                total_increasing_depth += 1

    print(f"Total Increasing Depth Levels: {total_increasing_depth}")

    total_increasing_depth_windows = 0
    for i,depth in enumerate(data):
        if i < (len(data) - 2) and i > 0:
            sum = data[i] + data[i+1] + data[i+2]
            prev_sum = data[i-1] + data[i] + data[i+1]
            #if data[i+2] > data[i-1]:   <---- devolves into this, in practice
            if sum > prev_sum:
                total_increasing_depth_windows += 1

    print(f"Total Increasing Depth Window Levels: {total_increasing_depth_windows}")
        


if __name__ == '__main__':
    main()
