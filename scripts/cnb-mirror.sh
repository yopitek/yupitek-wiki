#!/usr/bin/env bash
# cnb.cool 完整 mirror 腳本（git push --mirror）。
#
# 用途：將本 repo 所有 refs 鏡像至 cnb.cool（中國境內可直連備援）。
# Remote 參數化：可用環境變數 CNB_REMOTE 或第一個參數覆蓋。
#
# 用法：
#   bash scripts/cnb-mirror.sh                          # 使用預設 remote
#   CNB_REMOTE=git@cnb.cool:foo/bar.git scripts/cnb-mirror.sh
#   bash scripts/cnb-mirror.sh git@cnb.cool:yupitek/yupitek-wiki.git
#
# 安全性：
#   - 工作區不乾淨時拒絕執行（mirror 前必須先 commit）。
#   - --mirror 會以本地 refs 覆蓋遠端所有 refs（含刪除遠端多餘分支），屬破壞性同步，
#     故非 CI 環境下要求輸入 y 確認；CI 可設 CNB_ASSUME_YES=1 跳過。

set -euo pipefail

CNB_DEFAULT_REMOTE="git@cnb.cool:yupitek/yupitek-wiki.git"
REMOTE_NAME="cnb"

usage() {
    sed -n '2,16p' "${BASH_SOURCE[0]}"
}

main() {
    local cnb_remote="${1:-${CNB_REMOTE:-$CNB_DEFAULT_REMOTE}}"

    if [[ "$cnb_remote" == "-h" || "$cnb_remote" == "--help" ]]; then
        usage
        return 0
    fi

    # 1. 必須在 git repo 內
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        echo "[ERROR] 不在 git repo 內，無法鏡像。" >&2
        return 1
    fi

    # 2. 工作區必須乾淨（mirror 代表「本地即真相」）
    if [[ -n "$(git status --porcelain)" ]]; then
        echo "[ERROR] 工作區有未 commit 變更，請先 commit 再 mirror。" >&2
        git status --short >&2
        return 1
    fi

    # 3. 綁定/更新 cnb remote
    if git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
        git remote set-url "$REMOTE_NAME" "$cnb_remote"
    else
        git remote add "$REMOTE_NAME" "$cnb_remote"
    fi

    echo "Mirror 目標：$cnb_remote"
    echo "將推送 refs："
    git for-each-ref --format='  %(refname)' refs/heads refs/tags

    # 4. 破壞性操作確認（CI 用 CNB_ASSUME_YES=1 跳過）
    if [[ "${CNB_ASSUME_YES:-0}" != "1" ]]; then
        read -r -p "以上 refs 將強制覆蓋 cnb.cool 遠端，確定？[y/N] " reply
        if [[ ! "$reply" =~ ^[Yy]$ ]]; then
            echo "已取消。"
            return 1
        fi
    fi

    git push --mirror "$REMOTE_NAME"
    echo "[OK] 已鏡像至 $cnb_remote"
}

main "$@"
