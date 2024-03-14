from concurrent.futures import ThreadPoolExecutor
from DrissionPage import WebPage, ChromiumOptions
from DataRecorder import Recorder
from datetime import date
        
        
def collect_s_ele(page, r):
    """静态"""
    map_dict = {'今日发布': str(date.today())}
    for _ in range(2):
        for item in page.s_eles('.card-item-single'):
            name = item('.task-names').text
            url = item('t:a').link
            money = item('.total-money').text
            des = item('.description-requir').text
            content = item('.contents-text').text
            labels = item('.boxs-logos').texts()
            marks = item('.mark-text').texts()
            marks = [map_dict.get(m, m) for m in marks]
            label = ' '.join(labels)
            mark = ' '.join(marks)
            r.add_data((page.url, name, url, money, des, content, label, mark))
            # time.sleep(round(random.random(), 2))
        print(f"完成{page.url}")
        btn = page('@@type=button@@class=btn-next', timeout=2)
        if btn:
            btn.click()
            page.wait.load_start()
        else:
            break

        
def get_start_url(max_page: int):
    urls = ['https://www.zbj.com/xq/sjclrj/r4/?kw']
    for i in range(1, max_page, 2):
        url = f'https://www.zbj.com/xq/sjclrj/r4p{i+2}/?kw&osStr'
        urls.append(url)
    return urls


def main(max_page: int):
    """_summary_

    Args:
        max_page (int): 页数,偶数页
    """
    urls = get_start_url(max_page-2)
    co = ChromiumOptions()
    co.headless(True)
    page = WebPage(chromium_options=co)
    filepath = r".\zbj_demo\data.csv"
    r = Recorder(filepath)
    r.add_data(('from_page_url', 'name', 'url', 'money', 'des', 'content', 'label', 'mark'))
    args = []
    for index, url in enumerate(urls):
        if index == 0:
            page.get(url)
            tab = page.get_tab()
        else:
            tab2 = page.new_tab(url)
            tab = page.get_tab(tab2)
        args.append([tab, r])
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(collect_s_ele, *list(zip(*args)))
    if page:
        page.quit()
    

        
if __name__ == '__main__':
    """多线程爬取猪八戒的职位"""
    main(4)