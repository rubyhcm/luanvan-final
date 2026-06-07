# Hướng dẫn cài đặt Git config trên máy mới

## 1. Thông tin cá nhân

```bash
git config --global user.name "James"
git config --global user.email "loindp@ttcagris.com.vn"
```

## 2. Cấu hình pull & credential

```bash
git config --global pull.rebase false
git config --global credential.helper store
```

## 3. Cấu hình Azure DevOps (PAT token)

```bash
git config --global url."https://pat:<PAT_TOKEN>@dev.azure.com/".insteadOf "https://dev.azure.com/"
git config --global url."https://dev.azure.com/".insteadOf "git://dev.azure.com/"
```

> ⚠️ Thay `<PAT_TOKEN>` bằng token mới tạo từ Azure DevOps (Settings > Personal Access Tokens).

## 4. SSH key cho GitHub

```bash
# Tạo SSH key
ssh-keygen -t ed25519 -C "loindp@ttcagris.com.vn"

# Copy public key, sau đó thêm vào GitHub > Settings > SSH Keys
cat ~/.ssh/id_ed25519.pub
```

## 5. Kiểm tra

```bash
git config --list --global
ssh -T git@github.com
```
