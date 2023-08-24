import sys

import requests
import json
import random
import time
import http.client
import os
from typing import Dict


def _request_gpt_3_5_turbo(prompt, temperature=0.95, system=None):
    ip_list = ['11.180.217.42', '11.155.117.14', '30.165.29.23']
    ip = random.choice(ip_list)
    url = "http://" + ip + ":8080/http.tme_monitor.chatgpt_openapi_svr.OpenApiServic/ChatGPT"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "bussId": "rec_song_list",
        "temperature": temperature
    }
    if system is not None:
        payload['messages'] = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
        # print('request_length: ', len(system + prompt))
    else:
        payload['messages'] = [
            {"role": "user", "content": prompt}
        ]
        # print('request_length: ', len(prompt))

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
        # print(response)
        response_json = response.json()
        msg = response_json.get('msg')
        reply_content = response_json.get('replyContent')
        if msg == 'success' and reply_content is not None:
            return reply_content
    except requests.exceptions.ConnectionError:
        print('connection error occurred')
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON response{response}: {e}")
    except Exception as e:
        print(f'Failed with exception: {e}')


# http://central.tmeoa.com/tmegpt/index.html的网页接口 外网可用
def _request_tme_chatgpt(prompt, temperature=0.95, system=None):
    import http.client

    conn = http.client.HTTPSConnection("central.tmeoa.com")
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "key": "",
        "temperature": temperature,
        "bussId": "web_common"
    }
    if system is not None:
        payload['messages'].insert(0, {"role": "system", "content": system})
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Cookie': 'x-client-ssid=17d79075775-9954b8a182bd92b66d6d069a780cd1ae4c2e7884; x-host-key-front=17d7907578e-c85f7c96df505793654aa8c022e8a5cf3f005159; x_host_key=17d7907577d-659914e3bb4e916fe23921b3df31d1732d238395; x-host-key-ngn=17d79075775-628df3a72f35641a211c6e34b7f466dafb03443e; caagw_uid=bezjygwywyryy; x_host_key_access=5ad69f5feb35ef0cafc89615f32a26e61d628cc3_s; qk_uid=josephwei; RIO_TCOA_TICKET=tof:TOF4TeyJ2IjoiNCIsInRpZCI6Im50aHNuWndDM3g3SHJMWVZ1ejVFMFIxR2owejY4OGlHIiwiaXNzIjoiMTAuOTkuMTUuMzkiLCJpYXQiOiIyMDIzLTA3LTMxVDExOjEwOjUyLjY5ODI4NzIyOCswODowMCIsImF1ZCI6IjEwLjkxLjIwNi4xNTMiLCJoYXNoIjoiMzUzQjc2QUM1MkNEQ0VFNjIwQkFBQkM2Mjc4NUNDNEM2QkZBMTE2NkIxMjU2NENBNEIwMDM4MjlGMzhBMkNGNiIsIm5oIjoiMjNDRDU2M0ZGNjMwRDQ5MUQ1QTg0NkQzQ0NEMkY3NEE5MjQwNkNEMjA4NUUyRjZEM0M3OTdCMkIxOEUyRTRERCJ9; RIO_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0b2Y0YXV0aCIsInN1YiI6IjI5ODUyMiIsImV4cCI6MTY5MDg1OTQ1MiwibmFtZSI6Impvc2VwaHdlaSIsImVuYyI6IkI3SFdPOVFBZURLekkvU0dCQ3VwajI4emh3eGNSNjNyOTVhc1VHRjNHenZ2MDdsSEtNVEpQb0QyajV6VHpYRS83dUE4VHJ4OHJNeHFnOFJKMnV0WFFmZ2VCL0R0aFdJNU5xck1sc3I4QzVXSkVQZmc3RjJncVFocFNMNHdiT0V4NGNZekFLaUtoRWp2dmErRWgzTVJXQjdFZ2F5b3ZQMHZ3QmVpTWUvZkVmaEZkZW1UbXgzUis2Q1BKbEVwcEh4cnNuK1dnRHBmRFlNcWZ4cVhacEhMeVRxcVhwS21RUjdxdHRRdFAyZEthb1YwWG51UjQwSHJhRUFyNEtFNmZIWHV2NzBWYkJlQTBlZUw5VnpwdEFOSmFobUc3MDFvUjlVSlJWYXJZMzYzcURvZzhQTnFVMmc5cmZ1N3ZZakdveWlnUGZGLzY0UnlycVdzSnh3V0J6UVVzZ3VkR0VrTzRXYmtia0RZZG1wSUdaeVhSUUpmVzZkQUNQdDJLTGkxejVNYjFqQkJwM1hHUTU4MmtwbGNGTzliZGlsWmorK0dnSm02L2JVVzBxWi9mOXh4RmJ0M0NTL0NjWmtNUXBoeVc0RUk0Vm4zVWp0Z2NVN0ZrTmdnakUxaHJ3Zm10eUhlWkFqWDNiZFd3UmRjU1pFNEFaelg2Rk52cllpWkxVYnF4cXZ0UjFuK3ZLZ1JBemVkUlNxbldsaVI5RGZzNXJ5cmFnZTcwU016WE8xN1RSa3VJTUdseWUwM1lEN3NpZWU3ckU4MnZYbUZhMWhSZktLTjlPaUwxYnpVajJEenJwVnZOYjJCc2pGMjNIdjg3Rjl4cXZwQ3JUYW12RHhpeUVNM0xTN1o5WE1RdFhaenhHdmlPU25MUU9wZjllaUY4blh4MGtyZWVubXdweVEwcUdoVlpBRjlNV2VzMUFIb1didWJKb0dQYVJyT3Z5MmtQMTJjV01kbER6czAzWmRESVpkcXBldEFBVmRndzMrSDdHalpTdU1YQmtBWGZUS29vWFVGMlRnMWNqWU9HT3dxN0Z3bGM0VTF6Mm55M3d3RlYwTEM5K1NYOEVPUVFxZ1h4dUVRZUZ4ZVdLYWh0Y2VJVWtvcmhsNzRNZkNqTk5pOGllWi9lVnhBOHJlVGlOeWlWdlJsSkJSMDAwMUxWR0I4VE1lRXJOY2dlY2ZUYW5lWmxTSzFKRENuQmtPOWpwb0NpNzZyRytuREYydVBJWUxIVEYxSlRMRTF0RG5mVGRHZU9XRDZZcUp4TkJMSVhna1BmQjZSNkVwSVp6N2hmZzZmZFRzWktnbGw1OGdiallHVEdoNlEzY3NUOGVEMzFvTGxNNTNwQ2ErcXFsbkxpdGYrT0hueGo5WVplL0VZRzZaVGJCQmpVQjZCN2FaeDNFOWpXSzV4dENVVEZmYjVKV3ZHbXdlSWZ2S2FWaERaSkI4ZkUzYy9vTTViemtFYlIyeEtIWkJpUHdCTytWR0dteGhteTY5eDBOelVsRlBYdlA2dGhwTW0xbHZvRHlWZ1pmYi9oWUk3eDhneGVyYUpML2cvM29DL3JvaXlxcThtWnc9PSIsImp0aSI6IjA3cm1mY2RidzBrOGZ5MGEzc3dhbjUiLCJpYXQiOjE2OTA3NzMwNTIsInYiOiIyMDIyMTAifQ.RX_x7w1ehf58cvBPTA5GVtBjnj_duvSTKGwXG143rcQ; TME_TCOA=b3c5ac29cb3580cc581d0640b5fd4098e4723887; SGW_TICKET=aT0xMDAxNDU4OSZlPWpvc2VwaHdlaSZjPemtj-S7geadsCZlbT1qb3NlcGh3ZWlAdGVuY2VudC5jb20mdD1FTVAmcD0xMDAwMDI5Ny8xMDAwMDMwNi8xMDAwMDYyNi8xMDAwMDkxNyZlcD0xNjkyNTkyNTU5JnNpZ249UlJOS3gxTmxDUC9kNTNDOUhHSVJZRFYvSHFJPQ',
        'Origin': 'http://central.tmeoa.com',
        'Referer': 'http://central.tmeoa.com/tmegpt/index.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    try:
        conn.request("POST", "/tmegpt/api/http.tme_monitor.chatgpt_openapi_svr.OpenApiServic/StreamChatGPT",
                     json.dumps(payload),
                     headers)
        res = conn.getresponse()
        data = res.read()
        res = data.decode("utf-8")
        return res
    except Exception as e:
        print(f'Failed with exception: {e}')


def _request_tme_baichuan(prompt, temperature=0.95, system=None, max_tokens=None, parameters=None):
    url = "http://10.101.137.107:5314/"
    data = {
        "prompt": prompt,
        # "max_new_tokens": max_tokens,
        # "history": history,
        # "max_length": max_length,
        # "top_p": top_p,
        # "temperature": temperature
    }
    # max_new_tokens = json_post_list.get('max_new_tokens')
    #     temperature = json_post_list.get('temperature')
    #     top_k = json_post_list.get('top_k')
    #     top_p = json_post_list.get('top_p')
    #     repetition_penalty = json_post_list.get('repetition_penalty')
    print('parameters: ', parameters)
    if parameters is not None:
        if 'max_tokens' in parameters:
            data['max_new_tokens'] = parameters['max_tokens']
        if 'temperature' in parameters:
            temperature = parameters['temperature']
            if temperature == 0.0:
                temperature += 0.1
            data['temperature'] = temperature
        if 'top_k' in parameters:
            data['top_k'] = parameters['top_k']
        if 'top_p' in parameters:
            data['top_p'] = parameters['top_p']
        if 'repetition_penalty' in parameters:
            data['repetition_penalty'] = parameters['repetition_penalty']
    # print(data)
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    # print(response)
    # print(response.json()['response'])
    try:
        json_res = response.json()
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON response{response}: {e}")
        return None
    if "response" not in json_res:
        print(f"[_request_tme_chatglm] Failed to decode JSON response{response}: {json_res}")
        return None
    res = json_res["response"]
    return res


def _request_tme_chatglm(prompt, temperature=0.95, system=None):
    history = []
    max_length = 2048
    top_p = 0.9
    url = "http://10.101.137.107:5314/"
    data = {
        "prompt": prompt,
        "history": history,
        "max_length": max_length,
        "top_p": top_p,
        "temperature": temperature
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    # print(response)
    # print(response.json()['response'])
    try:
        json_res = response.json()
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON response{response}: {e}")
        return None
    if "response" not in json_res:
        print(f"[_request_tme_chatglm] Failed to decode JSON response{response}: {json_res}")
        return None
    res = json_res["response"]
    return res


def _request_tme_llama2(prompt, temperature=0.95, system=None, parameters=None):
    url = "http://10.101.137.107:5314/"
    data = {
        "prompt": prompt,
    }
    print('parameters: ', parameters)
    if parameters is not None:
        if 'max_tokens' in parameters:
            data['max_new_tokens'] = int(parameters['max_tokens'] * 0.7)
        if 'temperature' in parameters:
            temperature = parameters['temperature']
            if temperature == 0.0:
                temperature += 0.1
            data['temperature'] = temperature
        if 'top_k' in parameters:
            data['top_k'] = parameters['top_k']
        if 'top_p' in parameters:
            data['top_p'] = parameters['top_p']
        if 'repetition_penalty' in parameters:
            data['repetition_penalty'] = parameters['repetition_penalty']
    # data['prompt'] = prompt
    # print(data)
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    # print(response)
    # print(response.json()['response'])
    try:
        json_res = response.json()
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON response{response}: {e}")
        return None
    if "response" not in json_res:
        print(f"[_request_tme_chatglm] Failed to decode JSON response{response}: {json_res}")
        return None
    res = json_res["response"]
    return res


def llm(prompt, temperature=0.95, system=None, max_retry_times=3, print_request=False, model_name='llama2',
        parameters=None):
    if model_name == 'tme':
        request_func = _request_gpt_3_5_turbo
    elif model_name == 'glm':
        request_func = _request_tme_chatglm
    elif model_name == 'baichuan':
        request_func = _request_tme_baichuan
    elif model_name == 'llama2':
        request_func = _request_tme_llama2
    else:
        model_name = 'original_gpt'
        request_func = _request_tme_chatgpt

    log_prefix = model_name + '_' + time.strftime("%Y-%m-%d", time.localtime())
    log_path = log_prefix + '.log'
    with open(log_path, 'a',
              encoding='utf-8') as f:
        f.write(
            f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]==================Q=================={prompt}\n')
        f.write(parameters.__str__() + '\n')
        f.flush()
        if print_request:
            print(prompt)
        for i in range(max_retry_times):

            reply = request_func(prompt, temperature=temperature, system=system, parameters=parameters)
            if reply is not None:
                f.write(
                    f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]==================A=================={reply}\n')
                f.flush()
                return reply

    return None


if __name__ == '__main__':
    prompt = """[INST] Hourly schedule format: 
[Monday February 13 -- 00:00 AM] Activity: [Fill in]
[Monday February 13 -- 01:00 AM] Activity: [Fill in]
[Monday February 13 -- 02:00 AM] Activity: [Fill in]
[Monday February 13 -- 03:00 AM] Activity: [Fill in]
[Monday February 13 -- 04:00 AM] Activity: [Fill in]
[Monday February 13 -- 05:00 AM] Activity: [Fill in]
[Monday February 13 -- 06:00 AM] Activity: [Fill in]
[Monday February 13 -- 07:00 AM] Activity: [Fill in]
[Monday February 13 -- 08:00 AM] Activity: [Fill in]
[Monday February 13 -- 09:00 AM] Activity: [Fill in]
[Monday February 13 -- 10:00 AM] Activity: [Fill in]
[Monday February 13 -- 11:00 AM] Activity: [Fill in]
[Monday February 13 -- 12:00 PM] Activity: [Fill in]
[Monday February 13 -- 01:00 PM] Activity: [Fill in]
[Monday February 13 -- 02:00 PM] Activity: [Fill in]
[Monday February 13 -- 03:00 PM] Activity: [Fill in]
[Monday February 13 -- 04:00 PM] Activity: [Fill in]
[Monday February 13 -- 05:00 PM] Activity: [Fill in]
[Monday February 13 -- 06:00 PM] Activity: [Fill in]
[Monday February 13 -- 07:00 PM] Activity: [Fill in]
[Monday February 13 -- 08:00 PM] Activity: [Fill in]
[Monday February 13 -- 09:00 PM] Activity: [Fill in]
[Monday February 13 -- 10:00 PM] Activity: [Fill in]
[Monday February 13 -- 11:00 PM] Activity: [Fill in]
===
Name: Isabella Rodriguez
Age: 34
Innate traits: friendly, outgoing, hospitable
Learned traits: Isabella Rodriguez is a cafe owner of Hobbs Cafe who loves to make people feel welcome. She is always looking for ways to make the cafe a place where people can come to relax and enjoy themselves.
Currently: Isabella Rodriguez is planning on having a Valentine's Day party at Hobbs Cafe with her customers on February 14th, 2023 at 5pm. She is gathering party material, and is telling everyone to join the party at Hobbs Cafe on February 14th, 2023, from 5pm to 7pm.
Lifestyle: Isabella Rodriguez goes to bed around 11pm, awakes up around 6am.
Daily plan requirement: Isabella Rodriguez opens Hobbs Cafe at 8am everyday, and works at the counter until 8pm, at which point she closes the cafe.
Current Date: Monday February 13

[Monday February 13 -- 00:00 AM] Activity: Isabella is sleeping
[Monday February 13 -- 01:00 AM] Activity: Isabella is sleeping
[Monday February 13 -- 02:00 AM] Activity: Isabella is sleeping
[Monday February 13 -- 03:00 AM] Activity: Isabella is sleeping
[Monday February 13 -- 04:00 AM] Activity: Isabella is sleeping
[Monday February 13 -- 05:00 AM] Activity: Isabella is sleeping
[Monday February 13 -- 06:00 AM] Activity: Isabella is sleeping
[Monday February 13 -- 07:00 AM] Activity: Isabella is sleeping
Here the originally intended hourly breakdown of Isabella's schedule today: 1) wake up and complete the morning routine at 8:00 am, 2) the questions in Slack from 9:00 am to 10:30 am, 3) prepare salads at 11:00 am, 4) talk to visitors at the Cafe Inquiry at 12:30 pm
What is Isabella doing at 8:00 AM? [/INST]
[Monday February 13 -- 08:00 AM] Activity: Isabella is
"""
    for _ in range(10):
        response = llm(prompt, max_retry_times=5, model_name='llama2',
                       parameters={'max_tokens': 30, 'temperature': 0.1, 'repetition_penalty': 0})
        print('------\n', response)
#     # print(_request_tme_chatgpt("GPT3.5你是谁？", system='使用英文回答'))
#     # print(_request_tme_chatglm("你是谁？"))
