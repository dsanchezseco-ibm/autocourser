import requests
import random
import json

def solver(quiz_id, JWT_token, old):
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Authorization": "Bearer " + JWT_token,
        'Content-Type': 'application/json'
    }

    quiz_base_url = "https://yourlearning.ibm.com/api/v3/ibm/userQuizzes/"+quiz_id

    # init test -> get Q&A (PUT)

    test = requests.put(quiz_base_url, headers=headers).json()['data']
    test_q = test['questions']

    if old:
        print("I know this one!")
        with open("QAs/"+quiz_id + ".txt", "r") as infile:
            test_q = json.load(infile)
    else:
        print("Hold on, I'm studying for the quiz....")
        print("I do not know that one.")

    # repeat while < passing_score %
    while (
        100 * (test['correctlyAnsweredQuestionsCount'] /
            test['totalQuestionsCount'] )< test['passingScore']
    ):
        if test['status'] != "In Progress":
           requests.put(quiz_base_url, headers=headers).json()['data']

        # answer randomly all the Q (PUT)
        answered = []
        for q in test_q:
            choice = random.choice(q['answers'])['id']
            answered.append({
                "id": q['id'],
                "choice": choice
            })
            requests.put(
                quiz_base_url + "/answerQuestion/" + q['id'],
                headers=headers,
                data=json.dumps({"answers": choice})
            )

        # evaluate test (PUT)
        test = requests.put(quiz_base_url + "/evaluate",
                            headers=headers, data={}).json()['data']
        test_res_q = test['questions']

        print(str(100 * test['correctlyAnsweredQuestionsCount'] /
              test['totalQuestionsCount']) + " of " + str(test['passingScore']) + "%")

        if not old:
            # compare result with random answers
            new_q = []
            for q_res in test_res_q:
                a = list(filter(lambda x: x['id'] == q_res['id'], answered))[0]
                q = list(filter(lambda x: x['id'] == q_res['id'], test_q))[0]
                # print(q_res['id'], q_res['wasCorrectlyAnswered'], a['choice'])
                if q_res['wasCorrectlyAnswered']:
                    new_q.append({
                        "id": q["id"],
                        "answers": list(filter(lambda x: x['id'] == a['choice'], q['answers']))
                    })
                else:
                    new_q.append({
                        "id": q["id"],
                        "answers": list(filter(lambda x: x['id'] != a['choice'], q['answers']))
                    })

            test_q = new_q

    if not old:
        with open("QAs/"+quiz_id + ".txt", "w") as outfile:
            json.dump(new_q, outfile, indent=4)

    print()
    print("Congrats, you passed!")
    print(str(100 * test['correctlyAnsweredQuestionsCount'] /
              test['totalQuestionsCount']) + " of " + str(test['passingScore']) + "%")
    print()
    input("press a key to continue")