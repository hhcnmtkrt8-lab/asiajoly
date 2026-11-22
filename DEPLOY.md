# 部署说明 / Deployment

> 结论先放这里：**不需要 Hostinger 面板权限，也能让 asiajoly.com 指向这个 GitHub 仓库。**
> 你需要的不是主机商权限，而是 **DNS 权限** —— 也就是域名注册商（新网 / Xin Net）的账号。

## 现在的状态 / Current state

| 项目 | 现状 | 检查方式 |
|---|---|---|
| 代码仓库 | `github.com/hhcnmtkrt8-lab/asiajoly`（public，main 分支） | `gh repo view hhcnmtkrt8-lab/asiajoly` |
| GitHub Pages | **已发布**，30 页全部 200 | https://hhcnmtkrt8-lab.github.io/asiajoly/ |
| asiajoly.com | 指向 Hostinger，显示 **“Coming soon”** 占位页 | `curl -sI https://asiajoly.com` |
| 域名注册商 | **Xin Net Technology Corporation（新网）** | `whois asiajoly.com` |
| 权威 DNS | `hermes.dns-parking.com` / `artemis.dns-parking.com`（**Hostinger 的 NS**） | `dig NS asiajoly.com` |

也就是说：域名在**新网**注册，DNS 托管在 **Hostinger**。你只要在**新网**把 NS 换掉，
就和 Hostinger 彻底无关了。

---

## 方案 A（推荐）：在新网改 NS → Cloudflare → 指向 GitHub Pages

完全不需要 Hostinger 权限，只需要新网账号。

### A1. 在新网把 NS 换成 Cloudflare

1. 注册/登录 Cloudflare → **Add a site** → 输入 `asiajoly.com` → 选 **Free** 计划。
2. Cloudflare 会给你两条 NS，例如 `xxx.ns.cloudflare.com` / `yyy.ns.cloudflare.com`。
3. 登录 **新网**（`www.xinnet.com`）→ 我的域名 → `asiajoly.com` → **DNS 解析 / 修改域名服务器** →
   选「使用自定义 DNS」→ 填入 Cloudflare 的两条 NS → 提交。
4. 等生效（通常 10 分钟–24 小时）。检查：`dig +short NS asiajoly.com` 应显示 cloudflare.com。

> 如果新网面板里 NS 是灰的/改不了，说明域名可能开启了「DNS 托管锁」，
> 需要先在新网关掉，或联系新网客服解锁。

### A2. 在 Cloudflare 加 DNS 记录（指向 GitHub Pages）

| 类型 | 名称 | 内容 | 代理状态 |
|---|---|---|---|
| A | `@` | `185.199.108.153` | **DNS only（灰云）** |
| A | `@` | `185.199.109.153` | DNS only |
| A | `@` | `185.199.110.153` | DNS only |
| A | `@` | `185.199.111.153` | DNS only |
| CNAME | `www` | `hhcnmtkrt8-lab.github.io` | DNS only |

**必须关掉橙云（Proxy）**，否则 GitHub 的 HTTPS 证书签发会失败（会一直卡在 "Certificate not yet created"）。
证书签发完成后，如果你想开 Cloudflare CDN 可以再打开。

### A3. 在 GitHub 绑定自定义域名

仓库 → **Settings → Pages → Custom domain** → 填 `asiajoly.com` → **Save**
→ 等 DNS check 通过 → 勾选 **Enforce HTTPS**。

GitHub 会自动在仓库根目录生成一个 `CNAME` 文件（内容就是 `asiajoly.com`）。
**不要提前手动加这个文件** —— 在 DNS 没生效前加，`github.io` 那个地址会立刻跳转到打不开的域名上。

### A4. 验证

```bash
dig +short asiajoly.com          # 应返回 185.199.108-111.153
dig +short www.asiajoly.com      # 应返回 hhcnmtkrt8-lab.github.io 及 GitHub IP
curl -sI https://asiajoly.com | head -3   # 应返回 200 + server: GitHub.com
```

### 之后的发布流程

改完代码 `git push` → GitHub Pages 自动重建（约 1 分钟）。没有构建步骤，仓库根目录就是站点。

---

## 方案 B：如果能拿到 Hostinger 权限

两条路，任选：

### B1. 只用 Hostinger 的 DNS（最简单）

hPanel → **Domains → asiajoly.com → DNS Zone**，把现有的 A / CNAME 改成方案 A2 那五条，
然后在 GitHub 里做 A3。Hostinger 的托管空间可以继续空着不用。

### B2. 用 Hostinger 托管 + GitHub 自动同步（FTP）

hPanel → **Files → FTP Accounts** 拿到主机地址、用户名、密码，然后在 GitHub 仓库
**Settings → Secrets and variables → Actions** 里添加三个 secret：

| Secret | 值 |
|---|---|
| `FTP_SERVER` | 例如 `ftp.asiajoly.com` 或 hPanel 里给的 IP |
| `FTP_USERNAME` | FTP 用户名 |
| `FTP_PASSWORD` | FTP 密码 |

然后到 **Actions → Deploy to Hostinger (FTP) → Run workflow** 手动触发。
工作流文件：`.github/workflows/deploy-hostinger.yml`（只在手动触发时运行，不会自动跑）。

> 这个方案会把整个仓库根目录同步到 `/public_html/`，并自动排除 `.git`、`.build`、
> Python 脚本和 `copy/` 等构建源码。

---

## 方案 C：暂时不改域名

站点已经可以直接用：**https://hhcnmtkrt8-lab.github.io/asiajoly/**

缺点是品牌域名还是占位页。适合在拿到 DNS 权限前先给客户/朋友看。

---

## 常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| Pages 设置里 DNS check 一直红 | Cloudflare 开了橙云，或记录还没传播 | 关掉代理，等 10 分钟再试 |
| 证书一直 "not yet created" | 同上 | 关橙云 → Remove domain → 重新 Add |
| `www` 打不开 | 漏了 CNAME 记录 | 加 `www → hhcnmtkrt8-lab.github.io` |
| 改了 NS 但域名还显示 Hostinger 页面 | 旧 NS 有缓存 | `dig NS asiajoly.com` 确认，等 TTL |
| 想换回 Hostinger | 把 NS 改回 `hermes/artemis.dns-parking.com` | 记录保留在 Hostinger 侧 |

## 一个提醒：大陆访问

GitHub Pages 在中国大陆访问不稳定（时快时慢，偶尔被墙）。
你的目标市场是北美/欧洲，用 Pages 没问题；但如果之后要做中国大陆访问，
建议保留 Hostinger 或换到有国内节点的对象存储 + CDN，不要同时用两套 DNS。
