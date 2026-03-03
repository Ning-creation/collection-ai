import requests
import os

url = "https://summer-ospp.ac.cn/api/getProList"

payload = {
    "difficulty": [],
    "lang": "zh",
    "orgName": [],
    "pageNum": 1,
    "pageSize": 50,
    "programName": "",
    "programmingLanguageTag": [],
    "supportLanguage": [],
    "techTag": []
}

# HTTP请求头，指定发送的数据格式为JSON
headers = {
    "Content-Type": "application/json"
}

resp = requests.post(url, json=payload, headers=headers)

data = resp.json()

print(data.keys())

rows = data["rows"]
# print(len(rows))
print(rows[0])

import json

def parse_project(p): # p：参数，接收一个项目字典
    raw = p.get("techTag", [])

    print(raw)

    tech_tags = []

    if isinstance(raw, list):
        for t in raw:
            if isinstance(t, dict):
                tech_tags.append(t.get("tagName"))
            elif isinstance(t, str):
                tech_tags.append(t)

    elif isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                for item in parsed:
                    # item 形如 ["os", "Linux"]
                    if isinstance(item, list) and len(item) == 2:
                        tech_tags.append(item[1])
        except json.JSONDecodeError:
            pass

    return {
        "programCode": p.get("programCode"),
        "name": p.get("programName"),
        "difficulty": p.get("difficulty"),
        "tech_tags": tech_tags
    }

projects_basic = [parse_project(p) for p in rows]

for p in projects_basic[:3]:
    print(p)

DETAIL_URL = "https://summer-ospp.ac.cn/api/getProDetail"

DETAIL_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/145.0.0.0 Safari/537.36",
    "Referer": "https://summer-ospp.ac.cn/org/prodetail/255660173?lang=zh&list=pro",
    "Origin": "https://summer-ospp.ac.cn",
    "Cookie": "UM_distinctid=19c7a16fc13429-0f0ecf19b263cf8-26061c51-1bcab9-19c7a16fc14958; "
              "cna=47107357364d43b388ebf85094c59d2d; "
              "tgt=1771830086.023.798.614882|2125b4d7ab6829ae59e8509cd0133f66; "
              "CNZZDATA1281243141=1655484495-1771574853-%7C1771830125"
}

def fetch_project_detail(program_code):
    url = "https://summer-ospp.ac.cn/api/getProDetail"
    payload = {
        "programId": program_code,
        "type": "org"
    }

    resp = requests.post(
        url,
        json=payload,
        headers=DETAIL_HEADERS
    )

    return resp.json()

def parse_description(detail):
    return detail.get("programDesc", "")

def parse_output_requirement(detail):
    results = []

    for item in detail.get("outputRequirement", []):
        if isinstance(item, dict):
            title = item.get("title")
            if title:
                results.append(title)

    return results

def parse_project_detail(detail):
    return {
        "description": detail.get("programDesc"),
        "outputRequirement": parse_output_requirement(detail)
    }

all_projects_full = []

for p in projects_basic:
    code = p["programCode"]
    detail = fetch_project_detail(code)

    detail_parsed = parse_project_detail(detail)

    full = {
        **p,                 # 基本信息
        **detail_parsed      # 仅新增字段
    }

    all_projects_full.append(full)

print(all_projects_full[0])

PDF_URL = "https://summer-ospp.ac.cn/api/publicApplication"

PDF_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/145.0.0.0 Safari/537.36",
    "Origin": "https://summer-ospp.ac.cn",
    "Referer": "https://summer-ospp.ac.cn/",
    "Cookie": "UM_distinctid=19c7a16fc13429-0f0ecf19b263cf8-26061c51-1bcab9-19c7a16fc14958; "
              "cna=47107357364d43b388ebf85094c59d2d; "
              "tgt=1771830086.023.798.614882|2125b4d7ab6829ae59e8509cd0133f66; "
              "CNZZDATA1281243141=1655484495-1771574853-%7C1771833346"
}

def download_application_pdf(pro_id, filename):
    payload = {
        "proId": pro_id
    }

    resp = requests.post(
        PDF_URL,
        json=payload,
        headers=PDF_HEADERS
    )

    # 保险校验
    content_type = resp.headers.get("Content-Type", "")
    print("PDF Content-Type:", content_type)

    if "pdf" not in content_type.lower():
        raise RuntimeError("返回的不是 PDF，请检查 Cookie / proId")

    with open(filename, "wb") as f:
        f.write(resp.content)

def parse_pro_id(detail):
    return detail.get("orgProgramId")

os.makedirs("pdfs", exist_ok=True)

for p in projects_basic:
    code = p["programCode"]
    detail = fetch_project_detail(code)

    pro_id = parse_pro_id(detail)

    if pro_id:
        filename = f"pdfs/{code}.pdf"
        try:
            download_application_pdf(pro_id, filename)
            print(f"PDF 下载成功: {filename}")
        except Exception as e:
            print(f"PDF 下载失败 {code}: {e}")
    else:
        print(f"项目 {code} 没有 proId")