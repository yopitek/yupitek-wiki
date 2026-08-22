#!/usr/bin/env python3
"""飛書知識庫同步腳本（workbuddy 上傳準備）。

依 manifest CSV（欄位同 scripts/feishu-node-mapping.md 規劃：
filepath,brand,doc_type,title,parent_node_token）批次在飛書知識庫建立節點。

- 內容來源：i18n/zh-CN/docusaurus-plugin-content-docs/current/<filepath>
- 帳號 / 知識庫 space 一律參數化，從環境變數或 CLI 帶入，絕不寫死。
- 標準庫實作（urllib），無第三方依賴，可直接進 CI。

用法：
    # 先試跑（不呼叫寫入 API，僅列出將建立的節點）
    python3 scripts/feishu-sync.py plan --manifest scripts/feishu-manifest.csv

    # 實際建立節點
    FEISHU_APP_ID=xxx FEISHU_APP_SECRET=xxx FEISHU_SPACE_ID=7419... \
        python3 scripts/feishu-sync.py sync

環境變數：
    FEISHU_APP_ID      飛書企業自建應用 App ID（sync 必填）
    FEISHU_APP_SECRET  飛書企業自建應用 App Secret（sync 必填）
    FEISHU_SPACE_ID    知識空間 space_id（sync 必填；可用 --space-id 覆蓋）
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ZH_CN_DOCS = REPO_ROOT / "i18n/zh-CN/docusaurus-plugin-content-docs/current"
API_ROOT = os.environ.get("FEISHU_API_ROOT", "https://open.feishu.cn/open-apis")

MANIFEST_COLUMNS = ("filepath", "brand", "doc_type", "title", "parent_node_token")


class FeishuError(RuntimeError):
    """飛書 API 或設定錯誤。"""


def load_manifest(path: Path) -> list[dict[str, str]]:
    """讀取並基本校驗 manifest CSV。"""
    if not path.is_file():
        raise FeishuError(f"manifest 不存在：{path}")
    rows: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in MANIFEST_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise FeishuError(f"manifest 缺少欄位：{missing}（需含 {list(MANIFEST_COLUMNS)}）")
        for lineno, row in enumerate(reader, start=2):
            if not row.get("title"):
                continue
            rows.append({k: (row.get(k) or "").strip() for k in MANIFEST_COLUMNS})
            rows[-1]["_lineno"] = str(lineno)  # type: ignore[assignment]
    return rows


def check_source_files(rows: list[dict[str, str]]) -> tuple[list[dict], list[str]]:
    """確認每列對應的 zh-CN markdown 存在，回傳 (有效列, 缺檔警告)。"""
    ok, warnings = [], []
    for row in rows:
        fp = row["filepath"]
        if fp and not (ZH_CN_DOCS / fp).is_file():
            warnings.append(f"L{row['_lineno']}: zh-CN 缺檔 {fp}")
            continue
        ok.append(row)
    return ok, warnings


def http_json(method: str, url: str, *, token: str | None = None,
              payload: dict | None = None) -> dict:
    """極簡 JSON HTTP client（urllib）。"""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise FeishuError(f"{method} {url} -> HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise FeishuError(f"{method} {url} 連線失敗：{exc.reason}") from exc
    if body.get("code") not in (0, None):
        raise FeishuError(f"{method} {url} -> code={body.get('code')} msg={body.get('msg')}")
    return body


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    body = http_json(
        "POST", f"{API_ROOT}/auth/v3/tenant_access_token/internal",
        payload={"app_id": app_id, "app_secret": app_secret},
    )
    token = body.get("tenant_access_token")
    if not token:
        raise FeishuError(f"取得 tenant_access_token 失敗：{body}")
    return str(token)


def create_wiki_node(space_id: str, token: str, *, title: str,
                     parent_node_token: str, obj_type: str = "docx",
                     obj_token: str | None = None) -> dict:
    """POST /wiki/v2/spaces/:space_id/nodes — 在指定父節點下建立子節點。"""
    payload: dict = {
        "space_id": space_id,
        "title": title,
        "obj_type": obj_type,
        "parent_node_token": parent_node_token,
        "node_type": "origin",
    }
    if obj_token:
        payload["obj_token"] = obj_token
        payload["node_type"] = "origin"
    return http_json(
        "POST", f"{API_ROOT}/wiki/v2/spaces/{space_id}/nodes",
        token=token, payload=payload,
    )


def cmd_plan(args: argparse.Namespace) -> int:
    rows = load_manifest(Path(args.manifest))
    valid, warnings = check_source_files(rows)
    for w in warnings:
        print(f"[WARN] {w}", file=sys.stderr)
    print(f"manifest 共 {len(rows)} 列，有效 {len(valid)} 列（將於 zh-CN 找到源檔者才上傳）")
    for row in valid:
        print(f"  [{row['brand']}/{row['doc_type']}] {row['title']}  <- {row['filepath']}"
              f"  parent={row['parent_node_token'] or '(第一層)'}")
    print("plan 模式未呼叫任何寫入 API。")
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    app_id = args.app_id or os.environ.get("FEISHU_APP_ID")
    app_secret = args.app_secret or os.environ.get("FEISHU_APP_SECRET")
    space_id = args.space_id or os.environ.get("FEISHU_SPACE_ID")
    missing = [name for name, val in (
        ("FEISHU_APP_ID", app_id),
        ("FEISHU_APP_SECRET", app_secret),
        ("FEISHU_SPACE_ID", space_id),
    ) if not val]
    if missing:
        raise FeishuError(f"sync 模式缺少參數：{missing}（環境變數或 CLI 帶入）")

    rows = load_manifest(Path(args.manifest))
    valid, warnings = check_source_files(rows)
    for w in warnings:
        print(f"[WARN] {w}", file=sys.stderr)

    token = get_tenant_access_token(str(app_id), str(app_secret))
    created, failed = [], []
    for row in valid:
        try:
            body = create_wiki_node(
                str(space_id), token,
                title=row["title"], parent_node_token=row["parent_node_token"],
            )
            node = (body.get("data") or {}).get("node") or {}
            created.append((row["title"], node.get("node_token", "?")))
            print(f"[OK] {row['title']} -> node_token={node.get('node_token')}")
        except FeishuError as exc:
            failed.append((row["title"], str(exc)))
            print(f"[FAIL] {row['title']}: {exc}", file=sys.stderr)

    print(f"\n完成：建立 {len(created)} 節點、失敗 {len(failed)}。")
    print("node_token 請回填 scripts/feishu-node-mapping.md 對照表。")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="飛書知識庫同步（節點建立）腳本")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--manifest", default=str(REPO_ROOT / "scripts/feishu-manifest.csv"),
                        help="manifest CSV 路徑")

    p_plan = sub.add_parser("plan", parents=[common], help="乾跑：列出將建立的節點")
    p_plan.set_defaults(func=cmd_plan)

    p_sync = sub.add_parser("sync", parents=[common], help="實際建立節點")
    p_sync.add_argument("--app-id", help="覆蓋 FEISHU_APP_ID")
    p_sync.add_argument("--app-secret", help="覆蓋 FEISHU_APP_SECRET")
    p_sync.add_argument("--space-id", help="覆蓋 FEISHU_SPACE_ID")
    p_sync.set_defaults(func=cmd_sync)

    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except FeishuError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
