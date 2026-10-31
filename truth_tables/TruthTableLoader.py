import pandas as pd

def load_truth_table(file: str):


    table = pd.read_csv(file)

    #try:
    #    separator_idx = list(table.columns).index("out")
    #except ValueError:
    #    separator_idx = 0


    truth_table = []
    for i, column_head in enumerate(table.columns):
        column = table.get(column_head)
        for y, value in enumerate(column):
            if len(truth_table) - 1 < y:
                truth_table.append([[],[]])

            # separate into in/output pairs.
            if "in" in column_head.lower():
                truth_table[y][0].append(value)
            elif "out" in column_head.lower():
                truth_table[y][1].append(value)


    print(truth_table)
    return truth_table

    #print(len(table.columns))
    #one = table.get(table.columns[2])
    #print(one)





if __name__ == '__main__':
    load_truth_table("C:/Users/sheog/Desktop/n0scrs7t.csv", 2)