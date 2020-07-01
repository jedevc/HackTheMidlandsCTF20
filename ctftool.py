#!/usr/bin/env python3

import argparse
import glob
import json
import os
import sys
import re
import traceback
from typing import Any, Dict, Iterable, List, Optional

import colorama
import requests
import yaml
from colorama import Fore, Style

UPSTREAM = "https://raw.githubusercontent.com/jedevc/mini-ctf-tool/master/ctftool.py"


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser("list", help="list all challenges")
    list_parser.add_argument(
        "--verbose", "-v", action="store_true", help="increase verbosity"
    )
    list_parser.set_defaults(func=list_challenges)

    refresh_parser = subparsers.add_parser("validate", help="validate all config files")
    refresh_parser.set_defaults(func=validate_challenges)

    upload_parser = subparsers.add_parser("upload", help="upload all challenges")
    upload_parser.add_argument("url", help="base url of the CTFd instance")
    upload_parser.add_argument(
        "--username", "-u", required=True, help="username for the admin user"
    )
    upload_parser.add_argument(
        "--password", "-p", required=True, help="password for the admin user"
    )
    upload_parser.add_argument(
        "--insecure", "-k", action="store_true", help="do not check ssl certificates"
    )
    upload_parser.set_defaults(func=upload_challenges)

    upgrade_parser = subparsers.add_parser("upgrade", help="upgrade ctftool")
    upgrade_parser.set_defaults(func=upgrade)

    args = parser.parse_args()
    if hasattr(args, "func"):
        success = args.func(args)
        if not success:
            sys.exit(1)
    else:
        parser.print_help()


def list_challenges(args):
    cache = {}
    for challenge in Challenge.load_all(True):
        if challenge.category not in cache:
            cache[challenge.category] = []
        cache[challenge.category].append(challenge)

    for category, challenges in cache.items():
        for challenge in challenges:
            if challenge.error is not None:
                continue

            print(f"[{challenge.category}] ", end="")
            print(f"{Style.BRIGHT}{challenge.name}{Style.RESET_ALL} ", end="")
            print(f"{Fore.LIGHTBLACK_EX}- {challenge.path}")
            if args.verbose:
                INDENT = "\n\t\t"
                description = INDENT + challenge.description.replace("\n", INDENT)

                print(f"\tdescription: {description}")
                print(f"\tpoints: {challenge.points}")
                print(f"\tflags: {challenge.flags}")
                print(f"\tfiles: {challenge.files}")

    return True


def validate_challenges(args):
    success = True

    existing_challenges = set()

    for challenge in Challenge.load_all(True):
        print(challenge.path, end="")

        failed = False

        def fail(message):
            nonlocal failed
            failed = True
            success = False
            print(f"\n{Fore.RED}✗{Style.RESET_ALL} {message}", end="")

        if challenge.error is not None:
            fail(f"challenge parse error ({challenge.error})")
        else:
            if not challenge.name:
                fail("challenge name must not be empty")
            elif not (challenge.name.isdecimal() or challenge.name.isalnum()):
                fail("challenge name must not be alpha-numeric")
            elif challenge.name in existing_challenges:
                fail("challenge name must not be a duplicate")
            else:
                existing_challenges.add(challenge.name)

            if not challenge.category:
                fail("challenge category must not be empty")
            if not (challenge.name.isdecimal() or challenge.name.isalnum()):
                fail("category name must not be alpha-numeric")

            for filename in challenge.files:
                filename_relative = os.path.join(
                    os.path.dirname(challenge.path), filename
                )
                if not os.path.exists(filename_relative):
                    fail(f'challenge file "{filename}" does not exist')

            if len(challenge.flags) == 0:
                fail("challenge must have at least 1 flag")

        if failed:
            print()
        else:
            print(f" {Fore.GREEN}✔{Style.RESET_ALL}")

    return success


def upload_challenges(args):
    ctfd = CTFd(args.url, args.username, args.password, verify=(not args.insecure))
    success = True
    skipped = False

    online_names = [challenge["name"] for challenge in ctfd.list()]
    challenge_data = []

    # upload challenges
    for challenge in Challenge.load_all():
        print(challenge.path, end="")
        if challenge.name in online_names:
            skipped = True
            print(f"{Fore.YELLOW} ~")
            continue

        try:
            cid = ctfd.upload(challenge)
            online_names.append(challenge.name)
            challenge_data.append((cid, challenge))
            print(f"{Fore.GREEN} ✓")
        except Exception as e:
            success = False
            print(f"{Fore.RED} ✗ {e}")

    # apply requirements
    online = ctfd.list()
    for cid, challenge in challenge_data:
        ctfd.requirements(cid, challenge, online)

    if skipped:
        print()
        print(
            Fore.LIGHTBLACK_EX
            + "Some challenges have not been uploaded because a challenge of the same name already existed.",
        )
        print(
            Fore.LIGHTBLACK_EX
            + "To fix this, remove the challenge and try again, or manually modify the challenge using the web tool.",
        )

    return success


def upgrade(args):
    # download new code
    source_code = requests.get(UPSTREAM).text

    # write code
    path = os.path.realpath(__file__)
    with open(path, "w") as ctftool:
        ctftool.write(source_code)


class Challenge:
    """
    Interface to the challenge files and their contained data.
    """

    def __init__(
        self,
        name: str,
        category: str,
        path: Optional[str],
        description: str = "",
        points: int = 0,
        flags: List[str] = None,
        files: List[str] = None,
        requirements: List[str] = None,
        deploy: "Deploy" = None,
    ):
        self.name = name
        self.category = category
        self.path = path
        self.description = description
        self.points = points
        self.flags = flags or []
        self.files = files or []
        self.requirements = requirements or []
        self.deploy = deploy

        self.error: Optional[Exception] = None

    @staticmethod
    def load_all(suppress_errors: bool = False) -> Iterable["Challenge"]:
        globpath = "challenges/**/challenge.*"
        paths = glob.glob(globpath, recursive=True)

        for path in paths:
            yield Challenge.load(path, suppress_errors)

    @staticmethod
    def load(filename: str, suppress_errors: bool = False) -> "Challenge":
        try:
            return Challenge._load(filename)
        except Exception as e:
            if suppress_errors:
                challenge = Challenge("", "", filename)
                challenge.error = e
                return challenge
            else:
                raise

    @staticmethod
    def _load(filename: str) -> "Challenge":
        with open(filename) as f:
            ext = os.path.splitext(filename)[-1]
            if ext == ".yaml" or ext == ".yml":
                data = yaml.safe_load(f)
            elif ext == ".json":
                data = json.load(f)
            else:
                raise ChallengeLoadError(f'unknown file extension "{ext}"')

        chal = Challenge._load_dict(data)
        chal.path = filename
        return chal

    @staticmethod
    def _load_dict(data: Dict[str, Any]) -> "Challenge":
        return Challenge(
            name=data.get("name", ""),
            category=data.get("category", ""),
            path=None,
            description=data.get("description", ""),
            points=data.get("points", 0),
            flags=data.get("flags", []),
            files=data.get("files", []),
            requirements=data.get("requirements", []),
            deploy=Deploy._load_dict(data.get("deploy", {})),
        )


class Deploy:
    def __init__(
        self, docker: bool = False, internalPort: int = 0, externalPort: int = 0
    ):
        self.docker = docker
        self.internalPort = internalPort
        self.externalPort = externalPort

    @staticmethod
    def _load_dict(data: Dict[str, Any]):
        return Deploy(
            docker=data.get("docker", False),
            internalPort=data.get("internalPort", 0),
            externalPort=data.get("externalPort", 0),
        )


class ChallengeLoadError(RuntimeError):
    pass


class CTFd:
    """
    Client for CTFd server.

    This was originally tested with CTFd 2.5.0 on API v1 and should continue
    to work in the future, as long as the API doesn't change too much.

    Note that this is quite hacky - it is near impossible to find any
    documentation on the CTFd api.
    """

    NONCE_EXPRESSION = re.compile(
        "'?csrf_?nonce'?\s*[:=]\s*['\"]([a-zA-Z0-9]*)['\"]", re.IGNORECASE
    )

    def __init__(self, url: str, username: str, password: str, verify: bool = True):
        self.base = url
        self.verify = verify
        self.session = requests.Session()

        self._extract_nonce()

        self.username = username
        self.password = password
        self._login()

        self._extract_nonce()

    def list(self) -> List[Challenge]:
        headers = {"CSRF-Token": self.nonce}

        resp = self.session.get(
            self.base + "/api/v1/challenges?view=admin",
            headers=headers,
            verify=self.verify,
        )
        resp_data = resp.json()
        if "success" in resp_data and resp_data["success"]:
            return resp_data["data"]
        else:
            return []

    def upload(self, challenge: Challenge) -> int:
        headers = {"CSRF-Token": self.nonce}

        # create challenge
        data = {
            "name": challenge.name,
            "category": challenge.category,
            "state": "visible",
            "value": challenge.points,
            "type": "standard",
            "description": challenge.description,
        }
        resp = self.session.post(
            self.base + "/api/v1/challenges",
            headers=headers,
            json=data,
            verify=self.verify,
        )
        resp_data = resp.json()
        if "success" not in resp_data or not resp_data["success"]:
            raise RuntimeError("could not add challenge")
        challenge_id = int(resp_data["data"]["id"])

        # add challenge flags
        for flag in challenge.flags:
            if flag.startswith("/") and flag.endswith("/"):
                data = {
                    "challenge": challenge_id,
                    "content": flag[1:-1],
                    "type": "regex",
                }
            else:
                data = {"challenge": challenge_id, "content": flag, "type": "static"}

            resp = self.session.post(
                self.base + "/api/v1/flags",
                headers=headers,
                json=data,
                verify=self.verify,
            )
            resp_data = resp.json()
            if "success" not in resp_data or not resp_data["success"]:
                raise RuntimeError("could not add flag to challenge")

        # upload challenge files
        if challenge.path:
            for filename in challenge.files:
                fullfilename = os.path.join(os.path.dirname(challenge.path), filename)
                data = {
                    "nonce": self.nonce,
                    "challenge": challenge_id,
                    "type": "challenge",
                }
                files = {"file": (filename, open(fullfilename, "rb"))}

                resp = self.session.post(
                    self.base + "/api/v1/files",
                    data=data,
                    files=files,
                    verify=self.verify,
                )
                resp_data = resp.json()
                if "success" not in resp_data or not resp_data["success"]:
                    raise RuntimeError("could not add file to challenge")

        return challenge_id

    def requirements(
        self, challenge_id: int, challenge: Challenge, online: List[Dict[str, Any]]
    ):
        headers = {"CSRF-Token": self.nonce}

        # determine the requirement ids
        requirement_ids = []
        for req in challenge.requirements:
            for chal in online:
                if chal["name"] == req:
                    requirement_ids.append(chal["id"])
                    break
        if len(requirement_ids) != len(challenge.requirements):
            raise RuntimeError("could not find challenge requirements")

        # link the requirements
        if requirement_ids:
            data = {"requirements": {"prerequisites": requirement_ids}}
            resp = self.session.patch(
                self.base + f"/api/v1/challenges/{challenge_id}",
                headers=headers,
                json=data,
                verify=self.verify,
            )

    def _extract_nonce(self):
        resp = self.session.get(self.base, verify=self.verify)
        matches = CTFd.NONCE_EXPRESSION.search(resp.content.decode())
        if matches:
            self.nonce = matches.group(1)
        else:
            raise RuntimeError("could not extract nonce")

    def _login(self):
        data = {"name": self.username, "password": self.password, "nonce": self.nonce}
        resp = self.session.post(self.base + "/login", verify=self.verify, data=data)
        if "username or password is incorrect" in resp.text:
            raise RuntimeError("could not login, invalid credentials")


if __name__ == "__main__":
    # run with colorama
    colorama.init(autoreset=True)
    try:
        main()
    except Exception:
        traceback.print_exc()
    finally:
        colorama.deinit()
