from lab.parser import Parser
import re


def add_coverage(content, props):
    props["coverage"] = 0

    if "Total time:" in content:
        assert "fasb" in content or "Number of plans:" in content
        if "fasb" not in content:
            props["coverage"] = 1
        else:
            "fasb return code: 0\n" in content
            props["coverage"] = 1

    if "Planalyst time" in content:
        assert "fasb" not in content and "Number of plans:" in content
        props["coverage"] = 1


def add_fasb_num_plans(content, props):
    if "Executing fasb script scripts/count-sols.fasb" not in content:
        return

    if props["coverage"] != 1:
        return

    assert "Done!" in content

    match = re.search(r"#\!\n(\d+)\n", content)
    assert match
    props["num_plans"] = int(match.group(1))


def add_fasb_num_facets(content, props):
    if (
        "Executing fasb script scripts/facet-reason.fasb" not in content
        and "Executing fasb script scripts/list-facets.fasb" not in content
    ):
        return

    if props["coverage"] != 1:
        return

    assert "Done!" in content

    if "Executing fasb script scripts/list-facets.fasb" in content:
        match = re.search(r"#\?\n(\d+)\n", content)
        assert match
        props["num_facets"] = int(match.group(1))

        splitted_content = content.split("\n")
        for i, line in enumerate(splitted_content):
            if "::" in line and "?" in line and "#" not in line:
                facets_string = splitted_content[i + 1]
                props["facet_list"] = []
                if facets_string:
                    props["facet_list"] = facets_string.split(" ")
                break

        assert "facet_list" in props
        assert props["num_facets"] == 2 * len(props["facet_list"])

    if "Executing fasb script scripts/facet-reason.fasb" in content:
        splitted_content = content.split("\n")
        facet_prompt_start = [
            x[0] for x in enumerate(splitted_content) if "#??" in x[1]
        ][0]
        props["facet_reason"] = []
        for line in splitted_content[facet_prompt_start + 1 :]:

            if "Done!" in line:
                break
            props["facet_reason"].append(line)

        props["num_facets"] = len(props["facet_reason"])


class CustomParser(Parser):
    def __init__(self):
        Parser.__init__(self)


def get_parser():
    parser = CustomParser()
    parser.add_pattern("num_plans", r"Number of plans: (.+)", type=int)
    parser.add_pattern("total_time", r"Total time: (.+)s", type=float)
    parser.add_pattern("total_time", r"Planalyst time: (.+)s", type=float)
    parser.add_function(add_coverage)
    parser.add_function(add_fasb_num_plans)
    parser.add_function(add_fasb_num_facets)
    return parser
