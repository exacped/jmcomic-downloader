import jmcomic
import os
import subprocess
import sys

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')

option = jmcomic.create_option_by_str(f'''
dir_rule:
  base_dir: {DOWNLOAD_DIR}
  rule: Bd_Pname
download:
  cache: true
  image:
    decode: true
  threading:
    image: 30
    photo: 20
client:
  domain: []
  postman:
    type: curl_cffi
    meta_data:
      impersonate: chrome
  impl: api
  retry_times: 5
plugins:
  valid: log
''')

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    print("JMComic 下载器")
    print("=" * 40)

    while True:
        album_id = input("\n请输入本子ID (输入 q 退出): ").strip()
        if album_id.lower() == 'q':
            break

        if not album_id.isdigit():
            print("ID 必须是数字，请重新输入")
            continue

        try:
            print(f"正在下载本子 {album_id} ...")
            jmcomic.download_album(album_id, option)
            print(f"下载完成！保存至: {DOWNLOAD_DIR}")
            print("正在合成 PDF ...")
            subprocess.run([sys.executable, 'make_pdf.py'], cwd=os.path.dirname(__file__))
        except Exception as e:
            print(f"下载失败: {e}")

if __name__ == '__main__':
    main()
