from concurrent.futures import ThreadPoolExecutor
from DrissionPage import WebPage, ChromiumOptions


def collect(page, start_page: int=1):
    
    for _ in range(2):
        for item in page.eles('.img-box'):
            download_btn = item('.down-span')
            if not download_btn:
                print("找不到下载按钮")
                continue
            download_btn.click()
            # 等待触发下载，同时取消该任务
            mission = page.wait.download_begin(cancel_it=True)
            # 转用download()方法下载
            page.download(mission.url, goal_path=r'.\jjbz_demo', rename=f'{start_page}')
            # 每页只下载一张
            break
        next_btn = page('.vue_pagination_next vue_pagination_item')
        if next_btn:
            next_btn.click()
            page.wait.load_start()
            start_page += 1
        else:
            break
        
def get_start_page(max_page: int, interval=2):
    return [p for p in range(1, max_page, interval)]
        
        
        
def main(pages: int):
    start_pages = get_start_page(pages)
    co = ChromiumOptions()
    co.headless(True)
    page = WebPage(chromium_options=co)
    args1 = []
    for i, p in enumerate(start_pages):
        if i == 0:
            page.get('https://bz.zzzmh.cn/index')
            page.wait.load_start()
            tab = page.get_tab()
            tab.set.download_path('.')
        else:
            tab2 = page.new_tab('https://bz.zzzmh.cn/index')
            tab = page.get_tab(tab2)
            tab.wait.load_start()
            # 输入并且回车
            tab('.vue_pagination_message').ele('t:input').input(f"{p}\n")
            tab.set.download_path('.')
        args1.append(tab)
    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(collect, args1, start_pages)
    except Exception as e:
        print(f"执行失败{e}")
        page.quit()
    else:
        print("执行成功")
        page.quit()
        
if __name__ == '__main__':
    main(4)