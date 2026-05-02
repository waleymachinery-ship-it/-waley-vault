#!/usr/bin/env python3
"""
waley-vault 同步脚本
将本地 Vault 推送到腾讯云服务器

用法: python sync_vault_to_server.py
"""
import paramiko
import os
import posixpath

LOCAL_VAULT = 'D:/桌面文件/伟力机械知识库/00_Workflow/memory'
REMOTE_BASE = '/root/waley-vault'
HOST = '106.53.207.188'
PORT = 22
USERNAME = 'root'
PASSWORD = 'Weili2026!'  # 或使用 SSH key: look_for_keys=True

def sync_folder(sftp, local_folder, remote_folder):
    for item in os.listdir(local_folder):
        local_path = os.path.join(local_folder, item)
        remote_path = posixpath.join(remote_folder, item)

        if item == '.git':
            continue

        if os.path.isfile(local_path):
            try:
                remote_mtime = sftp.stat(remote_path).st_mtime
                local_mtime = os.path.getmtime(local_path)
                if local_mtime > remote_mtime:
                    print(f'  UPDATE: {item}')
                    sftp.put(local_path, remote_path)
                else:
                    print(f'  SKIP: {item}')
            except FileNotFoundError:
                print(f'  NEW: {item}')
                sftp.put(local_path, remote_path)
        elif os.path.isdir(local_path):
            print(f'DIR: {item}/')
            try:
                sftp.stat(remote_path)
            except FileNotFoundError:
                sftp.mkdir(remote_path)
            sync_folder(sftp, local_path, remote_path)

def main():
    print(f'Connecting to {HOST}...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, PORT, USERNAME, PASSWORD, look_for_keys=False, allow_agent=False)
    sftp = ssh.open_sftp()

    print(f'Syncing Vault to server...')
    sync_folder(sftp, LOCAL_VAULT, REMOTE_BASE)

    # Git add/commit on server
    print('\nCommitting on server...')
    chan = ssh.get_transport().open_session()
    chan.exec_command('cd /root/waley-vault && git add -A && git commit -m "Vault update from local sync" 2>&1')
    output = b''
    while True:
        data = chan.recv(4096)
        if not data:
            break
        output += data
    result = output.decode('utf-8', errors='replace').strip()
    if result:
        print(result[:300])

    # Verify file count
    chan2 = ssh.get_transport().open_session()
    chan2.exec_command('find /root/waley-vault -type f | wc -l')
    count = chan2.recv(4096).decode('utf-8', errors='replace').strip()
    print(f'\nDone! {count} files on server.')

    sftp.close()
    ssh.close()

if __name__ == '__main__':
    main()
