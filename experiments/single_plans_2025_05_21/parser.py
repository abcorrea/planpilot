from lab.parser import Parser

def add_plan(content, props):
    if props["coverage"] != 1:
        return

    splitted_content = content.split("\n")
    plan_start = [x[0] for x in enumerate(splitted_content) if "Best plan:" in x[1]][0]
    props["plan"] = []
    for line in splitted_content[plan_start + 1 :]:

        if line.startswith("[t="):
            break
        props["plan"].append(line)

    assert props["plan_length"] == len(props["plan"])


class CustomParser(Parser):
    def __init__(self):
        Parser.__init__(self)


def get_parser():
    parser = CustomParser()
    parser.add_function(add_plan)
    return parser
