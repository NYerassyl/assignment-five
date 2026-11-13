from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    return hashlib.sha256(f"worldofcodes-demo::{password}".encode("utf-8")).hexdigest()


@dataclass
class UserRecord:
    id: int
    email: str
    nickname: str
    password_hash: str
    bio: str = ""
    xp: int = 0
    coins: int = 0
    created_at: datetime = field(default_factory=utcnow)


@dataclass
class LessonRecord:
    id: int
    title: str
    description: str
    level: str
    topic: str
    xp_reward: int
    author_id: int | None
    prerequisite_lesson_id: int | None = None
    published: bool = True
    created_at: datetime = field(default_factory=utcnow)


@dataclass
class CompletionRecord:
    user_id: int
    lesson_id: int
    xp_awarded: int
    completed_at: datetime = field(default_factory=utcnow)


@dataclass
class ProblemRecord:
    id: int
    title: str
    prompt: str
    difficulty: str
    topic: str
    expected_answer: str
    xp_reward: int
    coin_reward: int
    author_id: int | None
    created_at: datetime = field(default_factory=utcnow)


@dataclass
class SubmissionRecord:
    id: int
    problem_id: int
    user_id: int
    answer: str
    verdict: str
    rewarded: bool
    xp_awarded: int
    coins_awarded: int
    message: str
    created_at: datetime = field(default_factory=utcnow)


class Storage:
    def __init__(self) -> None:
        self.lock = RLock()
        self.reset()

    def reset(self) -> None:
        with self.lock:
            self.users: dict[int, UserRecord] = {}
            self.lessons: dict[int, LessonRecord] = {}
            self.completions: dict[tuple[int, int], CompletionRecord] = {}
            self.problems: dict[int, ProblemRecord] = {}
            self.submissions: dict[int, SubmissionRecord] = {}
            self._next_user_id = 1
            self._next_lesson_id = 1
            self._next_problem_id = 1
            self._next_submission_id = 1
            self._seed()

    def new_user_id(self) -> int:
        value = self._next_user_id
        self._next_user_id += 1
        return value

    def new_lesson_id(self) -> int:
        value = self._next_lesson_id
        self._next_lesson_id += 1
        return value

    def new_problem_id(self) -> int:
        value = self._next_problem_id
        self._next_problem_id += 1
        return value

    def new_submission_id(self) -> int:
        value = self._next_submission_id
        self._next_submission_id += 1
        return value

    def _seed(self) -> None:
        variables = LessonRecord(
            id=self.new_lesson_id(),
            title="Python Variables and Types",
            description="Create variables and inspect the four core Python types.",
            level="beginner",
            topic="basics",
            xp_reward=20,
            author_id=None,
        )
        loops = LessonRecord(
            id=self.new_lesson_id(),
            title="Lists and Loops",
            description="Store sequences and iterate over them with for and while loops.",
            level="beginner",
            topic="collections",
            xp_reward=30,
            author_id=None,
            prerequisite_lesson_id=variables.id,
        )
        functions = LessonRecord(
            id=self.new_lesson_id(),
            title="Dictionaries and Functions",
            description="Model key-value data and move it through reusable functions.",
            level="intermediate",
            topic="functions",
            xp_reward=40,
            author_id=None,
            prerequisite_lesson_id=loops.id,
        )
        self.lessons = {lesson.id: lesson for lesson in (variables, loops, functions)}

        sum_problem = ProblemRecord(
            id=self.new_problem_id(),
            title="Sum of a List",
            prompt="What is sum([1, 2, 3, 4, 5])?",
            difficulty="easy",
            topic="basics",
            expected_answer="15",
            xp_reward=10,
            coin_reward=2,
            author_id=None,
        )
        reverse_problem = ProblemRecord(
            id=self.new_problem_id(),
            title="Reverse a String",
            prompt="Which slice returns 'abc' reversed?",
            difficulty="easy",
            topic="strings",
            expected_answer="[::-1]",
            xp_reward=15,
            coin_reward=3,
            author_id=None,
        )
        lookup_problem = ProblemRecord(
            id=self.new_problem_id(),
            title="Safe Dictionary Lookup",
            prompt="What does {'a': 1}.get('b', 0) return?",
            difficulty="medium",
            topic="dictionaries",
            expected_answer="0",
            xp_reward=25,
            coin_reward=5,
            author_id=None,
        )
        self.problems = {
            problem.id: problem
            for problem in (sum_problem, reverse_problem, lookup_problem)
        }


store = Storage()
