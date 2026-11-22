# Hostinger 拉取 GitHub 仓库做站点部署 · 操作手册

> 你想要的方式：**Hostinger 主动拉取 GitHub 仓库 → 同步到 `public_html` → 自动发布**。
> 这条路可行，但**必须有 hPanel 权限**才能配置。下面是「现在能做什么」和「拿到权限后 6 步」，
> 以及两种绕开权限的替代方案。

---

## 一、先确认你被卡在哪一层

Hostinger 的 Git 部署不是所有套餐都有，也不一定是所有账号角色都能看见。按顺序排查：

| # | 检查 | 怎么查 | 如果不符合 |
|---|---|---|---|
| 1 | **套餐**是否含 Git | hPanel → 左侧菜单找 **Advanced → GIT**（有的版本在 **Files → Git**） | Premium/Starter 一般没有；需升级到 **Business 及以上** |
| 2 | **账号角色** | hPanel 右上角头像 → 看是否显示 "Owner"，或你是被邀请的 **Team member** | 让 Owner 给你 **Websites / Files** 权限 |
| 3 | **站点是否已创建** | hPanel → Websites，`asiajoly.com` 是否在列表里 | 没有站点就没有可部署的目标，需 Owner 创建 |

> 如果连 hPanel 都登不进去（不是账号里的人），那这一步只能由账号持有人操作，
> 你能做的是「把仓库准备好」——下面第二节全部可以在没有权限时完成。

---

## 二、现在就能做的准备（不需要任何权限）

仓库已经满足 Hostinger 拉取的全部条件，我已逐项检查：

| 条件 | 状态 |
|---|---|
| 仓库公开（Hostinger 可匿名 clone，无需 token） | ✅ `public` |
| 默认分支 `main` | ✅ |
| 站点入口在根目录 `index.html` | ✅ |
| 纯静态、无构建步骤（不需要 npm/composer） | ✅ |
| 所有资源用相对路径（`assets/...`），子目录部署也不会断 | ✅ 已扫描，无 `/` 开头路径 |
| 无子模块、无 LFS、无 >200KB 大文件 | ✅ |
| 构建产物已提交（不需要在服务器上跑 Python） | ✅ 30 个 HTML 都在仓库里 |

自检命令（在仓库根目录跑）：

```bash
python3 tools/preflight.py
```

### 如果要改成私有仓库

Hostinger 用 SSH deploy key 拉私有库。生成并添加**只读**部署密钥：

```bash
ssh-keygen -t ed25519 -C "hostinger-deploy" -f ./hostinger_deploy -N ""
# 把公钥加到 GitHub：仓库 → Settings → Deploy keys → Add deploy key（不要勾 Allow write）
cat hostinger_deploy.pub
```

然后把私钥 `hostinger_deploy` 的内容填进 Hostinger 的 Git 配置里（Private repository → SSH key）。

---

## 三、拿到权限后的 6 步

1. hPanel → **Websites → asiajoly.com → Manage**
2. 左侧 **Advanced → GIT**（或 **Files → Git**）→ **Create new repository**
3. 选择 **GitHub** → **Connect** 授权 → 选仓库 **`hhcnmtkrt8-lab/asiajoly`**
4. 填部署参数：

   | 字段 | 填什么 |
   |---|---|
   | Branch | `main` |
   | Install path / Directory | `/public_html` |
   | Build command | **留空** |
   | Node/PHP version | 无关，留默认 |

5. 点 **Create / Deploy**，等 30–60 秒完成 clone。
6. 之后每次改动：仓库 push → hPanel 里点 **Deploy / Pull**（部分套餐支持 webhook 自动拉取）。

### 部署后必须处理的两个坑

**坑 1：默认 `index.php` 会抢在 `index.html` 前面。**
你现在的 asiajoly.com 返回的是 Hostinger 占位页（`x-powered-by: PHP/8.3`、`panel: hpanel`），
说明 `public_html` 里很可能有 `index.php` 或 `default.php`。Apache 的 `DirectoryIndex`
默认把 `index.php` 排在 `index.html` 之前 —— 结果就是：部署成功了，但打开还是 Coming soon。

处理：在 **File Manager** 里删掉 `public_html/index.php`、`default.php`、`coming-soon.*`，
或加 `.htaccess`：

```apache
DirectoryIndex index.html index.php
```

**坑 2：部署进了子目录。**
如果 Install path 填了 `/public_html/asiajoly`，网址会变成 `asiajoly.com/asiajoly/`。
要根域名直出，必须部署到 `/public_html`。

---

## 四、如果没有 Git 功能（套餐不支持）

用 **FTP + GitHub Actions** 推送，效果等价，只需要 FTP 账号，不需要 Git 菜单：

1. hPanel → **Files → FTP Accounts**，记下 **FTP host / username / password**
2. GitHub 仓库 → **Settings → Secrets and variables → Actions**，加三个 secret：
   `FTP_SERVER`、`FTP_USERNAME`、`FTP_PASSWORD`
3. GitHub → **Actions → Deploy to Hostinger (FTP) → Run workflow**

工作流已放在 `.github/workflows/deploy-hostinger.yml`，只在手动触发时运行，不会随 push 自动跑。
它会同步整个仓库到 `/public_html/`，并排除 `.git`、`.build`、`copy/`、Python 脚本等源文件。

---

## 五、验证清单

```bash
# 1. 首页是不是我们的站（不应出现 Hostinger 占位）
curl -s https://asiajoly.com | grep -o "<title>[^<]*"

# 2. 是不是静态（不应再有 x-powered-by: PHP）
curl -sI https://asiajoly.com | grep -iE "server|x-powered-by"

# 3. 关键资源可达
for f in shop.html p-spring-01.html assets/styles.css assets/products/spring-01.svg; do
  printf "%s  %s\n" "$(curl -s -o /dev/null -w '%{http_code}' https://asiajoly.com/$f)" "$f"
done
```

期望：标题是 `Asiajoly — Calm, clean objects / for cats and dogs`，`server: LiteSpeed` 或 `openresty`，
没有 `x-powered-by: PHP`，四个资源全部 `200`。

---

## 六、给账号持有人的一句话说明（可直接转发）

> 请帮我开通 Hostinger 的 Git 部署：套餐需要 Business 或以上，并给我的账号 Websites / Files 权限。
> 要部署的仓库是 `github.com/hhcnmtkrt8-lab/asiajoly`，分支 `main`，部署目录 `/public_html`，
> 无构建命令（纯静态）。部署前请先删除 `public_html` 里的默认 `index.php` 和占位页，
> 否则会一直显示 Coming soon。
