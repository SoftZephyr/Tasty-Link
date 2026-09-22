#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the final Subconverter/ACL4SSR config from CMLiu's current config."""

import os
from pathlib import Path
from urllib.request import Request, urlopen

UPSTREAM_URL = 'https://raw.githubusercontent.com/cmliu/ACL4SSR/refs/heads/main/Clash/config/ACL4SSR_Online_Mini_NoAuto_CF.ini'
RULESET_PATH = "ad-rules.list"
OUTPUT = Path("config.ini")


def fetch(url):
    req = Request(url, headers={"User-Agent": "github-actions-acl4ssr-generator/1.0"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    owner = os.environ["REPO_OWNER"]
    repo = os.environ["REPO_NAME"]
    branch = os.environ.get("REPO_BRANCH", "main")

    raw_rules_url = (
        f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"
        f"{RULESET_PATH}"
    )

    upstream = fetch(UPSTREAM_URL)
    lines = upstream.splitlines()

    if "[custom]" not in upstream:
        raise RuntimeError("上游文件没有 [custom] 段，拒绝生成。")

    first_ruleset = next(
        (i for i, line in enumerate(lines) if line.startswith("ruleset=")),
        None,
    )
    if first_ruleset is None:
        raise RuntimeError("上游文件没有 ruleset= 行，拒绝生成。")

    # 防止重复插入。
    lines = [
        line for line in lines
        if not line.startswith("ruleset=🛑 全球拦截," + raw_rules_url)
    ]

    first_ruleset = next(
        i for i, line in enumerate(lines) if line.startswith("ruleset=")
    )
    lines.insert(first_ruleset, f"ruleset=🛑 全球拦截,{raw_rules_url}")

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print("Generated:", OUTPUT)
    print("CMLiu source:", UPSTREAM_URL)
    print("Custom rules:", raw_rules_url)


if __name__ == "__main__":
    main()
