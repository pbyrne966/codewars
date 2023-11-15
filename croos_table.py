from typing import List, Union, List, Dict
from collections import defaultdict

d, _ = 0.5, None
wht_space = " "
newline = "\n"

def sum_array(arr: List[Union[None, float, int]]) -> float:
    return sum(e for e in arr if e is not None)

def set_cache(d: Dict, index: int, table: List[Union[int, float]]) -> float:
    found = d.get(index)
    if found is None:
        found = sum_array(table[index])
        d[index] = found

    return found

def calc_sb(table: List[Union[int, float]]) -> List[Union[int, float]]:
    completed = []
    row_sums: Dict = {}

    for outer, row in enumerate(table):
        sb = 0
        row_sum = set_cache(row_sums, outer, table)
        for inner, value in enumerate(row):
            if value in [None, 0] or inner == outer:
                continue
            found_value = set_cache(row_sums, inner, table)
            sb += found_value * value
        completed.append(
            [e for e in row if e is not None] + [row_sum, sb]
        )
    
    return completed

def complex_sort(as_pairs: Dict[str, List]) -> Dict[str, List[Union[int, float]]]:
    scores_dict = defaultdict(list)    

    for key, values in as_pairs.items():
        sort_on = (values[-2] , values[-1])
        scores_dict[sort_on].append({key: values})

    sorted_dict = {}
    for score in sorted(scores_dict.keys(), reverse=True):
        results: List[Dict] = scores_dict[score]
        sorted_dict.update({
            key: value for d  in results
            for key, value in d.items()
        })
    
    return sorted_dict

def make_value_entry(skip_entry ,values):
    to_insert = []
    val_len = len(values) - 1
    for idx, val in enumerate(values):
        is_float = isinstance(val, float)
        if is_float:
            if val == 0.5:
                entry = "=" + wht_space
            elif idx == val_len:
                entry =  f"{val:.2f}" + newline
            else:
                entry = wht_space + f"{val:.1f}" + wht_space * 2
                to_insert = to_insert[::-1]
        else:
            entry = str(val) + wht_space
        to_insert.append(entry)

    to_insert.insert(skip_entry, '  ')
    as_str = "".join(to_insert)
    return as_str 

def create_string(sorted_dict: Dict) -> str:
    player_count = [str(idx) + wht_space for idx, _ in enumerate(sorted_dict, start=1)]
    player_header = "#  Player           "
    header = "".join([player_header, *player_count, " Pts   ", "SB\n"])
    split = "=" * (sum(len(strs) for strs in header)) + newline
    retrun_arr = [header, split]

    skip_index, rank_number, last_seen_pair = 0, 1, None

    for k, v in sorted_dict.items():
        score = tuple(v[-2:])
        rank = str(rank_number) if last_seen_pair != score else wht_space
        padded_name = rank + wht_space * 2 + k
        player_entry = padded_name + wht_space * (len(player_header) - len(padded_name) - 1)
        retrun_arr.append(player_entry + wht_space + make_value_entry(skip_index, v))
        last_seen_pair, rank_number, skip_index = score, rank_number + 1, skip_index + 1
    
    return "".join(retrun_arr)

def crosstable(
        players: List[str],
        results: List[List[Union[float, int]]]):

    sb = calc_sb(results) 
    as_pair = dict(zip(players, sb))
    sorted_data = complex_sort(as_pair)
    return create_string(sorted_data)


def do_test(players, results, expected):
    actual = crosstable(players, results)
    print(actual)
    print(expected)
    # if actual != expected:
        # print("crosstable({!r}, {!r})\n\nactual:\n{}\n\nexpected:\n{}".format(players, results, actual, expected))
    #     test.assert_equals(actual.count('\n') + 1, expected.count('\n') + 1, "There should be {} lines".format(expected.count('\n') + 1))
        # for i, (actual_line, expected_line) in enumerate(zip(actual.split('\n'), expected.split('\n')), 1):
        #     if actual_line != expected_line:
        #         print("*"*10)
        #         print("found line:{!r}".format(actual_line))
        #         print("other line:{!r}".format(expected_line))
        #         print("*"*10)
    #             test.assert_equals(actual_line, expected_line, "line {}".format(i))
    # test.assert_equals(actual, expected)

d, _ = 0.5, None

do_test([
    "Emmett Frost", "Cruz Sullivan", "Deandre Bullock", "George Bautista", "Norah Underwood", "Renee Preston"], [
    [_, 1, 0, 0, d, 0],
    [0, _, d, 1, 0, 0],
    [1, d, _, d, d, d],
    [1, 0, d, _, d, d],
    [d, 1, d, d, _, d],
    [1, 1, d, d, d, _]],
    "#  Player           1 2 3 4 5 6  Pts   SB\n"
    "==========================================\n"
    "1  Renee Preston      = = = 1 1  3.5  7.25\n"
    "2  Deandre Bullock  =   = = = 1  3.0  6.75\n"
    "   Norah Underwood  = =   = 1 =  3.0  6.75\n"
    "4  George Bautista  = = =   0 1  2.5  6.25\n"
    "5  Cruz Sullivan    0 = 0 1   0  1.5  4.00\n"
    "6  Emmett Frost     0 0 = 0 1    1.5  3.00")

# do_test([
#     'Ana Gill', 'Alan Benitez', 'Lina Estes', 'Greta Kline', 'Simone Kelly', 'Quinn Sexton', 'India Cooper',
#     'Ashton Richardson'], [
#     [_, 0, 1, d, d, d, 0, 1],
#     [1, _, 0, d, 1, d, 0, 0],
#     [0, 1, _, d, 0, 1, 1, 1],
#     [d, d, d, _, 1, 1, d, 0],
#     [d, 0, 1, 0, _, d, d, d],
#     [d, d, 0, 0, d, _, 1, d],
#     [1, 1, 0, d, d, 0, _, d],
#     [0, 1, 0, 1, d, d, d, _]],
#     "#  Player             1 2 3 4 5 6 7 8  Pts   SB\n"
#     "=================================================\n"
#     "1  Lina Estes           = 0 1 1 0 1 1  4.5  15.00\n"
#     "2  Greta Kline        =   = = 0 1 = 1  4.0  13.25\n"
#     "3  Ana Gill           1 =   0 1 = 0 =  3.5  13.00\n"
#     "4  India Cooper       0 = 1   = = 1 0  3.5  11.75\n"
#     "   Ashton Richardson  0 1 0 =   = 1 =  3.5  11.75\n"
#     "6  Simone Kelly       1 0 = = =   0 =  3.0  11.25\n"
#     "7  Alan Benitez       0 = 1 0 0 1   =  3.0  10.00\n"
#     "   Quinn Sexton       0 0 = 1 = = =    3.0  10.00")

# do_test([
#     'Trystan Randall', 'Pamela Glass', 'Coleman Serrano', 'Brycen Beasley', 'Wayne Allison', 'Natalia Powell',
#     'Carlos Koch', 'Emilio Mejia', 'Lennon Rollins', 'Madilynn Huerta'], [
#     [_, 1, 1, 0, 1, 1, d, d, 0, 1],
#     [0, _, d, 0, d, d, 1, 0, 1, 0],
#     [0, d, _, 0, 0, d, 0, 0, 1, 1],
#     [1, 1, 1, _, d, 1, d, 1, 1, d],
#     [0, d, 1, d, _, 0, d, 0, d, d],
#     [0, d, d, 0, 1, _, 1, 1, 1, d],
#     [d, 0, 1, d, d, 0, _, 0, d, d],
#     [d, 1, 1, 0, 1, 0, 1, _, d, d],
#     [1, 0, 0, 0, d, 0, d, d, _, 0],
#     [0, 1, 0, d, d, d, d, d, 1, _]],
#     " #  Player            1  2  3  4  5  6  7  8  9 10  Pts   SB\n"
#     "==============================================================\n"
#     " 1  Brycen Beasley       1  1  1  =  =  =  1  1  1  7.5  31.75\n"
#     " 2  Trystan Randall   0     1  =  1  =  1  1  1  0  6.0  24.50\n"
#     " 3  Natalia Powell    0  0     1  =  1  1  =  =  1  5.5  20.50\n"
#     " 4  Emilio Mejia      0  =  0     =  1  1  1  1  =  5.5  20.00\n"
#     " 5  Madilynn Huerta   =  0  =  =     =  =  1  0  1  4.5  18.75\n"
#     " 6  Carlos Koch       =  =  0  0  =     =  0  1  =  3.5  15.00\n"
#     " 7  Wayne Allison     =  0  0  0  =  =     =  1  =  3.5  13.75\n"
#     " 8  Pamela Glass      0  0  =  0  0  1  =     =  1  3.5  12.00\n"
#     " 9  Coleman Serrano   0  0  =  0  1  0  0  =     1  3.0  11.50\n"
#     "10  Lennon Rollins    0  1  0  =  0  =  =  0  0     2.5  12.25")

# do_test([
#     'K. Kel', 'A. Vau', 'Z. Aya', 'J. Coc', 'M. Hue', 'A. Sim', 'C. Yan', 'J. Wal',
#     'M. Hor', 'L. Ell', 'H. Mic', 'P. Bla', 'L. Lan', 'M. Rid', 'M. Bec', 'J. Gat'], [
#     [_, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, _, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     [1, 1, _, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, _, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 0, 1, _, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
#     [1, 1, 1, 1, 0, _, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 1, 0, _, 1, 0, 0, 0, 0, 0, 1, 0, 0],
#     [1, 1, 1, 1, 1, 1, 0, _, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, _, 0, 0, 1, 0, 1, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, _, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, _, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, _, 0, 0, 0, 0],
#     [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, _, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, _, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 0],
#     [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _]],
#     " #  Player   1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16  Pts     SB\n"
#     "=========================================================================\n"
#     " 1  J. Gat      1  1  1  1  1  1  1  0  1  1  1  1  1  1  1  14.0  100.00\n"
#     " 2  M. Bec   0     1  1  1  1  1  1  1  1  1  1  1  1  1  1  14.0   92.00\n"
#     " 3  M. Rid   0  0     1  0  1  1  1  1  0  1  1  1  1  1  1  11.0   65.00\n"
#     " 4  L. Lan   0  0  0     1  1  1  1  0  1  1  1  1  1  1  1  11.0   64.00\n"
#     " 5  M. Hor   0  0  1  0     0  1  0  1  1  1  1  1  1  1  1  10.0   53.00\n"
#     " 6  H. Mic   0  0  0  0  1     0  1  1  1  1  1  1  1  0  1   9.0   50.00\n"
#     " 7  P. Bla   0  0  0  0  0  1     1  0  1  1  1  1  1  1  1   9.0   45.00\n"
#     " 8  L. Ell   0  0  0  0  1  0  0     1  1  1  1  1  1  1  1   9.0   43.00\n"
#     " 9  M. Hue   1  0  0  1  0  0  1  0     0  0  1  0  0  1  1   6.0   43.00\n"
#     "10  C. Yan   0  0  1  0  0  0  0  0  1     1  0  0  1  1  1   6.0   30.00\n"
#     "11  J. Wal   0  0  0  0  0  0  0  0  1  0     1  1  1  1  1   6.0   21.00\n"
#     "12  A. Sim   0  0  0  0  0  0  0  0  0  1  0     1  1  1  1   5.0   16.00\n"
#     "13  K. Kel   0  0  0  0  0  0  0  0  1  1  0  0     0  0  1   3.0   14.00\n"
#     "14  Z. Aya   0  0  0  0  0  0  0  0  1  0  0  0  1     1  0   3.0   11.00\n"
#     "15  A. Vau   0  0  0  0  0  1  0  0  0  0  0  0  1  0     0   2.0   12.00\n"
#     "16  J. Coc   0  0  0  0  0  0  0  0  0  0  0  0  0  1  1      2.0    5.00")

# do_test([
#     "Harry Pillsbury", "Mikhail Chigorin", "Emanuel Lasker", "Siegbert Tarrasch", "William Steinitz",
#     "Emanuel Schiffers", "Curt Bardeleben", "Richard Teichmann", "Carl Schlechter", "Joseph Blackburne",
#     "Carl Walbrodt", "David Janowski", "James Mason", "Amos Burn", "Isidor Gunsberg", "Henry Bird", "Adolf Albin",
#     "Georg Marco", "William Pollock", "Jacques Mieses", "Samuel Tinsley", "Beniamino Vergani"], [
#     [_, 0, 0, 1, 1, 1, 1, 1, 0, d, d, 1, 1, 1, 1, 1, 1, d, 1, 1, 1, 1],
#     [1, _, 1, 1, 0, 0, 1, 1, 1, 1, d, 0, 1, 1, 1, d, d, 1, 1, d, 1, 1],
#     [1, 0, _, 0, 1, 1, 0, 1, 1, 0, 1, 1, d, 1, 1, 1, d, 1, 1, d, 1, 1],
#     [0, 0, 1, _, 1, 1, d, 0, d, 1, 1, 1, 0, 1, d, 1, 1, 1, 0, d, 1, 1],
#     [0, 1, 0, 0, _, 1, 1, d, d, 1, 1, 0, 1, d, 1, 0, 1, 1, 0, d, 1, 1],
#     [0, 1, 0, 0, 0, _, d, d, 0, 1, 1, 1, d, d, 1, 1, 0, d, 1, d, 1, 1],
#     [0, 0, 1, d, 0, d, _, d, d, 0, 0, d, 1, 1, 1, d, d, 1, 1, 1, 0, 1],
#     [0, 0, 0, 1, d, d, d, _, d, 0, 0, d, 1, 1, 0, 1, d, 1, d, 1, 1, 1],
#     [1, 0, 0, d, d, 1, d, d, _, d, d, 0, 1, 1, d, d, d, d, d, d, 1, 0],
#     [d, 0, 1, 0, 0, 0, 1, 1, d, _, 0, 1, 0, 1, 0, d, 1, 0, 1, 0, 1, 1],
#     [d, d, 0, 0, 0, 0, 1, 1, d, 1, _, 0, d, 0, d, d, 0, d, d, 1, 1, 1],
#     [0, 1, 0, 0, 1, 0, d, d, 1, 0, 1, _, d, 0, 0, d, 0, 1, d, 1, 0, 1],
#     [0, 0, d, 1, 0, d, 0, 0, 0, 1, d, d, _, 1, 0, 1, d, 0, 1, 1, 0, 1],
#     [0, 0, 0, 0, d, d, 0, 0, 0, 0, 1, 1, 0, _, 0, d, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, d, 0, 0, 0, 1, d, 1, d, 1, 1, 1, _, 0, 1, d, 0, 1, 0, 0],
#     [0, d, 0, 0, 1, 0, d, 0, d, d, d, d, 0, d, 1, _, 1, d, 0, d, d, 1],
#     [0, d, d, 0, 0, 1, d, d, d, 0, 1, 1, d, 0, 0, 0, _, 0, 0, 1, 1, d],
#     [d, 0, 0, 0, 0, d, 0, 0, d, 1, d, 0, 1, 0, d, d, 1, _, 1, 1, 0, d],
#     [0, 0, 0, 1, 1, 0, 0, d, d, 0, d, d, 0, 0, 1, 1, 1, 0, _, 0, 0, 1],
#     [0, d, d, d, d, d, 0, 0, d, 1, 0, 0, 0, 0, 0, d, 0, 0, 1, _, 1, 1],
#     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, d, 0, 1, 1, 0, _, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, d, d, 0, 0, 0, _]],
#     " #  Player              1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22  Pts     SB\n"
#     "======================================================================================================\n"
#     " 1  Harry Pillsbury        0  0  1  1  1  1  1  0  =  =  1  1  1  1  1  1  =  1  1  1  1  16.5  157.50\n"
#     " 2  Mikhail Chigorin    1     1  1  0  0  1  1  1  1  =  0  1  1  1  =  =  1  1  =  1  1  16.0  163.00\n"
#     " 3  Emanuel Lasker      1  0     0  1  1  0  1  1  0  1  1  =  1  1  1  =  1  1  =  1  1  15.5  150.75\n"
#     " 4  Siegbert Tarrasch   0  0  1     1  1  =  0  =  1  1  1  0  1  =  1  1  1  0  =  1  1  14.0  136.00\n"
#     " 5  William Steinitz    0  1  0  0     1  1  =  =  1  1  0  1  =  1  0  1  1  0  =  1  1  13.0  125.75\n"
#     " 6  Emanuel Schiffers   0  1  0  0  0     =  =  0  1  1  1  =  =  1  1  0  =  1  =  1  1  12.0  111.50\n"
#     " 7  Curt Bardeleben     0  0  1  =  0  =     =  =  0  0  =  1  1  1  =  =  1  1  1  0  1  11.5  108.25\n"
#     " 8  Richard Teichmann   0  0  0  1  =  =  =     =  0  0  =  1  1  0  1  =  1  =  1  1  1  11.5  105.25\n"
#     " 9  Carl Schlechter     1  0  0  =  =  1  =  =     =  =  0  1  1  =  =  =  =  =  =  1  0  11.0  115.50\n"
#     "10  Joseph Blackburne   =  0  1  0  0  0  1  1  =     0  1  0  1  0  =  1  0  1  0  1  1  10.5  102.75\n"
#     "11  Carl Walbrodt       =  =  0  0  0  0  1  1  =  1     0  =  0  =  =  0  =  =  1  1  1  10.0   95.25\n"
#     "12  David Janowski      0  1  0  0  1  0  =  =  1  0  1     =  0  0  =  0  1  =  1  0  1   9.5   93.75\n"
#     "13  James Mason         0  0  =  1  0  =  0  0  0  1  =  =     1  0  1  =  0  1  1  0  1   9.5   89.25\n"
#     "14  Amos Burn           0  0  0  0  =  =  0  0  0  0  1  1  0     0  =  1  1  1  1  1  1   9.5   79.50\n"
#     "15  Isidor Gunsberg     0  0  0  =  0  0  0  1  =  1  =  1  1  1     0  1  =  0  1  0  0   9.0   88.25\n"
#     "16  Henry Bird          0  =  0  0  1  0  =  0  =  =  =  =  0  =  1     1  =  0  =  =  1   9.0   84.25\n"
#     "17  Adolf Albin         0  =  =  0  0  1  =  =  =  0  1  1  =  0  0  0     0  0  1  1  =   8.5   85.50\n"
#     "18  Georg Marco         =  0  0  0  0  =  0  0  =  1  =  0  1  0  =  =  1     1  1  0  =   8.5   79.25\n"
#     "19  William Pollock     0  0  0  1  1  0  0  =  =  0  =  =  0  0  1  1  1  0     0  0  1   8.0   77.50\n"
#     "20  Jacques Mieses      0  =  =  =  =  =  0  0  =  1  0  0  0  0  0  =  0  0  1     1  1   7.5   74.25\n"
#     "21  Samuel Tinsley      0  0  0  0  0  0  1  0  0  0  0  1  1  0  1  =  0  1  1  0     1   7.5   63.50\n"
#     "22  Beniamino Vergani   0  0  0  0  0  0  0  0  1  0  0  0  0  0  1  0  =  =  0  0  0      3.0   28.50")
        