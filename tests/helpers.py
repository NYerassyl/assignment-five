def headers(user_id: int) -> dict[str, str]:
    return {"X-User-Id": str(user_id)}


from storage import CompletionRecord, Storage, SubmissionRecord, UserRecord, hash_password


def populated_store(store=None):
    store = store or Storage()
    ada = UserRecord(
        id=store.new_user_id(),
        email="ada@worldofcodes.dev",
        nickname="ada",
        password_hash=hash_password("ada-password-1"),
        bio="Learning Python one lesson at a time.",
    )
    grace = UserRecord(
        id=store.new_user_id(),
        email="grace@worldofcodes.dev",
        nickname="grace",
        password_hash=hash_password("grace-password-2"),
        bio="Interested in algorithms and compilers.",
    )
    store.users = {ada.id: ada, grace.id: grace}

    variables = store.lessons[1]
    sum_problem = store.problems[1]
    for catalog in (store.lessons, store.problems):
        for entry in catalog.values():
            entry.author_id = ada.id if entry.id < 3 else grace.id
    store.completions[(ada.id, variables.id)] = CompletionRecord(
        user_id=ada.id, lesson_id=variables.id, xp_awarded=variables.xp_reward
    )
    ada.xp += variables.xp_reward

    accepted = SubmissionRecord(
        id=store.new_submission_id(),
        problem_id=sum_problem.id,
        user_id=ada.id,
        answer="15",
        verdict="ACCEPTED",
        rewarded=True,
        xp_awarded=sum_problem.xp_reward,
        coins_awarded=sum_problem.coin_reward,
        message="Seeded sample submission.",
    )
    store.submissions[accepted.id] = accepted
    ada.xp += sum_problem.xp_reward
    ada.coins += sum_problem.coin_reward

    return store
