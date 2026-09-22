# Custom ACL4SSR for EdgeTunnel

这个仓库自动维护一个基于 CMLiu `CM_Online_Mini_NoAuto_CF` 的自定义 Subconverter 配置。

## 文件

- `ad-rules.list`：自定义全球拦截规则
- `generate.py`：下载 CMLiu 最新配置并自动插入自定义 ruleset
- `config.ini`：最终给 EdgeTunnel / Subconverter 使用的配置
- `.github/workflows/update.yml`：每天自动更新

## EdgeTunnel 使用

最终只需要填写：

`https://raw.githubusercontent.com/你的用户名/你的仓库/main/config.ini`

第一次创建仓库后，手动运行一次 GitHub Actions，然后确认 `config.ini` 已生成即可。

## 更新逻辑

GitHub Actions 每天下载 CMLiu 最新的 `ACL4SSR_Online_Mini_NoAuto_CF.ini`，然后在第一条 `ruleset=` 前插入：

`ruleset=🛑 全球拦截,<本仓库 ad-rules.list 的 Raw 地址>`

因此 EdgeTunnel 使用的 URL 不需要改变。
