import json
import os
import sys


def gen_index_page(data):
    with open("./index.html") as f:
        reference = f.read()

    desc = data["description"]
    if isinstance(desc, list):
        desc = "\n".join([f"<p>{x}</p>" for x in data["description"]])

    return (
        reference.replace("{{Test Name}}", data["name"])
        .replace("{{Test Start Image}}", f"/tricky-tester/static/img/{data['start_image']}")
        .replace("{{Test Description}}", desc)
        .replace("{{Fist Question}}", f"/tricky-tester/static/{data['folder']}/q0.html")
    )


def gen_question_page(question, answers, qid, qtotal, next_link):
    with open("./question.html") as f:
        reference = f.read()

    new_data = (
        reference
            .replace("{{Question}}", str(question))
            .replace("{{Question Answered}}", str(qid))
            .replace("{{Questions Total}}", str(qtotal))
            .replace("{{Question Number}}", str(qid + 1))
            .replace("{{Next Question Link}}", next_link)
    )

    sections = new_data.split("{{Answer Section}}")
    assert len(sections) == 3
    answer_ref = sections[1]

    new_answer_sections = []

    for i, a in enumerate(answers, 1):
        new_answer_sections.append(answer_ref.replace("{{i}}", str(i)).replace("{{Answer}}", a))

    new_data = "".join([sections[0], *new_answer_sections, sections[2]])
    return new_data


def gen_result(data):
    with open("./result.html") as f:
        reference = f.read()

    result = data["result"]
    if isinstance(result, list):
        result = "\n".join([f"<p>{x}</p>" for x in data["result"]])

    return (
        reference
        .replace("{{Test Name}}", data["name"])
        .replace("{{Test Result}}", result)
        .replace("{{Result Image}}", data["result_image"])
    )


def gen_test(test_config_file):
    data = json.load(open(test_config_file))
    folder = data["folder"]
    index_page = gen_index_page(data)
    with open(f"../static/{folder}/index.html", "w") as f:
        f.write(index_page)

    num_questions = len(data["questions"])

    for idx, question_block in enumerate(data["questions"]):
        next_link = f"/tricky-tester/static/{folder}/q{idx + 1}.html"
        if idx == num_questions - 1:
            next_link = f"/tricky-tester/static/{folder}/result.html"
        qpage = gen_question_page(question_block["question"], question_block["answers"], idx, num_questions, next_link)
        with open(f"../static/{folder}/q{idx}.html", "w") as f:
            f.write(qpage)

    result_page = gen_result(data)
    with open(f"../static/{folder}/result.html", "w") as f:
        f.write(result_page)


if __name__ == '__main__':
    conf = sys.argv[1]
    os.system(f"mkdir ../static/{conf}")
    gen_test(f"./test_data/{conf}.json")
