"""Answer Normalizer
======================

- Create each answer case in a new line;
- Write a digit that represents the answer of that specific number;
- returns a key&value pairs in dictionary; 

Example:
1 A \n
2 Car/Vehicle \n
3 John Smith * \n
4 45 \n
"""

def get_dict_result(answers: str, user_answers: dict) -> dict:
    result = {
        "answers": answers,
        "user_answers": user_answers,
        "assertion": {},
        "correct_count": 0,
        "total_count": 0,
    }

    lines = [
        line.strip()
        for line in answers.splitlines()
        if line.strip()
    ]

    for line in lines:
        question_number, answers_string = line.split(" ", 1)
        question_key = f"question{question_number}"

        variants = {}
        is_correct = False
        if answers_string.endswith("*"):
            for i, variant in enumerate(answers_string.split("/"), start=1):
                variant = variant.strip()

                # * belgisi correct variantni bildiradi
                if variant.endswith("*"):
                    variant = variant[:-1].strip()

                variants[f"variant{i}"] = variant

                user_answer = user_answers.get(question_key, "").strip()

                if variant == user_answer:
                    is_correct = True
        else:
            for i, variant in enumerate(answers_string.split("/"), start=1):
                variant = variant.strip()

                variants[f"variant{i}"] = variant

                user_answer = user_answers.get(question_key, "").strip()

                if variant.lower() == user_answer.lower():
                    is_correct = True

        result["assertion"][question_key] = {
            "user": user_answers.get(question_key, ""),
            "variants": variants,
            "is_correct": int(is_correct),
        }

        if is_correct:
            result["correct_count"] += 1

    result["total_count"] = len(lines)

    return result

def count_correct(user_input: dict, task_answers: str) -> int:
    correct_answers = 0
    lines = [line for line in task_answers.split("\n") if line.strip() != ""]

    for line in lines:
            # Split on the FIRST space only to separate the number from the answers
            parts = line.strip().split(' ', 1)
            
            # Ensure we actually have a number and an answer part
            if len(parts) == 2:
                key_num = parts[0]
                answers_string = parts[1].strip()
                
                key = f"question{key_num}"
                
                if answers_string.strip()[-1] == '*':
                    # dict_answers[key] = [variant.strip() if not variant.strip()[-1] == "*" else variant.strip()[0:len(variant)-1].strip() for variant in answers_string.split("/")]
                    for variant in answers_string.split('/'):
                        variant = variant.strip()
                        if variant[-1] == "*":
                            variant = variant[:-1]

                        if variant == user_input[key]:
                            correct_answers += 1
                            break
                else:
                    # Split by "/", strip whitespace from each, and assign the list
                    for variant in answers_string.split('/'):
                        if variant.lower() == user_input[key].lower():
                            correct_answers += 1
                            break
                    


    return correct_answers

if __name__ == "__main__":
    """representation code"""

    string = "1 A\n2 B\n3 Battle/War * \n4 Car \n5 Rabbit \n6hello \n7 A/ C /D \n8 111 \nxhnsa \n9 Catch * \n 10 PhoNe"
    # print(ge(string))