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

def prepare(context: str) -> dict:
    dict_answers = {}
    
    # Split by newline and ignore empty strings immediately
    lines = [line for line in context.split("\n") if line.strip() != ""]
    
    for line in lines:
        # Split on the FIRST space only to separate the number from the answers
        parts = line.strip().split(' ', 1)
        
        # Ensure we actually have a number and an answer part
        if len(parts) == 2:
            key_num = parts[0]
            answers_string = parts[1]
            
            key = f"question{key_num}"
            
            if answers_string.strip()[-1] == '*':
                dict_answers[key] = [variant.strip() if not variant.strip()[-1] == "*" else variant.strip()[0:len(variant)-1].strip() for variant in answers_string.split("/")]

            else:
                # Split by "/", strip whitespace from each, and assign the list
                tepm = []
                for variant in answers_string.split('/'):
                    tepm.append(variant.strip())
                    tepm.append(variant.strip().upper())
                    tepm.append(variant.strip().lower())
                    tepm.append(variant.strip().capitalize())
                dict_answers[key] = tepm
    return dict_answers

if __name__ == "__main__":
    """representation code"""

    string = "1 A\n2 B\n3 Battle/War * \n4 Car \n5 Rabbit \n6hello \n7 A/ C /D \n8 111 \nxhnsa \n9 Catch * \n 10 PhoNe"
    print(prepare(string))